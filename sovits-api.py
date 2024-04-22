import comfy.utils
import requests
import os
from datetime import datetime
import re

class GPTSOVITSAudio:
    def __init__(self):
        self.output_audio = None
        self.output_path = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "请输入要合成的文本..."
                }),
                "text_language": (["中文", "en", "ja"], {
                    "default": "中文",
                    
                }),
                "refer_wav_path": ( ["Keira.wav", "smoke.wav", "麻辣烫.wav"], {
                    "default": "Keira.wav"
                      # 添加更多选项
                }),
                "prompt_language": (["中文", "en", "ja"], {
                    "default": "中文",
                   
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_audio"
    CATEGORY = "GPT-SO-VITS"

    def generate_audio(self, text, text_language, refer_wav_path, prompt_language):
        api_url = "http://127.0.0.1:9880"
        text = re.sub(r'\[/\\]+', '', text)

        # 定义一个类似JavaScript对象的字典,根据refer_wav_path设置对应的prompt_text
        prompt_text_map = {
            "Keira.wav": "光动嘴不如亲自做给你看,等我一下呀",
            "smoke.wav": "哦,你昨天晚上终于让客人签约了?",
            "麻辣烫.wav": "平凡如你我，再平凡的一天也可以来上这么一碗平凡不平淡的麻辣烫"

        }

        # 根据选择的refer_wav_path获取对应的prompt_text
        prompt_text = prompt_text_map.get(refer_wav_path, "")

        data = {
            "text": text,
            "text_language": text_language
        }
        if refer_wav_path and prompt_text and prompt_language:
            data["refer_wav_path"] = refer_wav_path
            data["prompt_text"] = prompt_text
            data["prompt_language"] = prompt_language

        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            audio_data = response.content
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(current_dir, "sovits-output")
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            text_short = re.sub(r'\[\n\r\t\s]+', '_', text[:10])
            text_short = re.sub(r'[\\/:\*?"<>|]', '', text_short)
            output_filename = f"{text_short}_{timestamp}.wav"
            self.output_path = os.path.join(output_dir, output_filename)
            with open(self.output_path, "wb") as file:
                file.write(audio_data)
            print(f"音频文件已保存到: {self.output_path}")
        else:
            error_message = response.json()["error"]
            print(f"请求失败,错误信息: {error_message}")
            self.output_audio = None
            self.output_path = ""

        return (self.output_path,)

NODE_CLASS_MAPPINGS = {
    "GPTSOVITSAudio": GPTSOVITSAudio
}