from typing import Dict

import kserve
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class SentimentAnalysisModel(kserve.Model):
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        super().__init__(name="sentiment-analyzer")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def preprocess(self, data: Dict) -> Dict:
        text = data.get("text")
        if not text:
            raise ValueError("Missing 'text' field in input data")
        encoded_text = self.tokenizer(text, return_tensors="pt")
        return encoded_text

    def predict(self, data: Dict) -> Dict:
        encoded_text = self.preprocess(data)
        with torch.no_grad():
            output = self.model(**encoded_text)
        logits = output.logits.squeeze(0)
        prediction = int(torch.argmax(logits))
        return {"sentiment": prediction}

if __name__ == "__main__":
    model = SentimentAnalysisModel()
    model_server = kserve.ModelServer(model=model)
    model_server.start()