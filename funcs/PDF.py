# PDF.py

import os
from fpdf import FPDF

def txt_to_pdf(txt_filename):
    """Converte um arquivo TXT para PDF e salva na pasta PDF."""
    if not os.path.exists(txt_filename):
        print(f"Erro: O arquivo '{txt_filename}' não foi encontrado.")
        return

    output_dir = "pdf"
    os.makedirs(output_dir, exist_ok=True)

    pdf_filename = os.path.join(output_dir, os.path.splitext(os.path.basename(txt_filename))[0] + ".pdf")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(txt_filename, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                pdf.multi_cell(0, 10, line.strip(), align="L")
            else:
                pdf.ln(5)

    pdf.output(pdf_filename)
    print("PDF gerado com sucesso:", pdf_filename)