import os

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class FileEntry:
    """
    Classe que representa um arquivo na árvore de seleção.
    """

    def __init__(
            self,
            parent_frame,
            file_path,
            file_name,
            is_selected,
            file_vars,
            folder_contents
    ):
        """
        Inicializa uma entrada de arquivo.

        Args:
            parent_frame: Frame pai onde este componente será inserido
            file_path: Caminho completo do arquivo
            file_name: Nome do arquivo para exibição
            is_selected: Estado inicial do checkbox
            file_vars: Dicionário de variáveis de controle dos checkboxes
            folder_contents: Estrutura de dados com o conteúdo das pastas
        """
        self.path = file_path
        self.file_vars = file_vars
        self.folder_contents = folder_contents

        # Frame para o item
        self.item_frame = ttk.Frame(parent_frame)
        self.item_frame.pack(fill=X)

        # Variável de controle para o checkbox
        self.var = ttk.IntVar(value=is_selected)
        self.file_vars[file_path] = self.var

        # Calcula a indentação baseada na profundidade do caminho
        self.indent = self._calculate_indent(file_path)

        self._create_file_entry(file_name)

    def _calculate_indent(self, path):
        """
        Calcula a indentação baseada na profundidade do caminho.
        """
        base_indent = 10
        depth = len(os.path.dirname(path).split(os.sep))
        return base_indent * (depth + 1)

    def _create_file_entry(self, file_name):
        """
        Cria os elementos visuais da entrada do arquivo.
        """
        # Frame para o conteúdo
        content_frame = ttk.Frame(self.item_frame)
        content_frame.pack(fill=X, side=LEFT, padx=(self.indent + 40, 0))

        # Checkbox com nome do arquivo
        checkbox = ttk.Checkbutton(
            content_frame,
            text=file_name,
            variable=self.var,
            bootstyle="round-toggle",
            command=self._on_toggle
        )
        checkbox.pack(side=LEFT)

    def _on_toggle(self):
        """
        Handler para alteração do estado do checkbox.
        """
        is_selected = bool(self.var.get())

        # Atualiza o estado em folder_contents
        if os.path.isfile(self.path):
            # Atualiza arquivo
            for folder, data in self.folder_contents.items():
                for i, (file_path, file_name, _) in enumerate(data['files']):
                    if file_path == self.path:
                        data['files'][i] = (file_path, file_name, is_selected)
                        break