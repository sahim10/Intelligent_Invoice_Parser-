from transformers import pipeline

fill_mask = pipeline("fill-mask", model="bert-base-uncased")

def clean_with_llm(field_name, field_value):
    if not field_value or field_value.lower() == "unknown":
        prompt = f"The {field_name} is [MASK]."
        result = fill_mask(prompt)
        return result[0]['token_str'].strip()
    return field_value
