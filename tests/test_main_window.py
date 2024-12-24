from tkinter import Tk
from unittest.mock import MagicMock, patch
from src.ui.main_window import MainWindow

@patch("src.ui.main_window.filedialog.askdirectory", return_value="/fake/path")
def test_select_folder(mock_askdirectory):
    root = Tk()
    main_window = MainWindow(root)
    main_window.select_folder()

    assert main_window.project_path == "/fake/path"
    assert "Pasta selecionada:" in main_window.folder_label.cget("text")
    root.destroy()

@patch("src.ui.main_window.filedialog.asksaveasfilename", return_value="/fake/output.pdf")
@patch("src.ui.main_window.PDFGenerator.generate_simple_pdf")
def test_generate_pdf(mock_generate_simple_pdf, mock_asksaveasfilename):
    root = Tk()
    main_window = MainWindow(root)
    main_window.selected_files = ["/fake/path/file.py"]
    main_window.project_path = "/fake/path"
    main_window._generate_pdf_with_format("texto_simples")

    mock_generate_simple_pdf.assert_called_once()
    root.destroy()
