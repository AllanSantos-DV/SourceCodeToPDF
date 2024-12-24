from src.core.file_handler import FileHandler


class FileManager:
    """
    Gerenciador principal de arquivos.
    Coordena operações de alto nível relacionadas aos arquivos do projeto.
    """

    @staticmethod
    def list_files_in_directory_with_ignored(directory):
        """
        Retorna todos os arquivos e pastas no diretório, incluindo ignorados.

        Args:
            directory: Diretório base a ser processado

        Returns:
            list: Lista de tuplas (path, selecionado_por_padrão)
        """
        # Obtém arquivos regulares e ignorados
        regular_files, ignored_items = FileHandler.process_directory(directory)

        # Combina as listas mantendo a ordem
        all_files = []

        # Adiciona arquivos ignorados
        all_files.extend(ignored_items)

        # Adiciona arquivos regulares
        all_files.extend(regular_files)

        return all_files