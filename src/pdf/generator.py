import html
import os

import pdfkit
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer_for_filename
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph

from src.config.settings import PAGE_SIZE, DEFAULT_FONT_SIZE


def _caminho_relativo(file, path):
    try:
        relative_path = os.path.relpath(file, start=path)
        return os.path.join(str(os.path.basename(path)), str(relative_path))
    except ValueError:
        return os.path.basename(file)  # Caso haja erro, retorna o nome do arquivo

class PDFGenerator:
    def __init__(self, font_size=DEFAULT_FONT_SIZE, page_size=PAGE_SIZE):
        self.font_size = font_size
        self.page_size = page_size
        self.styles = getSampleStyleSheet()
        # Estilo personalizado para o código
        self.custom_style = ParagraphStyle(
            'CodeStyle',
            parent=self.styles['Normal'],
            fontName='Courier',
            fontSize=self.font_size,
            textColor=black,
            alignment=TA_LEFT,
            leading=self.font_size * 1.2,
            spaceBefore=2,
            spaceAfter=2
        )

    def generate_simple_pdf(self, files, path, output_path, progress_callback=None):
        """Gera o PDF com texto simples."""
        pdf = SimpleDocTemplate(
            output_path,
            pagesize=self.page_size,
            leftMargin=40,
            topMargin=5,
            rightMargin=5,
            bottomMargin=5
        )
        content = []

        for i, file in enumerate(files, 1):

            display_path = _caminho_relativo(file, path)

            content.append(Paragraph(f"Arquivo: {display_path}", self.styles['Heading3']))
            content.append(Spacer(1, 12))
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        escaped_line = html.escape(line)
                        content.append(Paragraph(escaped_line, self.custom_style))
            except Exception as e:
                error_msg = html.escape(str(e))
                content.append(Paragraph(f"Erro ao processar {display_path}: {error_msg}", self.styles['Normal']))
            if progress_callback:
                progress_callback(i, len(files))
        pdf.build(content)

    @staticmethod
    def generate_indented_pdf(files, path, output_path, progress_callback=None):
        """Gera o PDF com texto indentado."""
        combined_html = ""

        # CSS personalizado para o estilo
        custom_css = """
        <style>
        .custom-code-style pre {
            font-family: Courier, monospace;
            font-size: 17pt;
            line-height: 1.5;
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        </style>
        """

        combined_html += custom_css

        for i, file in enumerate(files, 1):
            # Obtém o caminho relativo
            display_path = _caminho_relativo(file, path)

            combined_html += f"<h1>Arquivo: {display_path}</h1>\n"
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    code = f.read()
                    lexer = guess_lexer_for_filename(file, code)
                    formatter = HtmlFormatter(style='colorful', cssclass='custom-code-style')
                    highlighted_code = highlight(code, lexer, formatter)
                    combined_html += highlighted_code
            except Exception as e:
                combined_html += f"<p>Erro ao processar {display_path}: {html.escape(str(e))}</p>\n"

            if progress_callback:
                progress_callback(i, len(files))

        pdfkit.from_string(combined_html, output_path)