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

    # Método preservado como comentário para referência futura e possíveis melhorias
    #
    # @staticmethod
    # def get_file_extensions(directory):
    #     """
    #     Obtém todas as extensões únicas de arquivos no diretório.
    #     Útil para futura funcionalidade de filtro por extensão.
    #     """
    #     extensions = set()
    #     for root, _, files in os.walk(directory):
    #         for file in files:
    #             _, ext = os.path.splitext(file)
    #             if ext:
    #                 extensions.add(ext.lower())
    #     return sorted(extensions)

    # Método preservado para futura implementação de análise de arquivos
    #
    # @staticmethod
    # def analyze_file_content(file_path):
    #     """
    #     Analisa o conteúdo de um arquivo para determinar tipo e estrutura.
    #     Útil para futura funcionalidade de preview e highlight.
    #     """
    #     try:
    #         with open(file_path, 'r', encoding='utf-8') as f:
    #             content = f.read(1024)  # Lê apenas início para análise
    #             return {
    #                 'size': os.path.getsize(file_path),
    #                 'preview': content[:100],
    #                 'binary': not all(ord(c) < 128 for c in content)
    #             }
    #     except Exception as e:
    #         return {'error': str(e)}