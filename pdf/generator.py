import pdfkit
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph

from config.settings import PAGE_SIZE, DEFAULT_FONT_SIZE

class PDFGenerator:
    def __init__(self, font_size=DEFAULT_FONT_SIZE, page_size=PAGE_SIZE):
        self.font_size = font_size
        self.page_size = page_size
        self.styles = getSampleStyleSheet()
        self.custom_style = ParagraphStyle(
            'CodeStyle',
            parent=self.styles['Normal'],
            fontName='Courier',
            fontSize=self.font_size,
            textColor='black',
            alignment=TA_LEFT
        )

    def generate_pdf(self, files, output_path, progress_callback=None):
        pdf = SimpleDocTemplate(output_path, pagesize=self.page_size)
        content = []
        total_files = len(files)
        for i, file in enumerate(files, 1):
            content.append(Paragraph(f"Arquivo: {file}",
                                     self.styles['Heading3']))
            content.append(Spacer(1, 12))
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                for line in lines:
                    content.append(Paragraph(line, self.custom_style))
                content.append(Spacer(1, 12))
            except Exception as e:
                content.append(Paragraph(f"Erro ao processar {file}: {e}",self.styles['Normal']))

            if progress_callback:
                progress_callback(i, total_files)

        pdf.build(content)

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