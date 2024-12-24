import os
import sys
import unittest
from pathlib import Path

# Adiciona o diretório src ao PYTHONPATH
src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from config.settings import SUPPORTED_EXTENSIONS, IGNORED_FOLDERS, PAGE_SIZE, DEFAULT_FONT_SIZE


class TestConfig(unittest.TestCase):
    """Testes para as configurações do projeto"""

    def setUp(self):
        """Configuração inicial para os testes"""
        self.test_dir = Path(__file__).parent / 'test_files'
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        """Limpeza após os testes"""
        if self.test_dir.exists():
            for file in self.test_dir.glob('*'):
                file.unlink()
            self.test_dir.rmdir()

    def test_supported_extensions(self):
        """Testa se as extensões suportadas estão corretamente definidas"""
        expected_extensions = (
            '.java', '.py', '.js', '.html', '.css',
            '.xml', 'fxml', '.json', '.txt', 'yaml',
            'yml', 'sh', '.bat', '.cmd'
        )

        # Testa se todas as extensões esperadas estão presentes
        for ext in expected_extensions:
            with self.subTest(extension=ext):
                self.assertIn(ext, SUPPORTED_EXTENSIONS)

        # Testa se o número total de extensões está correto
        self.assertEqual(len(SUPPORTED_EXTENSIONS), len(expected_extensions))

    def test_ignored_folders(self):
        """Testa se as pastas ignoradas estão corretamente definidas"""
        expected_folders = (
            'properties', 'target', 'META-INF', '.venv',
            '.config', '.pytest_cache', '__pycache__',
            '.mvn', '.git', '.idea', '.vscode', 'node_modules'
        )

        # Testa se todas as pastas esperadas estão presentes
        for folder in expected_folders:
            with self.subTest(folder=folder):
                self.assertIn(folder, IGNORED_FOLDERS)

        # Testa se o número total de pastas está correto
        self.assertEqual(len(IGNORED_FOLDERS), len(expected_folders))

    def test_page_size(self):
        """Testa se o tamanho da página está definido corretamente"""
        from reportlab.lib.pagesizes import letter
        self.assertEqual(PAGE_SIZE, letter)

    def test_default_font_size(self):
        """Testa se o tamanho padrão da fonte está definido corretamente"""
        self.assertEqual(DEFAULT_FONT_SIZE, 8)
        self.assertIsInstance(DEFAULT_FONT_SIZE, int)

    def test_create_file_with_supported_extension(self):
        """Testa a criação de arquivos com extensões suportadas"""
        for ext in SUPPORTED_EXTENSIONS:
            if not ext.startswith('.'):
                ext = '.' + ext

            test_file = self.test_dir / f'test_file{ext}'
            test_file.touch()

            with self.subTest(extension=ext):
                self.assertTrue(test_file.exists())

    def test_create_ignored_folders(self):
        """Testa a criação de pastas que devem ser ignoradas"""
        for folder in IGNORED_FOLDERS:
            test_folder = self.test_dir / folder
            test_folder.mkdir(exist_ok=True)

            with self.subTest(folder=folder):
                self.assertTrue(test_folder.exists())
                test_folder.rmdir()


if __name__ == '__main__':
    unittest.main(verbosity=2)