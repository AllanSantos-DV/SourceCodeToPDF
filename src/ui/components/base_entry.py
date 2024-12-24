import os
from tkinter import messagebox
from typing import Optional, Callable

import ttkbootstrap as ttk

from src.core.selection_manager import logger, FileSelectionManager, SelectionState


def _handle_error(message: str) -> None:
    """
    Trata erros de forma centralizada.

    Args:
        message: Mensagem de erro
    """
    logger.error(message)
    messagebox.showerror("Erro", message)


class TreeEntryBase:
    """
    Classe base para entradas na árvore de arquivos.
    Fornece funcionalidades comuns para FileEntry e FolderEntry.
    """

    def __init__(
            self,
            parent_frame: ttk.Frame,
            path: str,
            selection_manager: 'FileSelectionManager',
            initial_state: bool = False,
            indent_level: int = 0
    ):
        """
        Inicializa uma entrada base na árvore.

        Args:
            parent_frame: Frame pai onde este componente será inserido
            path: Caminho do item (arquivo ou pasta)
            selection_manager: Gerenciador central de seleção
            initial_state: Estado inicial de seleção
            indent_level: Nível de indentação na árvore
        """
        self._custom_command = None
        self.path = path
        self.selection_manager = selection_manager
        self.indent_level = indent_level

        # Criação do frame principal
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(fill="x", expand=True)

        # Frame para indentação
        self.indent_frame = ttk.Frame(self.frame, width=self.indent_level * 20)
        self.indent_frame.pack(side="left")

        # Frame para o conteúdo
        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(side="left", fill="x", expand=True)

        # Variável de controle para o checkbox
        self.var = ttk.IntVar(value=int(initial_state))

        # Registro no gerenciador de seleção
        self._register_with_manager()

        # Configuração de eventos
        self._setup_events()

    def _register_with_manager(self) -> None:
        """Registra este item no gerenciador de seleção"""
        parent_folder = os.path.dirname(self.path) if self.path else None
        self.selection_manager.register_item(self.path, parent_folder)

    def _setup_events(self) -> None:
        """Configura os eventos e bindings"""
        self.frame.bind("<Enter>", self._on_mouse_enter)
        self.frame.bind("<Leave>", self._on_mouse_leave)

    def create_checkbox(
            self,
            text: str,
            command: Optional[Callable] = None,
            tooltip: Optional[str] = None
    ) -> ttk.Checkbutton:
        """
        Cria um checkbox com texto e comando opcional.

        Args:
            text: Texto a ser exibido no checkbox
            command: Função callback opcional
            tooltip: Texto de tooltip opcional

        Returns:
            Instância do checkbox criado
        """
        # Frame para o checkbox com padding
        checkbox_frame = ttk.Frame(self.content_frame)
        checkbox_frame.pack(side="left", padx=(5, 0))

        # Criação do checkbox
        checkbox = ttk.CHECKBUTTON(
            checkbox_frame,
            text=text,
            variable=self.var,
            command=self._on_checkbox_toggle,
            bootstyle="round-toggle"
        )
        checkbox.pack(side="left")

        # Configura o comando personalizado
        self._custom_command = command

        # Adiciona tooltip se fornecido
        if tooltip:
            ttk.TOOLBUTTON(checkbox, text=tooltip)

        return checkbox

    def _on_checkbox_toggle(self) -> None:
        """Callback interno para alteração do checkbox"""
        try:
            is_selected = bool(self.var.get())
            self.selection_manager.update_selection(self.path, is_selected)

            # Executa comando personalizado se existir
            if self._custom_command:
                self._custom_command()

        except Exception as e:
            _handle_error(f"Erro ao atualizar seleção: {str(e)}")

    def update_state(self, state: 'SelectionState') -> None:
        """
        Atualiza o estado visual do componente.

        Args:
            state: Novo estado de seleção
        """
        if self.var.get() != int(state.is_selected):
            self.var.set(int(state.is_selected))

        # Atualiza estilo baseado no estado
        if state.is_partial:
            self.frame.configure(style="partial.TFrame")
        else:
            self.frame.configure(style="normal.TFrame")

    def _on_mouse_enter(self, event) -> None:
        """Handler para evento de mouse enter"""
        event.widget.configure(style="hover.TFrame")
        self.frame.configure(style="hover.TFrame")

    def _on_mouse_leave(self, event) -> None:
        """Handler para evento de mouse leave"""
        event.widget.configure(style="normal.TFrame")
        self.frame.configure(style="normal.TFrame")

