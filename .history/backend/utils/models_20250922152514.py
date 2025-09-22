from transformers import pipeline

class ToxicityModel:
    def __init__(self):
        from transformers import pipeline
        self.model = pipeline("text-classification", model="unitary/toxic-bert")
        # Add phishing keywords
        self.keywords = ["free-money", "click here", "win now", "claim prize"]

    def predict(self, text):
        # 1️⃣ Check AI toxicity
        outputs = self.model(text)
        is_malicious = False
        reasons = []

        for out in outputs:
            if out["label"].lower() in ["toxic", "threat", "insult"] and out["score"] > 0.5:
                is_malicious = True
                reasons.append(f"Toxicity detected: {out['label']} ({out['score']:.2f})")

        # 2️⃣ Keyword-based phishing detection
        for kw in self.keywords:
            if kw.lower() in text.lower():
                is_malicious = True
                reasons.append(f"Suspicious keyword detected: '{kw}'")

        return is_malicious, reasons
