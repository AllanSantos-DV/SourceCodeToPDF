from src.pdf.generator import PDFGenerator


def test_generate_simple_pdf(tmp_path):
    # Configuração inicial
    pdf_generator = PDFGenerator()
    source_file = tmp_path / "example.py"
    source_file.write_text("print('Hello')")
    output_pdf = tmp_path / "output.pdf"

    # Executar método
    pdf_generator.generate_simple_pdf([str(source_file)], str(tmp_path), str(output_pdf))

    # Verificar resultados
    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0

def test_generate_indented_pdf(tmp_path):
    # Configuração inicial
    pdf_generator = PDFGenerator()
    source_file = tmp_path / "example.py"
    source_file.write_text("print('Hello')")
    output_pdf = tmp_path / "output_indented.pdf"

    # Executar método
    pdf_generator.generate_indented_pdf([str(source_file)], str(tmp_path), str(output_pdf))

    # Verificar resultados
    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0
