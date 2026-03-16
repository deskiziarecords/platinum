class UniversalTranslator:
    """
    Acts as a semantic bridge between high-level FERROS intents
    and low-level Platinum OS primitives (Letters).
    """
    def __init__(self, letters_library):
        self.library = letters_library
        # Mapping intents to primitive sequences
        self.intent_map = {
            "find_anomaly": ["L007", "L023", "L042"],  # Detection, Inference, Stability
            "optimize_stream": ["L000", "L005", "L010"], # Optimization, Compression, Control
            "synthesize_data": ["L080", "L085", "L090"]  # Synthesis, Transformation, Inference
        }

    def translate(self, intent):
        """
        Translates a high-level FERROS intent into Platinum primitives.
        """
        primitives = self.intent_map.get(intent, ["L001"]) # Default to basic inference
        executions = []
        for p_name in primitives:
            letter = self.library.get(p_name)
            if letter:
                executions.append({
                    "id": p_name,
                    "category": letter.category,
                    "action": f"Executing {letter.name} ({letter.category}) for {intent}"
                })
        return executions
