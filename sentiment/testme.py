import torch
import requests,os
from transformers import AutoModelForSequenceClassification, AutoTokenizer

#os.environ['REQUESTS_CA_BUNDLE']="/etc/ssl/certs/dellca2018-bundle.crt"
#os.environ['REQUESTS_CA_BUNDLE']="./dellca2018-bundle.crt"

# Load the pre-trained tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Prepare the text for sentiment analysis
text = "This movie is amazing! I loved every minute of it."
inputs = tokenizer(text, return_tensors="pt")

# Run the model to predict sentiment
with torch.no_grad():
    outputs = model(**inputs)
    predicted_class_id = outputs.logits.argmax(dim=-1).item()
    predicted_sentiment = model.config.id2label[predicted_class_id]

# Print the predicted sentiment
print(f"The predicted sentiment for the text is: {predicted_sentiment}")