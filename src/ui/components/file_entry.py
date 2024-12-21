import os

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from .base_entry import TreeEntryBase


class FileEntry(TreeEntryBase):
    def __init__(self, parent_frame, file_path, file_name, is_selected, file_vars, folder_contents):
        """
        Inicializa uma entrada de arquivo na árvore.
        Args:
            parent_frame: Frame pai onde este componente será inserido
            file_path: Caminho completo do arquivo
            file_name: Nome do arquivo para exibição
            is_selected: Estado inicial do checkbox
            file_vars: Dicionário de variáveis de controle dos checkboxes
        """
        super().__init__(parent_frame, file_path, is_selected, file_vars)

        self.folder_contents = folder_contents
        self.file = file_path
        # Frame para o conteúdo do arquivo
        content_frame = ttk.Frame(self.item_frame)
        content_frame.pack(fill=X, side=LEFT, padx=(self.indent + 30, 0))  # Adiciona indentação extra para arquivos

        # Cria o checkbox do arquivo
        self.create_checkbox(file_name, self._toggle)


    def _toggle(self):
        """Sincroniza o estado do checkbox com folder_contents"""
        is_selected = self.var.get()

        # Atualiza o estado em folder_contents
        if os.path.isfile(self.path):
            # Atualiza arquivo
            for folder, data in self.folder_contents.items():
                for i, (file_path, file_name, selected) in enumerate(data['files']):
                    if file_path == self.path:
                        data['files'][i] = (file_path, file_name, is_selected)
                        break
