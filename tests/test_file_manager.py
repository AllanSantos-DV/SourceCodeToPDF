from core.file_handler import FileHandler
from src.core.file_manager import FileManager


def test_list_files_in_directory_with_ignored(tmp_path):
    # Criar estrutura de teste
    ignored_folder = tmp_path / "__pycache__"
    ignored_folder.mkdir()
    valid_file = tmp_path / "script.py"
    valid_file.write_text("print('Hello')")
    invalid_file = tmp_path / "readme.md"
    invalid_file.write_text("# Readme")

    # Mock FileHandler
    FileHandler.is_supported_file = lambda x: x.endswith(".py")
    FileHandler.is_ignored_folder = lambda x: x == "__pycache__"

    # Executar método
    all_files = FileManager.list_files_in_directory_with_ignored(str(tmp_path))

    # Verificar resultados
    assert len(all_files) == 3
    assert any("script.py" in file[0] and file[1] for file in all_files)
    assert any("__pycache__" in file[0] and not file[1] for file in all_files)
    assert any("readme.md" in file[0] and not file[1] for file in all_files)
