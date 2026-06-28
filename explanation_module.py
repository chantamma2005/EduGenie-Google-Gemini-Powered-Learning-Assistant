# explanation_module.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load the improved model for explanations
explain_tokenizer = AutoTokenizer.from_pretrained(
    "MBZUAI/LaMini-Flan-T5-783M"
)
explain_model = AutoModelForSeq2SeqLM.from_pretrained(
    "MBZUAI/LaMini-Flan-T5-783M"
)

def explain_topic(topic: str) -> str:
    input_text = (
        f"Explain the concept of '{topic}' in a simple and clear way for a school student."
    )

    inputs = explain_tokenizer(input_text, return_tensors="pt")

    outputs = explain_model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        do_sample=True
    )

    explanation = explain_tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return explanation