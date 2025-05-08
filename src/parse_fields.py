import re

def extract_line_items(text):
    lines = text.splitlines()
    items = []
    capture = False

    for line in lines:
        if re.search(r'\bItem\b.*\bQty\b.*\bUnit Price\b.*\bTotal\b', line, re.IGNORECASE):
            capture = True
            continue
        if capture:
            if not line.strip():
                break
            parts = re.split(r'\s+', line.strip())
            if len(parts) >= 4:
                items.append({
                    "item": parts[0],
                    "qty": parts[1],
                    "unit_price": parts[2],
                    "total": parts[3]
                })
    return items

def parse_fields(text):
    patterns = {
        "invoice_number": r"Invoice Number[:\s]*([A-Z0-9\-]+)",
        "vendor": r"Vendor[:\s]*(.+)",
        "date": r"Date[:\s]*([\d]{2}/[\d]{2}/[\d]{4})",
        "due_date": r"Due Date[:\s]*([\d]{2}/[\d]{2}/[\d]{4})",
        "total": r"Total[:\s]*\$?([\d,]+\.\d{2})",
    }

    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        extracted[key] = match.group(1).strip() if match else "unknown"

    extracted["line_items"] = extract_line_items(text) or "line items not found"
    return extracted
