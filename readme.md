# Task : Intelligent Invoice Parser (Intermediate AI) - Mohamed Sahim

This project is a web-based Intelligent Invoice Parser built with **Python**, **Flask**, **pdfplumber**, **regex**, and **HuggingFace Transformers**.

It allows users to upload invoice PDFs through a web interface, automatically extracts key information using NLP and regex, validates missing fields using an LLM, and displays results in a clean UI.

---

##  Features

-  Upload invoices in PDF format
-  Extract key fields using Regex:
  - Invoice Number
  - Vendor
  - Total
  - Date
  - Due Date
  - Line Items
-  Fill missing fields using a HuggingFace BERT model
-  Save all outputs to a single JSON file (`all_invoices.json`)
-  Log all uploaded invoices in `all_inputs.json`
-  Download results as JSON
-  Stylish Bootstrap-powered single-page web UI

---

##  Technologies Used

- Python 3
- Flask
- pdfplumber
- regex
- HuggingFace Transformers (`bert-base-uncased`)
- Bootstrap 5 (for frontend)

---

##  Installation

1. Clone the repository:
   git clone <url>
   cd invoice-parser-task

2. Create a virtual environment:


python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

3. Install dependencies:

pip install -r requirements.txt
