from PIL import Image, ImageFont
import subprocess
import os
import torch
import numpy as np
import io

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

class ImageTextNode:
    @classmethod
    def INPUT_TYPES(cls):
        font_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

        return {
            "required": {
                "image": ("IMAGE",),
                "text": ("STRING", {"multiline": True}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 32, "min": 1, "max": 256}),
                "text_color": ("STRING", {"default": "#FFFFFF"}),
                "outline_color": ("STRING", {"default": "#000000"}),
                "outline_width": ("INT", {"default": 2, "min": 0, "max": 10}),
                "box_width": ("INT", {"default": 200, "min": 1}),
                "padding": ("INT", {"default": 20, "min": 0}),
                "text_position": (["top", "bottom"], {"default": "bottom"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_text"
    CATEGORY = "image/text"

    def apply_text(self, image, text, font_name, font_size, text_color, outline_color, outline_width, box_width, padding, text_position):
        images_out = []
        for i, img in enumerate(image):
            try:
                pil_image = tensor2pil(img)
                text_color = hex_to_rgb(text_color)
                outline_color = hex_to_rgb(outline_color)
                font_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
                font_path = os.path.join(font_dir, font_name)

                gravity_value = {
                    'top': 'North',
                    'middle': 'Center',
                    'bottom': 'South'
                }.get(text_position, 'South')

                # cmd = f'"convert" ' \
                #       f'-font "{font_path}" ' \
                #       f'-pointsize {font_size} ' \
                #       f'-fill "rgb({text_color[0]},{text_color[1]},{text_color[2]})" ' \
                #       f'-size {box_width}x ' \
                #       f'-background none ' \
                #       f'-gravity {gravity_value} ' \
                #       f'-verbose ' \
                #       f'caption:"{text}" ' \
                #       'png:-'

                cmd = [
                    "convert",
                    "-font", font_path,
                    "-pointsize", str(font_size),  # Convert integer to string
                    "-fill", f"rgb({text_color[0]},{text_color[1]},{text_color[2]})",  # Ensure RGB values are passed correctly
                    "-size", box_width + "x",  # Ensure dimensions are passed as string
                    "-background", "none",
                    "-gravity", gravity_value,
                    "-verbose",
                    "label:" + text,
                    "(",  # Parentheses must be separate elements in the list
                    "+clone",
                    "-background", "white",
                    "-shadow", "80x3+5+5",
                    ")",
                    "+swap",
                    "-background", "none",
                    "-layers", "merge",
                    "+repage",
                    "png:-"
                ]

        
                output = subprocess.check_output(cmd, shell=True)
                text_img = Image.open(io.BytesIO(output))
                text_width, text_height = text_img.size
                # print(text_width, text_height)
                # print(pil_image.width, pil_image.height)
                # combined_img = Image.new('RGBA', (pil_image.width, pil_image.height), (255, 255, 255, 0))
                # text_x = (combined_img.width - text_width) // 2
                # combined_img.paste(pil_image, (0, 0))
                # if text_position == "top":
                    
                #     combined_img.alpha_composite(text_img, (text_x, 0))
                    
                # elif text_position == "middle":
                #     text_y = (combined_img.height - pil_image.height - text_height) // 2
                #     combined_img.alpha_composite(text_img, (text_x, text_y))
                    
                # else:
                    
                #     combined_img.alpha_composite(text_img, (text_x, combined_img.height - text_height))
                # 假设 pil_image 是你的原始图像
                combined_img = Image.new('RGBA', pil_image.size, (0, 0, 0, 0))  # 创建与原始图像相同大小的透明图像
                text_layer = Image.new('RGBA', pil_image.size, (0, 0, 0, 0))  # 创建一个透明图层用于渲染文字

                # 计算文字在图像上的位置
                text_x = (combined_img.width - text_width) // 2

                if text_position == "top":
                    text_y = padding
                elif text_position == "middle":
                    text_y = (combined_img.height - text_height) // 2
                else:  # bottom
                    text_y = combined_img.height - text_height - padding

                # 在透明图层上粘贴文字图像
                text_layer.paste(text_img, (text_x, text_y), text_img)

                # 先将原始图像粘贴到combined_img上
                combined_img.paste(pil_image, (0, 0))

                # 然后将带有文字的透明图层合成到combined_img上
                combined_img.alpha_composite(text_layer, (0, 0))

                # 转换回tensor
                out_tensor = torch.from_numpy(np.array(combined_img).astype(np.float32) / 255.0).unsqueeze(0)
                images_out.append(out_tensor)

                print(f"Successfully processed image {i}")
            except Exception as e:
                print(f"Error processing image {i}: {e}")

        if not images_out:
            print("No images were successfully processed")

        return (torch.cat(images_out, dim=0),)

NODE_CLASS_MAPPINGS = {
    "ImageTextNode": ImageTextNode
}