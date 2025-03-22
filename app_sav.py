from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = FastAPI()

class TextInput(BaseModel):
    text: str

# Charger le modèle et le tokenizer
tokenizer = AutoTokenizer.from_pretrained("./")
model = AutoModelForSequenceClassification.from_pretrained(
    "./", 
    local_files_only=True
)

@app.post("/predict/")
def predict(input: TextInput):
    inputs = tokenizer(input.text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    prediction = torch.softmax(outputs.logits, dim=1)
    sentiment = "Positif" if torch.argmax(prediction) == 1 else "Négatif"
    return {"sentiment": sentiment, "score": prediction.tolist()}
