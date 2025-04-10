"Create the streaming data flow"
import sys
import os
import time
import copy
import threading
import asyncio

from .BLEBleak import BLE_device_instance, get_ble_device_address
from .Experiment import Experiment
# from .OfflineReplay import OfflineData

from ..utils.params import *
from ..utils.WindowFiltering_focus import *

class StreamingFLow:
    "Connect to a device and streaming data"
    def __init__(self, device_id=None, cache_folder='./cache', source=None, data_folder=None, s3_prefix=None, is_split_brain_signal=True):
        '''initializinng parameters, get device_id
        Args:
            device_id: str: if the streaming is in online mode (from a device)
            cache_folder: str: cache foldeer
            data_folder: str: pre-recorded data folder in offline mode, only consider if device_id==None
            source: str: "PC" or "S3":  source of the pre-recorded data, only in offline mode
        '''
        self.device_id = device_id
        self.cache_folder = cache_folder

        
        if self.device_id is not None:
            # If in online mode: create a BLE instantce
            self.Ble_stack = BLE_device_instance()
            # print("self.Ble_stack = BLE_device_instance()") # DEBUG
        else:
            # If in offline mode
            self.data_folder = data_folder
            self.source = source
            self.s3_prefix = s3_prefix

        # All data is stored in:
        # self.experiment.eeg
        # self.experiment.imu
        # self.experiment.ppg

        # Thêm tính toán các giá trị EEG/EOG/EMG
        if is_split_brain_signal:
            self.GetRawBrainComponents = GetRawBrainComponents()
        else:
            self.GetRawBrainComponents = None

    def start_streaming(self):
        "Start the data streaming threads (device -> BLE and BLE -> Experiment)"
        if self.device_id is not None:
        # Online mode processing
            # Set up BLE, connect to the device and start streaming data from the device to the BLE
            self.connect2device(self.device_id)

            #Set up the experiment
            self._createExperiment(self.device_id, cache_folder=self.cache_folder)

            # Start streaming data from the BLE (binary) to the Experiment (numpy)
            self.start_streaming_data_ble_to_databucket()

        else:
        # Offline mode processing
            # Tạo luồng data
            self.OfflineDataProcessor = OfflineData(data_folder=self.data_folder, source=self.source, s3_prefix=self.s3_prefix)
            # print("self.OfflineDataProcessor.eeg_full_data shape: ", self.OfflineDataProcessor.eeg_full_data.shape)

            #Set up the experiment
            self._createExperiment(self.device_id, cache_folder=self.cache_folder)

            # Tạo luồng streaming data offline
            self.start_stream_offline_data()
        
        # Khởi tạo data (khi chưa có update)
        self.eeg = self.experiment.eeg_data[:self.experiment.eeg_data_size, :]
        self.imu = self.experiment.imu_data[:self.experiment.imu_data_size, :]
        self.ppg = self.experiment.ppg_data[:self.experiment.ppg_data_size, :]

    def get_last_window(self, window_in_seconds=1):
        "Lấy data của một window(theo giây) gần nhất"
        data = {
                "EEG": self.eeg[-int(eeg_sampling_rate*window_in_seconds):, :],
                "IMU": self.imu[-int(imu_sampling_rate*window_in_seconds):, :],
                "PPG": self.ppg[-int(ppg_sampling_rate*window_in_seconds):, :],
            }
        return data


    def _ble_initializer(self, address):
        ''' Initilize BLE connection
         :address: ble address of the device'''
        asyncio.run(self.Ble_stack.main(address))

    def connect2device(self, device_id):
        ''' Set up BLE streaming and recording
            Start a threath to run streaming from device to BLE queue (BLE.raw_eeg_data)
        '''
        ble_address = asyncio.run(get_ble_device_address(device_id))
        if ble_address is None: 
            sys.exit('Unable to find device {}'.format(device_id))

        # Start the streaming data from the device to the BLE
        print ("Connecting ....")
        self.init_thread = threading.Thread(name='ble_initializer', target=self._ble_initializer, args=(ble_address,))
        self.init_thread.start()

    def _createExperiment(self, device_id, cache_folder=None):
        '''Create Experiment object which processed and stored data (RAM and disk)'''
        experiment_id = str(time.time())
        if cache_folder is None:
            # Create cache folder if none
            experiment_id_data_path = os.path.join(cache_folder, experiment_id)
        else:
            experiment_id_data_path = os.path.join(cache_folder, experiment_id)
        self.experiment_id_data_path = experiment_id_data_path
        # create experiment object
        self.experiment = Experiment(max_streaming_time_s=max_streaming_time_s, params=all_params, 
                                     device_id=device_id, experiment_id=experiment_id_data_path)
    
    def start_streaming_data_ble_to_databucket(self):
        '''start data streaming thread'''
        print ("Starting streaming ....")
        try: 
            self.stream_thread = threading.Thread(name='ble_stream', target=self._streaming_data_ble_to_databucket)
            self.stream_thread.start()
        except:
            return False
        return True

    # def _split_brain_signals(self):
    #     "cắt electrode data thành các thành phần eeg/eog/emg"
    #     data_to_filter = self.get_last_window(1)
    #     noise_removed_signal, eeg, eog, emg = self.GetRawBrainComponents.filter(data_to_filter)
    #     self.filtered_eeg.append(eeg)
    #     self.filtered_eog.append(eog)
    #     self.filtered_emg.append(emg)
    #     time.sleep(0.9)


        
    def _streaming_data_ble_to_databucket(self):
        """Process binary data received from BLE => convert to int array => append to the experiment's data
        Nơi xử lý từng binary packet trước khi chuyển đi
        """
        clock = time.time()
        expected_sequence_number = None
        
        while True:
            update = False
            self.DATA_SAVED = False

            # Check queue of eeg, ppg, imu; if there are packets of data haven't been processed yet:
            # Get the binary packet from the queue (FIFO)
            # Convert the binary packet -> int array
            # Append the processed data to experiment.eeg_data (memmap)
            if len(self.Ble_stack.raw_eeg_data) == 0:
                time.sleep(0.03) # Tránh hit vòng lặp quá nhiều lần khi không cần thiết

            # Processing eeg
            if len(self.Ble_stack.raw_eeg_data) != 0:
                packet_data = self.Ble_stack.raw_eeg_data.pop(0)
                pc_packet_timestamp = self.Ble_stack.raw_eeg_pc_timestamps.pop(0)
                timestamp, seq_num, channel_data = self.Ble_stack.get_data_from_eeg_binary_packet(packet_data, n_channels=num_eeg_channels)  
                 
                if expected_sequence_number is None:
                    # channel_data: numpy array: packet of EEG data
                    self.experiment.add_eeg_data(channel_data, pc_packet_timestamp, timestamp)
                #     expected_sequence_number = (seq_num+1)%256
                    update = True
                # else:
                #     if seq_num != expected_sequence_number:
                #         print('Sequence received:', seq_num, " Expected one:", expected_sequence_number)
                #         print('Missing or Duplicate packet')
                #         expected_sequence_number = (seq_num+1)%256
                #     else:
                #         self.experiment.add_eeg_data(channel_data, pc_packet_timestamp, timestamp)
                #         expected_sequence_number = (expected_sequence_number+1)%256
                #         update = True
                
            # Processing imu
            if len(self.Ble_stack.raw_imu_data) != 0:
                packet_data = self.Ble_stack.raw_imu_data.pop(0)
                pc_packet_timestamp = self.Ble_stack.raw_imu_pc_timestamps.pop(0)
                timestamp, data = self.Ble_stack.get_data_from_imu_binary_packet(packet_data, n_channels=num_imu_channels)
                # data: numpy array: packet of IMU data
                self.experiment.add_imu_data(data, pc_packet_timestamp) 
                update = True

            # Processing ppg
            if len(self.Ble_stack.raw_ppg_data) != 0:
                packet_data = self.Ble_stack.raw_ppg_data.pop(0)
                pc_packet_timestamp = self.Ble_stack.raw_ppg_pc_timestamps.pop(0)
                timestamp, data = self.Ble_stack.get_data_from_ppg_binary_packet(packet_data, n_channels=num_ppg_channels) 
                # data: numpy array: packet of PPG data
                self.experiment.add_ppg_data(data, pc_packet_timestamp)
                update = True
                
            if update:
                self.eeg = self.experiment.eeg_data[:self.experiment.eeg_data_size, :]
                self.imu = self.experiment.imu_data[:self.experiment.imu_data_size, :]
                self.ppg = self.experiment.ppg_data[:self.experiment.ppg_data_size, :]

                current_time = time.time()
                if current_time-clock > data_save_frequency:
                    # Save experiment data
                    self.experiment.save_data()
                    clock = current_time
                    self.DATA_SAVED = True

    def start_stream_offline_data(self):
        "Tạo thread để tạo luồng stream giả cho một bộ data offline"
        self.offline_stream_thread = threading.Thread(name='offline_stream', target=self._to_streaming_offline_data)
        self.offline_stream_thread.start()

    def _to_streaming_offline_data(self, frequency=10):
        "Thực hiện cắt dữ liệu để luồng streaming offline trông giống như một luồng online"
        # remain_seconds: toàn bộ số giây mà data có => mỗi lần cắt đi một chút đến khi hết thì thôi
        remain_seconds = self.OfflineDataProcessor.eeg_full_data.shape[0]/eeg_sampling_rate
        end_second=0 # điểm kết thúc của block trước đó
        
        while remain_seconds >0:
            start_second = end_second # điểm bắt đầu của block hiện tại
            end_second = start_second+1/frequency # điểm kết thúc của block hiện tại
            
            # EEG: get a block and add to the Experiment
            eeg_package = self.OfflineDataProcessor.eeg_full_data[ int(start_second*eeg_sampling_rate):int(end_second*eeg_sampling_rate),:]
            self.experiment.add_eeg_data(data=eeg_package, pc_timestamp=start_second, timestamp=start_second)

            # IMU: get a block and add to the Experiment
            imu_package = self.OfflineDataProcessor.imu_full_data[ int(start_second*imu_sampling_rate):int(end_second*imu_sampling_rate),:]
            self.experiment.add_imu_data(data=imu_package, timestamp=start_second)

            # PPG: get a block and add to the Experiment
            ppg_package = self.OfflineDataProcessor.ppg_full_data[ int(start_second*ppg_sampling_rate):int(end_second*ppg_sampling_rate),:]
            self.experiment.add_ppg_data(data=ppg_package, timestamp=start_second)

            # 20230213            
            self.eeg = self.experiment.eeg_data[:self.experiment.eeg_data_size, :]
            self.imu = self.experiment.imu_data[:self.experiment.imu_data_size, :]
            self.ppg = self.experiment.ppg_data[:self.experiment.ppg_data_size, :]

            time.sleep(1/frequency)


    def exit_signal_handler(self):
        """
        Xử lý phần dữ liệu còn tồn trong queue nhưng chưa xử lý xong + lưu data
        
        """
        # global expected_sequence_number, DATA_SAVED
        print('Exiting...')
        expected_sequence_number  = None
        # Save any additionall EEG data still in the raw data buffer
        remaining_eeg_data = copy.deepcopy(self.Ble_stack.raw_eeg_data)
        remaining_eeg_pc_timestamps = copy.deepcopy(self.Ble_stack.raw_eeg_pc_timestamps)
        while len(remaining_eeg_data) > 0:
            packet_data = remaining_eeg_data.pop(0)
            pc_packet_timestamp = remaining_eeg_pc_timestamps.pop(0)
            timestamp, seq_num, channel_data = self.Ble_stack.get_data_from_eeg_binary_packet(packet_data, n_channels=num_eeg_channels)
            if expected_sequence_number is None:
                self.experiment.add_eeg_data(channel_data, pc_packet_timestamp, timestamp)
                # expected_sequence_number = (seq_num+1)%256
            # else:
            #     if seq_num != expected_sequence_number:
            #         print('Missing or Duplicate packet')
            #         continue
            #     else:
            #         self.experiment.add_eeg_data(channel_data, pc_packet_timestamp, timestamp)
            #         expected_sequence_number = (expected_sequence_number+1)%256

        # Save IMU data still in the raw data buffer
        remaining_imu_data = copy.deepcopy(self.Ble_stack.raw_imu_data)
        remaining_imu_pc_timestamps = copy.deepcopy(self.Ble_stack.raw_imu_pc_timestamps)
        while len(remaining_imu_data) > 0:
            packet_data = remaining_imu_data.pop(0)
            pc_packet_timestamp = remaining_imu_pc_timestamps.pop(0)
            timestamp, data = self.Ble_stack.get_data_from_imu_binary_packet(packet_data, n_channels=num_imu_channels)
            self.experiment.add_imu_data(data, pc_packet_timestamp)

        # Save PPG data still in the raw data buffer
        remaining_ppg_data = copy.deepcopy(self.Ble_stack.raw_ppg_data)
        remaining_ppg_pc_timestamps = copy.deepcopy(self.Ble_stack.raw_ppg_pc_timestamps)
        while len(remaining_ppg_data) > 0:
            packet_data = remaining_ppg_data.pop(0)
            pc_packet_timestamp = remaining_ppg_pc_timestamps.pop(0)
            timestamp, data = self.Ble_stack.get_data_from_ppg_binary_packet(packet_data, n_channels=num_ppg_channels)
            self.experiment.add_ppg_data(data, pc_packet_timestamp)

        self.experiment.save_data()
        print('Data saved')
            
        self.Ble_stack.close()
        # sys.exit(0)
        os._exit(0)

class GetRawBrainComponents:
    def __init__(self) -> None:
        self.BaseFilter = WindowFilter([WindowIIRNotchFilter(60, 12, 125), \
                           WindowIIRNotchFilter(50, 10, 125)]) 
        self.EogFilter = WindowFilter([ WindowButterBandpassFilter(2, 0.3, 10, 125)])
        self.EegFilter = WindowFilter([ WindowButterBandpassFilter(2, 1, 20, 125)])
        self.Emg_Filter = WindowFilter([ WindowButterHighpassFilter(2, 20, 125)])

    def filter(self, data):
        noise_removed_signal = self.BaseFilter.filter_data(data)
        eog = self.EogFilter.filter_data(noise_removed_signal)
        eeg = self.EegFilter.filter_data(noise_removed_signal)
        emg = self.Emg_Filter.filter_data(noise_removed_signal)
        return noise_removed_signal, eeg, eog, emg