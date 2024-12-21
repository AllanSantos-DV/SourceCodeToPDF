import os
from tkinter import Toplevel
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Atualizando os imports para a nova estrutura
from src.ui.components.folder_entry import FolderEntry
from src.ui.components.file_entry import FileEntry


class FileSelectionDialog:
    """
    Diálogo para seleção de arquivos em uma estrutura de árvore.
    Permite navegação e seleção de arquivos e pastas.
    """

    def __init__(self, parent, project_path):
        """
        Inicializa o diálogo de seleção de arquivos.

        Args:
            parent: Janela pai
            project_path: Caminho base do projeto
        """
        self.window = Toplevel(parent)
        self.window.title("Seleção de Arquivos")
        self.window.geometry("600x600")

        self.project_path = project_path
        self.file_vars = {}
        self.folder_frames = {}
        self.folder_contents = {}

        self._create_ui()

    def _create_ui(self):
        """Cria a interface do diálogo com scroll"""
        # Frame principal
        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # Canvas e Scrollbar
        self.canvas = ttk.Canvas(main_frame)
        self.scrollbar = ttk.Scrollbar(
            main_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        # Frame scrollável
        self.scrollable_frame = ttk.Frame(self.canvas)
        self._configure_scrolling()

        # Empacotamento dos componentes
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Botão de confirmação
        self._add_confirm_button()

    def _configure_scrolling(self):
        """Configura o comportamento de scroll"""
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Configuração do mousewheel
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )
        self.window.bind(
            "<Destroy>",
            lambda e: self.canvas.unbind_all("<MouseWheel>")
        )

    def _add_confirm_button(self):
        """Adiciona o botão de confirmação"""
        confirm_btn = ttk.Button(
            self.window,
            text="Confirmar Seleção",
            command=self._confirm_selection,
            bootstyle=SUCCESS
        )
        confirm_btn.pack(pady=10)

    def populate_tree(self, folder_contents):
        """
        Popula a árvore com os arquivos e pastas.

        Args:
            folder_contents: Estrutura de dados com o conteúdo das pastas
        """
        self.folder_contents = folder_contents

        # Arquivos na raiz
        root_files = self.folder_contents.get('', {'files': []})['files']
        for file_path, file_name, is_selected in root_files:
            self._create_file_entry(
                file_path,
                file_name,
                is_selected,
                self.scrollable_frame
            )

        # Pastas do primeiro nível
        root_folders = {
            folder for folder, data in self.folder_contents.items()
            if data['parent'] == '' and folder != ''
        }

        for folder in sorted(root_folders):
            self._create_folder_entry(folder)

    def _create_folder_entry(self, folder):
        """Cria uma entrada de pasta"""
        return FolderEntry(
            self.scrollable_frame,
            folder,
            self.project_path,
            self.file_vars,
            self.folder_frames,
            self.folder_contents,
            self._create_file_entry
        )

    def _create_file_entry(self, file_path, file_name, is_selected, parent_frame):
        """Cria uma entrada de arquivo"""
        return FileEntry(
            parent_frame,
            file_path,
            file_name,
            is_selected,
            self.file_vars
        )

    def _confirm_selection(self):
        """Confirma a seleção e fecha o diálogo"""
        selected_files = [
            file for file, var in self.file_vars.items()
            if var.get() == 1 and os.path.isfile(file)
        ]
        self.window.selected_files = selected_files
        self.window.destroy()

    def get_selected_files(self):
        """Retorna os arquivos selecionados após o fechamento do diálogo"""
        self.window.wait_window()
        return getattr(self.window, 'selected_files', [])