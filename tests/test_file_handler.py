from src.core.file_handler import FileHandler

def test_is_supported_file():
    assert FileHandler.is_supported_file("example.py") is True
    assert FileHandler.is_supported_file("example.txt") is True
    assert FileHandler.is_supported_file("example.unsupported") is False

def test_is_ignored_folder():
    assert FileHandler.is_ignored_folder("__pycache__") is True
    assert FileHandler.is_ignored_folder("node_modules") is True
    assert FileHandler.is_ignored_folder("my_folder") is False

def test_process_directory(tmp_path):
    # Criar estrutura de teste
    ignored_folder = tmp_path / "__pycache__"
    ignored_folder.mkdir()
    valid_file = tmp_path / "script.py"
    valid_file.write_text("print('Hello, world!')")
    invalid_file = tmp_path / "readme.md"
    invalid_file.write_text("# Project Readme")

    # Processar diretório
    regular_files, ignored_items = FileHandler.process_directory(str(tmp_path))

    # Verificar resultados
    assert len(regular_files) == 1
    assert regular_files[0][0].endswith("script.py")
    assert regular_files[0][1] is True

    assert len(ignored_items) == 2
    assert any("__pycache__" in item[0] for item in ignored_items)
    assert any("readme.md" in item[0] for item in ignored_items)
