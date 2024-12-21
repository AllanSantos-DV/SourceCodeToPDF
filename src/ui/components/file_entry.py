import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .base_entry import TreeEntryBase


class FileEntry(TreeEntryBase):
    def __init__(self, parent_frame, file_path, file_name, is_selected, file_vars):
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

        # Frame para o conteúdo do arquivo
        content_frame = ttk.Frame(self.item_frame)
        content_frame.pack(fill=X, side=LEFT, padx=(self.indent + 30, 0))  # Adiciona indentação extra para arquivos

        # Cria o checkbox do arquivo
        checkbox = ttk.Checkbutton(
            content_frame,
            text=file_name,
            variable=self.var,
            bootstyle="round-toggle"
        )
        checkbox.pack(side=LEFT)