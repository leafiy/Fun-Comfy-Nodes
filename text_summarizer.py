from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

class TextSummarizer:
    NODE_NAME = "Text Summarizer"
    NODE_DESC = "Extract central idea or summary from text using Sumy"
    CATEGORY = "NLP"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "length": ("INT", {"default": 5, "min": 1, "max": 20, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "summarize_text"
    
    def summarize_text(self, text, length):
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LuhnSummarizer()
        summary = summarizer(parser.document, length)
        summary_text = " ".join([str(sentence) for sentence in summary])
        return (summary_text,)

NODE_CLASS_MAPPINGS = {
    "TextSummarizer": TextSummarizer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextSummarizer": "Text Summarizer"
}