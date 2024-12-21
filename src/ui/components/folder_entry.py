import os

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.config.settings import IGNORED_FOLDERS
from .base_entry import TreeEntryBase


class FolderEntry(TreeEntryBase):
    def __init__(self, parent_frame, folder_path, project_path, file_vars, folder_frames,
                 folder_contents, create_file_entry):
        self.folder_path = folder_path
        self.project_path = project_path
        self.folder_frames = folder_frames
        self.folder_contents = folder_contents
        self.create_file_entry = create_file_entry

        is_ignored = any(ignore in folder_path.split(os.sep)
                         for ignore in IGNORED_FOLDERS)

        # Container principal para a pasta e seu conteúdo
        self.container_frame = ttk.Frame(parent_frame)
        self.container_frame.pack(fill=X)

        # Frame para a linha da pasta (botão + checkbox)
        self.item_frame = ttk.Frame(self.container_frame)
        self.item_frame.pack(fill=X)

        # Chama construtor da classe base
        super().__init__(
            self.item_frame,
            os.path.join(project_path, folder_path),
            0 if is_ignored else 1,
            file_vars
        )

        # Frame para o conteúdo
        self.content_frame = ttk.Frame(self.container_frame)
        self.folder_frames[folder_path] = self.content_frame

        self._create_folder_controls()

    def _create_folder_controls(self):
        """Cria os controles visuais da pasta"""
        controls_frame = ttk.Frame(self.item_frame)
        controls_frame.pack(fill=X, side=LEFT, padx=(self.indent, 0))

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
        self.create_checkbox(
            os.path.basename(self.folder_path),
            command=self._toggle_folder_selection
        )

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
        is_selected = self.var.get()  # Estado do checkbox da pasta atual
        folder_data = self.folder_contents[self.folder_path]

        # Atualizar arquivos na pasta atual
        for file_path, _, _ in folder_data['files']:
            if file_path in self.file_vars:  # Atualiza se o arquivo já foi renderizado
                self.file_vars[file_path].set(is_selected)
            else:
                # Atualiza diretamente no estado armazenado
                folder_data['files'] = [
                    (fp, fn, is_selected) if fp == file_path else (fp, fn, sel)
                    for fp, fn, sel in folder_data['files']
                ]

        # Atualizar subpastas recursivamente
        for subfolder in folder_data['subfolders']:
            full_path = os.path.join(self.project_path, subfolder)
            if full_path in self.file_vars:
                self.file_vars[full_path].set(is_selected)  # Atualiza se renderizado
            self._toggle_subfolder_selection(subfolder, is_selected)  # Recursivo

    def _toggle_subfolder_selection(self, subfolder, is_selected):
        """Alterna a seleção de uma subpasta e seu conteúdo recursivamente"""
        folder_data = self.folder_contents[subfolder]

        # Atualizar arquivos na subpasta
        for file_path, _, _ in folder_data['files']:
            if file_path in self.file_vars:
                self.file_vars[file_path].set(is_selected)
            else:
                # Atualiza diretamente no estado armazenado
                folder_data['files'] = [
                    (fp, fn, is_selected) if fp == file_path else (fp, fn, sel)
                    for fp, fn, sel in folder_data['files']
                ]

        # Atualizar subpastas aninhadas
        for sub in folder_data['subfolders']:
            full_path = os.path.join(self.project_path, sub)
            if full_path in self.file_vars:
                self.file_vars[full_path].set(is_selected)
            self._toggle_subfolder_selection(sub, is_selected)
