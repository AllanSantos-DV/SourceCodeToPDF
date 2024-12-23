import os

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.config.settings import IGNORED_FOLDERS


class FolderEntry:
    """
    Classe que representa uma pasta na árvore de seleção.
    """
    def __init__(self, parent_frame, folder_path, project_path, file_vars, folder_frames,
                folder_contents, create_file_entry):
        self.folder_path = folder_path
        self.project_path = project_path
        self.folder_frames = folder_frames
        self.folder_contents = folder_contents
        self.create_file_entry = create_file_entry
        self.file_vars = file_vars

        # Container principal para a pasta e seu conteúdo
        self.container_frame = ttk.Frame(parent_frame)
        self.container_frame.pack(fill=X)

        # Frame para a linha da pasta (botão + checkbox)
        self.item_frame = ttk.Frame(self.container_frame)
        self.item_frame.pack(fill=X)

        is_ignored = any(ignore in folder_path.split(os.sep)
                        for ignore in IGNORED_FOLDERS)

        # Variável de controle para o checkbox
        self.var = ttk.IntVar(value=0 if is_ignored else 1)
        self.file_vars[os.path.join(project_path, folder_path)] = self.var

        # Frame para o conteúdo
        self.content_frame = ttk.Frame(self.container_frame)
        self.folder_frames[folder_path] = self.content_frame

        self._create_folder_controls()

    def _create_folder_controls(self):
        """Cria os controles visuais da pasta"""
        controls_frame = ttk.Frame(self.item_frame)
        controls_frame.pack(fill=X, side=LEFT, padx=(self._calculate_indent(), 0))

        # Botão de expansão
        self.toggle_btn = ttk.Button(
            controls_frame,
            text="■",
            width=2,
            bootstyle="link",
            command=self._toggle_folder
        )
        self.toggle_btn.pack(side=LEFT, padx=(0, 5))

        # Checkbox da pasta
        self.create_checkbox(os.path.basename(self.folder_path))

    def _calculate_indent(self):
        """Calcula a indentação baseada na profundidade do caminho"""
        base_indent = 15
        depth = len(self.folder_path.split(os.sep))
        return base_indent * depth

    def create_checkbox(self, text):
        """Cria o checkbox com texto"""
        checkbox = ttk.Checkbutton(
            self.item_frame,
            text=text,
            variable=self.var,
            bootstyle="round-toggle",
            command=self._toggle_folder_selection
        )
        checkbox.pack(side=LEFT)

    def _toggle_folder(self):
        """Alterna a exibição do conteúdo da pasta"""
        if self.content_frame.winfo_manager():
            self.content_frame.pack_forget()
            self.toggle_btn.configure(text="■")
        else:
            self.content_frame.pack(fill=X, expand=True)
            self.toggle_btn.configure(text="▼")
            self._create_content_if_empty()

    def _create_content_if_empty(self):
        """Cria o conteúdo da pasta se ainda não existir"""
        if not self.content_frame.winfo_children():
            folder_data = self.folder_contents[self.folder_path]

            is_ignored = any(ignore in self.folder_path.split(os.sep)
                        for ignore in IGNORED_FOLDERS)

            # Adicionar arquivos
            for file_path, file_name, is_selected in folder_data['files']:
                self.create_file_entry(
                    file_path,
                    file_name,
                    0 if is_ignored else is_selected,
                    self.content_frame
                )

            # Adicionar subpastas
            for subfolder in sorted(folder_data['subfolders']):
                self._create_subfolder(subfolder)

    def _create_subfolder(self, subfolder):
        """Cria uma subpasta dentro desta pasta"""
        return FolderEntry(
            self.content_frame,
            subfolder,
            self.project_path,
            self.file_vars,
            self.folder_frames,
            self.folder_contents,
            self.create_file_entry
        )

    def _toggle_folder_selection(self):
        """Alterna a seleção da pasta e seu conteúdo"""
        is_selected = self.var.get()

        folder_data = self.folder_contents[self.folder_path]
        # Atualizar arquivos na pasta atual
        for file_path, _, _ in folder_data['files']:
            if file_path in self.file_vars:  # Atualiza se o arquivo já foi renderizado
                self.file_vars[file_path].set(is_selected)
            else:
                # Atualiza diretamente no estado armazenado
                for i, (f_path, f_name, _) in enumerate(folder_data['files']):
                    if f_path == file_path:
                        folder_data['files'][i] = (f_path, f_name, bool(is_selected))

        # Atualizar subpastas recursivamente
        for subfolder in folder_data['subfolders']:
            subfolder_path = os.path.join(self.project_path, subfolder)
            if subfolder_path in self.file_vars:
                self.file_vars[subfolder_path].set(is_selected)
            self._toggle_subfolder_selection(subfolder, bool(is_selected))

    def _toggle_subfolder_selection(self, subfolder, is_selected):
        """Alterna a seleção de uma subpasta e seu conteúdo recursivamente"""
        folder_data = self.folder_contents[subfolder]

        # Atualizar arquivos na subpasta
        for file_path, _, _ in folder_data['files']:
            if file_path in self.file_vars:
                self.file_vars[file_path].set(is_selected)
            else:
                for i, (f_path, f_name, _) in enumerate(folder_data['files']):
                    if f_path == file_path:
                        folder_data['files'][i] = (f_path, f_name, is_selected)

        # Atualizar subpastas aninhadas
        for subfolder_path in folder_data['subfolders']:
            full_path = os.path.join(self.project_path, subfolder_path)
            if full_path in self.file_vars:
                self.file_vars[full_path].set(is_selected)
            self._toggle_subfolder_selection(subfolder_path, is_selected)