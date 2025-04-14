"""
Testes para o módulo generate_pdf.py
"""

from fpdf import FPDF
from docstring_pdf_converter.generate_pdf import (extract_docstrings, generate_cover,
                                                  docstrings_to_pdf)
from docstring_pdf_converter import exemplo

def test_extract_docstrings():
    """
    Testa a função extract_docstrings para garantir que as docstrings são extraídas
    :return: None
    """

    docstrings = extract_docstrings(exemplo)
    assert "1.   docstring_pdf_converter.exemplo" in docstrings
    assert "1.1    ClasseExemplo" in docstrings
    assert "1.1.1   __init__" in docstrings
    assert "1.1.1   metodo_exemplo" in docstrings
    assert "1.1     funcao_exemplo" in docstrings

def test_generate_cover():
    """
    Testa a função generate_cover para garantir que a capa do PDF é gerada corretamente.

    :return: None
    """

    pdf = FPDF()
    cover_info = {
        "title": "Documentação do projeto",
        "subtitle": "Conversão de docstring para PDF",
        "institution": "",
        "city": "São Paulo",
        "year": "2025"
    }
    generate_cover(pdf, cover_info)
    assert pdf.page_no() == 1

def test_docstrings_to_pdf():
    """
    Testa a função docstrings_to_pdf para garantir que as docstrings são adicionadas
    corretamente ao PDF.

    :return: None
    """

    pdf = FPDF()
    docstrings = (
        "1.   docstring_pdf_converter.exemplo\n"
        "1.1    ClasseExemplo\n"
        "1.1.1   __init__\n"
        "Inicializa a ClasseExemplo.\n"
        "1.1.2   metodo_exemplo\n"
        "Este é um método de exemplo.\n"
        "1.2    funcao_exemplo\n"
        "Esta é uma função de exemplo.\n"
    )

    docstrings_to_pdf(pdf, docstrings)
    assert pdf.page_no() == 1
