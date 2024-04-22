class SplitTextByLineWidth:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_text": ("STRING", {
                    "multiline": True,
                    "default": "在此输入您的文本..."
                }),
                "line_width": ("INT", {
                    "default": 30,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "number"
                }),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_with_newlines",)
    
    FUNCTION = "split_text"
    
    CATEGORY = "Text"
    
    def split_text(self, input_text, line_width):
        lines = []
        current_line = ""
        
        for char in input_text:
            if char == "\n":
                lines.append(current_line)
                current_line = ""
            elif len(current_line.encode("gbk")) + len(char.encode("gbk")) <= line_width:
                current_line += char
            else:
                lines.append(current_line)
                current_line = char
        
        if current_line:
            lines.append(current_line)
        
        output_text = "\n".join(lines)
        print(output_text)
        return (output_text,)

NODE_CLASS_MAPPINGS = {
    "SplitTextByLineWidth": SplitTextByLineWidth,
}