import os
from tkinter import IntVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class TreeEntryBase:
    def __init__(self, parent_frame, path, is_selected, file_vars):
        """
        Inicializa uma entrada na árvore.
        Args:
            parent_frame: Frame pai onde este componente será inserido
            path: Caminho do item (arquivo ou pasta)
            is_selected: Estado inicial de seleção
            file_vars: Dicionário de variáveis de controle dos checkboxes
        """
        self.path = path
        self.file_vars = file_vars

        # Frame para o item
        self.item_frame = ttk.Frame(parent_frame)
        self.item_frame.pack(fill=X)

        # Variável de controle para o checkbox
        self.var = IntVar(value=is_selected)
        file_vars[path] = self.var

        # Calcula a indentação baseada na profundidade do caminho
        self.indent = self._calculate_indent(path)

    def _calculate_indent(self, path):
        """
        Calcula a indentação baseada na profundidade do caminho
        Args:
            path: Caminho do item para calcular a indentação
        Returns:
            int: Valor da indentação em pixels
        """
        base_indent = 20
        depth = len(os.path.dirname(path).split(os.sep))
        return base_indent * (depth + 1)

    def create_checkbox(self, text, command=None):
        """
        Cria um checkbox com texto e comando opcional.
        Args:
            text: Texto a ser exibido no checkbox
            command: Função a ser chamada quando o checkbox for alterado
        """
        # Criamos um frame para manter os elementos alinhados
        content_frame = ttk.Frame(self.item_frame)
        content_frame.pack(fill=X, side=LEFT, padx=(0, 0))

        checkbox = ttk.Checkbutton(
            content_frame,
            text=text,
            variable=self.var,
            bootstyle="round-toggle",
            command=command
        )
        checkbox.pack(side=LEFT)