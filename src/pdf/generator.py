import html
import os

import pdfkit
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer_for_filename

from src.config.settings import PAGE_SIZE, DEFAULT_FONT_SIZE


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
            textColor='black',
            alignment=TA_LEFT,
            leading=self.font_size * 1.5,
            spaceBefore=5,
            spaceAfter=5
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

            display_path = self._caminho_relativo(file, path)

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

    def _caminho_relativo(self, file, path):
        """Obtém o caminho relativo do arquivo em relação ao projeto."""
        selected_folder_name = os.path.basename(path)
        relative_path = os.path.relpath(file, start=path)
        return os.path.join(selected_folder_name, relative_path)

    def generate_indented_pdf(self, files, path, output_path, progress_callback=None):
        """Gera o PDF com texto indentado."""
        combined_html = ""
        for i, file in enumerate(files, 1):
            # Obtém o caminho relativo
            display_path = self._caminho_relativo(file, path)

            combined_html += f"<h3>Arquivo: {display_path}</h3>\n"
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    code = f.read()
                    lexer = guess_lexer_for_filename(file, code)
                    formatter = HtmlFormatter(style='colorful', full=True)
                    highlighted_code = highlight(code, lexer, formatter)
                    combined_html += highlighted_code
            except Exception as e:
                combined_html += f"<p>Erro ao processar {display_path}: {html.escape(str(e))}</p>\n"
            if progress_callback:
                progress_callback(i, len(files))
        pdfkit.from_string(combined_html, output_path)


    # def generate_pdf(self, files, output_path, progress_callback=None):
    #     combined_html = ""
    #     total_files = len(files)
    #
    #     for i, file in enumerate(files, 1):
    #         combined_html += f"<h3>Arquivo: {file}</h3>\n"
    #
    #         # Destacar sintaxe do código
    #         highlighted_code = highlight_code(file)
    #
    #         if highlighted_code:
    #             combined_html += f"{highlighted_code}\n"
    #         else:
    #             combined_html += f"<p>Erro ao processar {file}</p>\n"
    #
    #         if progress_callback:
    #             progress_callback(i, total_files)
    #
    #     # Gerar PDF a partir do HTML concatenado
    #     pdfkit.from_string(combined_html, output_path)
    #
    # def highlight_code(self, file_path):
    #     """Usa Pygments para destacar o código de acordo com a linguagem do arquivo"""
    #     try:
    #         # Detecta o lexer adequado para o arquivo com base na extensão
    #         lexer = get_lexer_for_filename(file_path)
    #     except Exception:
    #         lexer = None  # Se não encontrar o lexer, não fará o destaque
    #
    #     if lexer:
    #         with open(file_path, 'r', encoding='utf-8') as f:
    #             code = f.read()
    #
    #         # Converte o código em HTML estilizado
    #         formatter = HtmlFormatter(style='colorful', full=True)
    #         highlighted_code = highlight(code, lexer, formatter)
    #         return highlighted_code
    #     else:
    #         return None