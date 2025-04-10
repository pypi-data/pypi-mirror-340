"""Calculate STATE of the user
tổng hợp từ 2 nguồn : Low-level state và High-level state,
STATE: { input: raw signals; output: state }
versus 
HLS: { input: STATE; output: state }

Version:
v1.x: chỉ bao gồm các scores hiện đã có (trước 1/2/2023)
"""
# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import time
import datetime
import numpy as np

from ..utils.params import imu_sampling_rate
from .algorithms.posture import get_posture
# from STATE.algorithms.posture_2 import get_posture as get_posture2
from .algorithms.poas import POAs_Calculator
# from .algorithms.focus import Focus_Calculator
from .algorithms.respiratory_rate import calculate_respiratory_rate
# from STATE.algorithms.gesture import detect_gaze
# from STATE.HLS import HLS_Inferor
from .algorithms.gesture_2 import BlinkDetection#, GazeDetection
from .algorithms.gaze_3 import GazeDetection
from .algorithms.emg_event_detection import emg_event_exists
from ..utils.WindowFiltering_focus import *
import copy
# from .utils.signal_processing import preprocess_eog


class StatesCalculator:
    "Khởi tạo, lưu trữ, cung cấp hàm tính STATE từ raw data"
    def __init__(self) -> None:
        self.all_states = {}

        # State khởi tạo
        # self.all_states["welcome_message"] = 'No' # 02Feb: "No" là giá trị mặc định ban đầu => không cần khởi tạo
        # self.all_states["remind_laydown"]='No'
        self.all_states["start_time"]= time.time()

        # Khởi tạo container cho historical STATE
        # self.all_states["posture_array"] = []

        # Khởi tạo, load các model cần cho tính chỉ số
        ## Tính POAS
        self.POAs_Calculator = POAs_Calculator()

        ## Tính Focus score
        # self.Focus_Calculator = Focus_Calculator()

        ## Tính HLS
        # self.HLS_Inferor = HLS_Inferor()

        ## Detect Blink, Gaze
        self.BlinkDetection = BlinkDetection()
        self.GazeDetection  = GazeDetection()
        self.EOGFilter = {}
        
        base_eog_filter = WindowFilter([
                            WindowIIRNotchFilter(60, 12, 125),
                            WindowIIRNotchFilter(50, 10, 125),
                            WindowButterBandpassFilter(2, 0.3, 10, 125)]) 
        self.EOGFilter = {i:copy.deepcopy(base_eog_filter) for i in ["lf", "rf","otel", "oter"]}


    def __getitem__(self, key):
        "Slicing STATE object to get a STATE"
        if key in self.all_states.keys():
            # Nếu tồn tại STATE key thì trả về giá trị hiện tại của STATE
            out = self.all_states[key]
        else:
            if key[:7] == "array__":
                out = []
            else:
                # Nếu không tồn tại STATE key thì gán giá trị No cho key đó (không báo lỗi)
                out = "No"
                # self.all_states[key] = out # Không lưu, tất cả value nếu không có key thì đều là "No"
        return out 

    def get(self, key):
        "API like python dictionary"
        return self[key]
    
    def __setitem__(self, key, value):
        "Set value to STATE"
        self.all_states[key] = value

    def update(self, STATE, stored_array=True):
        """
        Update all_states by a new STATE dictionary
        Params
            STATE: dict: states that need to be updated
            stored_array: bool: are that states would be stored in memory arrays?"""
        # Update state hiện tại
        self.all_states.update(STATE)

        # Append vào list của biến array__{score đang xét}
        if stored_array:
            available_keys = self.all_states.keys()
            # print("STATE available_keys: ", available_keys)
            for score_key in STATE.keys():
                if ("array__"+score_key) not in available_keys:
                    self.all_states["array__"+score_key] = []
                else:
                    self.all_states["array__"+score_key].append(STATE[score_key])
                # self["array__"+score_key].append(STATE[score_key])
                # print("APPEND: ", "array__"+score_key, " To value: " , STATE[score_key])

    def update_STATE_atstart(self):
        """ 
        Update STATE at the beginning of the session, one time only
        No params needed (using LLS to infer)
        """
        current_bedtime = get_decimal_hour(datetime.datetime.fromtimestamp(self["start_time"]))
        scores = {"BEDTIME":current_bedtime}
        # print("STATE.current_bedtime: ", current_bedtime)
        # if (self["PURPOSE"] == 'DEEP_SLEEP') and ((current_bedtime>20) or (current_bedtime<8)):
        #     # ONly check bedtime if the user use a sleep session (not a nap) and they start session at night
        #     last_average_bedtime = self["BEDTIME_2d"]
        #     recommended_bedtime = 22

        #     BETTER_BEDTIME = self.HLS_Inferor.is_better_bedtime(last_average_bedtime, current_bedtime, recommended_bedtime)
        #     print("BETTER_BEDTIME: ", BETTER_BEDTIME)
        #     scores["BETTER_BEDTIME"] = BETTER_BEDTIME

        self.update(scores, stored_array=False)
    
    @staticmethod
    def eye_map_value_to_state(value):
        """
        Mapping đầu ra của model eye detection (từ score 0-1) về dạng state: sure open, open, close, sure close
        """
        if type(value) == list:
            value = value[0]

        if value is None:
            return None 
        elif value <= 0.1:
            return "sure_close"
        elif value <= 0.2:
            return "close"
        elif value <= 0.5:
            return "open"
        else:
            return "sure_open"
        
    def update_STATE_1s(self, data_4s, data_3s):
        """
        Get Low level score, which update with frequency of 1s
        Params:
            data_4s: dict: với 3 keys: EEG, IMU, PPG
        """
        data_4s_eeg = data_4s["EEG"].T
        data_3s_eeg = data_3s["EEG"].T
        lf5 = data_3s_eeg[0]
        rf6 = data_3s_eeg[3]

        otel = data_3s_eeg[1]
        oter = data_3s_eeg[4]
        # print("rf6.SHAPE: ", rf6.shape)

        # gesture_id = detect_gaze(lf5, rf6, fs=125)
        eog_otel = self.EOGFilter["otel"].filter_data(otel)[-125*2:]
        eog_oter = self.EOGFilter["oter"].filter_data(oter)[-125*2:]
        is_blink = self.BlinkDetection.get_blink(otel_data=eog_otel, oter_data=eog_oter)

        eog_lf = self.EOGFilter["lf"].filter_data(lf5)[-125*2:]
        eog_rf = self.EOGFilter["rf"].filter_data(rf6)[-125*2:]
        # print("CHECK lf5: ", lf5.shape)
        # eog_lf = preprocess_eog(lf5, 125)[-125*2:]
        # eog_rf = preprocess_eog(rf6, 125)[-125*2:]
        gesture_id = self.GazeDetection.get_gaze(eog_lf, eog_rf) #lf5, rf6)
        gesture_map = {1:"eye_left", -1:"eye_right", 0:"undetected"}
        gesture_id = gesture_map[gesture_id]

        # emg_event, emg_event_channel = emg_event_exists([lf5[-125*2:], rf6[-125*2:]], 125)
        emg_event, emg_event_channel = emg_event_exists([otel[-125*2:], oter[-125*2:]], 125)

        if emg_event:
            current_gesture = 'emg'
            if emg_event_channel == "left":
                current_gesture = 'emg_left'
            elif emg_event_channel == "right":
                current_gesture = 'emg_right'
        elif is_blink:
            current_gesture = 'blink'
        elif gesture_id == 'eye_left':
            current_gesture = 'eye_left'
        elif gesture_id == 'eye_right':
            current_gesture = 'eye_right'
        else:
            current_gesture = 'normal'
            

        data_1s_imu = data_4s["IMU"]
        # posture_1s = get_posture(data=data_1s_imu.T[:,-(imu_sampling_rate*2):], imu_fs=imu_sampling_rate, window_size=2)
        
        scores = {
            # "eog_lf": eog_lf,
            "eye_gesture": gesture_id,
            "eye_blink": is_blink, 
            "emg_event": emg_event, 
            "current_gesture": current_gesture,
            "emg_event_channel":emg_event_channel
            # "posture_1s": posture_1s
        }

        print(scores)
        self.update(scores)

    def update_STATE_2s(self, data_2s, data_30s):
        """
        Get low level scores, which update with frequencies of 2s
        Params
            data_5s: dict: với 3 keys: EEG, IMU, PPG
        """
        data_2s_eeg = data_2s["EEG"].T
    
        data_30s_imu = data_30s["IMU"].T
        data_30s_ppg = data_30s["PPG"].T

        # focus_score = self.Focus_Calculator.get_focus(data_2s_eeg)
        # respiratory_rate = calculate_respiratory_rate(imu_segment=data_30s_imu, ppg_segment=data_30s_ppg)  # NOTE: OFF FOR DEBUG
        
        # EYE_score = self.Focus_Calculator.get_eyeStage()

        # EYE_ST = self.eye_map_value_to_state(EYE_score)

        # Tập hợp các state được tính trong mỗi 2s -> update STATE
        # scores = {
        #     "focus": focus_score,
        #     # "respiratory_rate":respiratory_rate, # NOTE: OFF FOR DEBUG
        #     "EYE_score": EYE_score,
        #     "EYE_ST" : EYE_ST
        # }
        
        # v1: thinking và stress được tính thông qua focus
        # TODO: v2: các thuật toán riêng cho thinking và stress
        # if focus_score > 0.65:
        #     THINKING_ST = 'high'
        #     scores["THINKING_ST"] = THINKING_ST
        # if focus_score > 0.7:
        #     STRESS_ST = 'high'
        #     scores["STRESS_ST"] = STRESS_ST
        
        # self.update(scores)

    def update_STATE_5s(self, data_5s):
        """
        Get low level scores, which update with frequencies of 5s
        Params
            data_5s: dict: với 3 keys: EEG, IMU, PPG
        """
        data_5s_imu = data_5s["IMU"]
        # data_30s_imu = data_30s["IMU"]

        # Tính posture: từ 20230214: chia X8/X2 ngay trong chính function tính posture
        # Chỉ chia case trên PC, trên mobile đã có phiên bản tính r nên không cần chia case
        # if self["DEVICE_TYPE"] == 'X8':
        #     posture = get_posture2(data_5s_imu.T)
        # else:
        #     posture = get_posture(data=data_5s_imu.T, imu_fs=imu_sampling_rate, window_size=5)[0]
        # print("data_5s_imu: ", data_5s_imu)
        posture = get_posture(data=data_5s_imu.T, imu_fs=imu_sampling_rate, window_size=5)
        

        # Tập hợp các state được tính trong mỗi 5s -> update STATE
        scores = {
            "posture": posture
        }
        
        self.update(scores)

    def update_STATE_30s(self, data_30s):
        """ Tính các score với tần số 30s, input data=30s
        Params
            data_30s: dict: với 3 keys: EEG, IMU, PPG
        """
        data_30s_eeg = data_30s["EEG"].T
        epoch_poas, sleep_stage = self.POAs_Calculator.get_poas_and_sleepstage(data_30s_eeg)
        scores = {
            "poas": epoch_poas,
            'sleep_stage': sleep_stage
        }
        self.update(scores)

        # Sleep progress
        # if len (self["array__poas"])>=6:
            # SLEEP_PROGRESS = self.HLS_Inferor.get_sleep_progress(self["array__poas"])

        #     self.update({
        #         "SLEEP_PROGRESS": SLEEP_PROGRESS,
            # })
        if len (self["array__poas"])>=10:
            poas_5m = np.mean(self["array__poas"][-10:])

            self.update({
                "poas_5m": poas_5m,
            })

def get_decimal_hour(dt):
    total_seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    return float(total_seconds) / 3600