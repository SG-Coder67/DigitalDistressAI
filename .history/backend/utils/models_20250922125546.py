from transformers import pipeline

class ToxicityModel:
    def __init__(self):
        # Load pre-trained toxicity classification model
        self.model = pipeline("text-classification", model="unitary/toxic-bert")

    def predict(self, text):
        # Run text through model
        outputs = self.model(text)
        is_toxic = False
        reasons = []

        for out in outputs:
            if out["label"].lower() in ["toxic", "threat", "insult"] and out["score"] > 0.5:
                is_toxic = True
                reasons.append(f"Detected {out['label']} with confidence {out['score']:.2f}")

        return is_toxic, reasons
