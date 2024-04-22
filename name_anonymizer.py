import fasttext
import os

class NameGenderPredictor:
    """
    A node that predicts the gender of a given name using a FastText model.

    Inputs:
    - name (str): The name to predict the gender for.

    Outputs:
    - gender (str): The predicted gender ('male' or 'female').
    """

    NODE_NAME = "Name Gender Predictor"
    NODE_DESC = "Predict the gender of a given name using FastText"
    CATEGORY = "NLP"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "predict_gender"

    def __init__(self):
        super().__init__()
        # Load the pre-trained FastText model
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'vec', 'wiki-news-300d-1M.vec')
        self.model = fasttext.load_model(model_path)

    def predict_gender(self, name):
        # Preprocess the name (optional)
        name = name.strip().title()

        # Make a prediction using the FastText model
        prediction = self.model.predict(name)[0][0]

        # Return the predicted gender
        if prediction == '__label__male':
            return ('male',)
        else:
            return ('female',)

# Register the node
NODE_CLASS_MAPPINGS = {
    "NameGenderPredictor": NameGenderPredictor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NameGenderPredictor": "Name Gender Predictor"
}