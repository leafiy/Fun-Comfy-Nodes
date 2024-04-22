import os
import math
from pydub import AudioSegment

class AudioDurationNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio_path": ("STRING", {"default": ""}),
                "frame_rate": ("INT", {"default": 30, "min": 1, "max": 120, "step": 1}),
            }
        }

    RETURN_TYPES = ["INT", "FLOAT", "INT"]
    RETURN_NAMES = ["帧数", "时长(FLOAT)", "时长(INT)"]
    FUNCTION = "calculate_duration"
    CATEGORY = "Audio/Video"

    def calculate_duration(self, audio_path, frame_rate):
        if not os.path.isfile(audio_path):
            print(f"音频文件不存在: {audio_path}")
            return [0, 0.0, 0]

        audio = AudioSegment.from_file(audio_path)
        duration_ms = len(audio)
        duration_s = duration_ms / 1000
        frames = math.ceil(duration_s * frame_rate)
        video_duration_ceil = math.ceil(frames / frame_rate)
        print(frames, duration_s, video_duration_ceil)
        return [frames, duration_s, video_duration_ceil]

NODE_CLASS_MAPPINGS = {
    "AudioDurationNode": AudioDurationNode
}