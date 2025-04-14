"""
Este módulo contém a função principal para gerar um PDF a partir de docstrings de um módulo Python.
"""
import importlib
from datetime import datetime
from fpdf import FPDF
from docstring_pdf_converter.generate_pdf import (generate_cover, extract_docstrings,
                                                  docstrings_to_pdf)

def main():
    """
    Função principal que gera um PDF a partir de docstrings extraídas de um módulo Python.

    :return: None
    """
    pdf = FPDF()

    print("Executando o conversor de docstrings para PDF...")
    print("Por favor, preencha as informações da capa do documento.")

    title = input("Digite o título do documento: ")
    subtitle = input("Digite o subtítulo do documento: ")
    institution = input("Digite a instituição (deixe em branco se não houver): ")
    city = input("Digite a cidade: ")

    cover_info = {
        "title": title,
        "subtitle": subtitle,
        "institution": institution,
        "city": city,
        "year": datetime.now().year
    }

    generate_cover(pdf, cover_info)

    module_name = input("Digite o nome do módulo (exemplo: docstring_pdf_converter.exemplo): ")
    module = importlib.import_module(module_name)
    docstrings = extract_docstrings(module)
    docstrings_to_pdf(pdf, docstrings)

    output_filename = input("Digite o nome do arquivo PDF (exemplo: docstrings.pdf): ")
    if not output_filename.endswith(".pdf"):
        output_filename += ".pdf"
    if not output_filename:
        output_filename = "docstrings.pdf"

    pdf.output(output_filename)
    print(f"PDF gerado com sucesso: {output_filename}")

if __name__ == "__main__":
    main()
