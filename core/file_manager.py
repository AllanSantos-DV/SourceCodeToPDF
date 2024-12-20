# core/file_manager.py
import os
from config.settings import SUPPORTED_EXTENSIONS, IGNORED_FOLDERS

class FileManager:
    @staticmethod
    def list_files_in_directory_with_ignored(directory):
        """Retorna todos os arquivos e pastas no diretório, incluindo ignorados."""
        files_with_states = []  # Lista de (path, selecionado_por_padrão)

        for root, dirs, files in os.walk(directory):
            ignored_dirs = [d for d in dirs if d in IGNORED_FOLDERS]
            dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]

            # Adicionar pastas ignoradas
            for ignored_dir in ignored_dirs:
                files_with_states.append((os.path.join(root, ignored_dir), False))

            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith(SUPPORTED_EXTENSIONS):
                    files_with_states.append((full_path, True))
                else:
                    files_with_states.append((full_path, False))

        return files_with_states
