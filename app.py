from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import mysql.connector

app = FastAPI()

# Configurer la connexion à la base de données MySQL
db_config = {
    'host': '127.0.0.1',       # Remplacez par l'adresse IP de votre serveur MySQL
    'user': 'root',            # Nom d'utilisateur MySQL
    'password': 'Mdo56deDepf2Zd1gpmfjD',       # Mot de passe MySQL
    'database': 'ai_engineer'               # Nom de la base de données
}

class TextInput(BaseModel):
    text: str

class FeedbackInput(BaseModel):
    text: str
    sentiment: str
    feedback: bool

@app.post("/predict/")
@app.post("/predict/")
def predict(input: TextInput):
    inputs = tokenizer(input.text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    prediction = torch.softmax(outputs.logits, dim=1)
    sentiment = "Positif" if torch.argmax(prediction) == 1 else "Négatif"
    return {"sentiment": sentiment, "score": prediction.tolist()}

@app.post("/feedback/")
def save_feedback(input: FeedbackInput):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "INSERT INTO feedbacks (text, sentiment, feedback) VALUES (%s, %s, %s)"
        values = (input.text, input.sentiment, input.feedback)
        
        cursor.execute(sql, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"message": "Feedback enregistré avec succès !"}
    
    except mysql.connector.Error as e:
        return {"error": str(e)}
