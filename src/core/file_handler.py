import os
from src.config.settings import SUPPORTED_EXTENSIONS, IGNORED_FOLDERS


class FileHandler:
    """
    Classe responsável por operações de manipulação de arquivos.
    Separa a lógica de manipulação de arquivos do gerenciamento geral.
    """

    @staticmethod
    def is_supported_file(filename):
        """Verifica se o arquivo é suportado baseado na extensão"""
        return filename.endswith(SUPPORTED_EXTENSIONS)

    @staticmethod
    def is_ignored_folder(folder_name):
        """Verifica se a pasta deve ser ignorada"""
        return folder_name in IGNORED_FOLDERS

    @staticmethod
    def process_directory(directory):
        """
        Processa um diretório separando arquivos e pastas ignorados.

        Args:
            directory: Caminho do diretório a ser processado

        Returns:
            tuple: (arquivos regulares, arquivos ignorados)
        """
        regular_files = []
        ignored_items = []

        for root, dirs, files in os.walk(directory):
            # Processar pastas ignoradas
            for d in dirs[:]:  # Copia da lista para permitir modificação
                if FileHandler.is_ignored_folder(d):
                    full_path = os.path.join(root, d)
                    ignored_items.append((full_path, False))
                    dirs.remove(d)

            # Processar arquivos
            for file in files:
                full_path = os.path.join(root, file)
                if FileHandler.is_supported_file(file):
                    regular_files.append((full_path, True))
                else:
                    ignored_items.append((full_path, False))

        return regular_files, ignored_items

    @staticmethod
    def get_relative_path(file_path, base_path):
        """
        Obtém o caminho relativo de um arquivo em relação a um diretório base.

        Args:
            file_path: Caminho completo do arquivo
            base_path: Diretório base para calcular o caminho relativo

        Returns:
            str: Caminho relativo do arquivo
        """
        try:
            return os.path.relpath(file_path, base_path)
        except ValueError:
            return file_path  # Retorna caminho original em caso de erro