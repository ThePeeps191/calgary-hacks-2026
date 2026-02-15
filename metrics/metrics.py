import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

print("metrics.py imports finished")

# Load pretrained emotion model
MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()
EMOTIONS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

# How much each emotion matters
EMOTION_WEIGHTS = {
    "anger": 1.2,
    "disgust": 1.0,
    "fear": 1.4,
    "sadness": 1.1,
    "surprise": 1.0,
    "joy": 0.4,
    "neutral": 0.0
}

def _emotion_probs(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        logits = model(**inputs).logits

    probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]
    return dict(zip(EMOTIONS, probs))


def get_drama_index(text):
    """
    Returns Drama Index from 1 to 100 for any article or speech
    Higher = more emotionally intense or manipulative
    """
    emotions = _emotion_probs(text)

    drama = 0.0
    for emotion, prob in emotions.items():
        drama += prob * EMOTION_WEIGHTS[emotion]

    max_possible = sum(EMOTION_WEIGHTS.values())
    normalized = drama / max_possible

    scaled = normalized ** 0.6

    score = int(round(scaled * 100))
    return max(1, min(100, score))

print("Drama index for 'The economy is collapsing and families are in crisis as radical policies destroy everything.':")
print(get_drama_index("The economy is collapsing and families are in crisis as radical policies destroy everything."))

print("Drama index for 'The inflation rate increased by 0.3% in the last quarter.':")
print(get_drama_index("The inflation rate increased by 0.3% in the last quarter."))