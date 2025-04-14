"""
Este módulo contém funções para gerar um PDF a partir de docstrings extraídas de um módulo Python.
"""
import inspect
from docstring_pdf_converter.config import PDF_CONFIG

def extract_docstrings(module):
    """
    Extrai docstrings de classes e funções de um módulo Python e retorna uma string formatada.

    :param module: O módulo Python do qual as docstrings serão extraídas.
    :type module: module
    :return: Uma string formatada contendo as docstrings extraídas.
    :rtype: str
    """
    module_counter = 1
    docstrings = [f"{module_counter}.   {module.__name__}\n"]
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            class_counter = 1
            docstrings.append(f"{module_counter}.{class_counter}    {name}\n")
            for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                method_counter = 1
                docstring = inspect.getdoc(method)
                if docstring:
                    docstrings.append(f"{module_counter}.{class_counter}.{method_counter}   "
                                      f"{method_name}\n{docstring}\n")
                    method_counter += 1
            class_counter +=1
        elif inspect.isfunction(obj):
            function_counter = 1
            docstring = inspect.getdoc(obj)
            if docstring:
                docstrings.append(f"{module_counter}.{function_counter}     {name}\n{docstring}\n")
                function_counter += 1
    return "\n".join(docstrings)

def generate_cover(pdf, cover_info):
    """
    Gera a capa do PDF com o título, subtítulo, instituição, cidade e ano.

    :param pdf: Instância do objeto PDF.
    :type pdf: FPDF
    :param cover_info: Dicionário contendo as informações da capa.
    :return: None
    """
    pdf.set_auto_page_break(auto=False)

    pdf.set_left_margin(PDF_CONFIG["margin_left"])
    pdf.set_top_margin(PDF_CONFIG["margin_top"])
    pdf.set_right_margin(PDF_CONFIG["margin_right"])

    pdf.add_page()

    pdf.set_font(PDF_CONFIG["font"], "B", PDF_CONFIG["font_size"])
    pdf.cell(0, 10,
             f"{cover_info["institution"].upper()
             if cover_info["institution"]
             else 'AUTOR INDEPENDENTE'}", ln=True, align="C")

    # Pular 8 linhas
    for _ in range(8):
        pdf.ln(10)

    pdf.cell(0, 10, f"{cover_info["title"].upper()}", ln=True, align="C")
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 10, f"{cover_info["subtitle"]}", ln=True, align="C")

    # Calcular a posição para a cidade e o ano
    pdf.set_font(PDF_CONFIG["font"], "B", PDF_CONFIG["font_size"])
    page_height = pdf.h - PDF_CONFIG["margin_bottom"]
    pdf.set_y(page_height - 20)
    pdf.set_font(PDF_CONFIG["font"], "B", PDF_CONFIG["font_size"])
    pdf.cell(0, 10, f"{cover_info["city"].upper()}", ln=True, align="C")
    pdf.cell(0, 10, f"{cover_info["year"]}", ln=True, align="C")

def add_page_number(pdf):
    """
    Adiciona o número da página no canto superior direito do PDF.

    :param pdf: Instância do objeto PDF.
    :type pdf: FPDF
    :return: None
    """
    pdf.set_y(10)
    pdf.set_x(pdf.w - PDF_CONFIG["margin_right"] - 20)
    pdf.set_font(PDF_CONFIG["font"], "", PDF_CONFIG["font_size"])
    pdf.cell(0, 10, f"{pdf.page_no()}", 0, 0, 'R')

def docstrings_to_pdf(pdf, docstrings):
    """
    Converte as docstrings extraídas em um PDF formatado.

    :param pdf: Instância do objeto PDF.
    :param docstrings: String formatada contendo as docstrings extraídas.
    :return: None
    """
    pdf.add_page()
    pdf.set_auto_page_break(auto=PDF_CONFIG["auto_page_break"], margin=PDF_CONFIG["break_margin"])

    for line in docstrings.split('\n'):
        if line.startswith("1. "):
            pdf.set_font(PDF_CONFIG["font"], PDF_CONFIG["title_format"]["level_1"]["style"],
                         PDF_CONFIG["title_format"]["level_1"]["size"])
        elif line.startswith("1.1 "):
            pdf.set_font(PDF_CONFIG["font"], PDF_CONFIG["title_format"]["level_2"]["style"],
                         PDF_CONFIG["title_format"]["level_2"]["size"])
        elif line.startswith("1.1.1 "):
            pdf.set_font(PDF_CONFIG["font"], PDF_CONFIG["title_format"]["level_3"]["style"],
                         PDF_CONFIG["title_format"]["level_3"]["size"])
        else:
            pdf.set_font(PDF_CONFIG["font"], "", PDF_CONFIG["font_size"])
        pdf.multi_cell(0, 10, line)

    for page_num in range(2, pdf.page_no() + 1):
        pdf.page = page_num
        add_page_number(pdf)
