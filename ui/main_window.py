import os
from tkinter import filedialog, messagebox, Toplevel, IntVar

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from config.settings import IGNORED_FOLDERS
from core.file_manager import FileManager
from pdf.generator import PDFGenerator


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Código-Fonte para PDF")
        self.project_path = ""
        self.selected_files = []
        self.create_widgets()

    def create_widgets(self):
        # Título
        title = ttk.Label(
            self.root,
            text="Conversor de Código-Fonte para PDF",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=10)

        # Botão para selecionar pasta
        select_btn = ttk.Button(
            self.root,
            text="Selecionar Pasta",
            command=self.select_folder,
            bootstyle=PRIMARY
        )
        select_btn.pack(pady=10)

        # Label para exibir o caminho da pasta
        self.folder_label = ttk.Label(
            self.root,
            text="Nenhuma pasta selecionada.",
            font=("Helvetica", 10),
            wraplength=300,
            justify="center"
        )
        self.folder_label.pack(pady=10)

        # Barra de progresso
        self.progress = ttk.Progressbar(
            self.root,
            mode='determinate',
            bootstyle=SUCCESS
        )
        self.progress.pack(pady=10)

        # Botão para gerar PDF
        generate_btn = ttk.Button(
            self.root,
            text="Gerar PDF",
            command=self.generate_pdf,
            bootstyle=SUCCESS
        )
        generate_btn.pack(pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Selecione a pasta do projeto")

        if not folder:
            messagebox.showwarning("Aviso", "Nenhuma pasta selecionada")
            return

        self.project_path = folder
        self.folder_label.config(text=f"Pasta selecionada:\n{folder}")

        files = FileManager.list_files_in_directory_with_ignored(folder)

        if not files:
            messagebox.showinfo("Aviso", "Nenhum arquivo encontrado na pasta selecionada.")
            return

        self.show_file_selection_window(files)

    def show_file_selection_window(self, files_with_states):
        selection_window = Toplevel(self.root)
        selection_window.title("Seleção de Arquivos")
        selection_window.geometry("600x600")

        # Frame principal
        main_frame = ttk.Frame(selection_window)
        main_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # Canvas e Scrollbar
        canvas = ttk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

        # Frame scrollável
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Configuração do canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Empacotamento do canvas e scrollbar
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Configuração do mousewheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        selection_window.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Estrutura de dados para armazenar os controles
        self.file_vars = {}  # Checkboxes das pastas e arquivos
        self.folder_frames = {}  # Frames de conteúdo das pastas
        self.folder_contents = {}  # Subpastas e arquivos de cada pasta

        # Organizar arquivos em estrutura de pastas
        self.organize_files(files_with_states)

        # Criar interface hierárquica
        self.create_folder_structure()

        # Botão de confirmação
        confirm_btn = ttk.Button(
            selection_window,
            text="Confirmar Seleção",
            command=lambda: self.confirm_selection(selection_window),
            bootstyle=SUCCESS
        )
        confirm_btn.pack(pady=10)

    def organize_files(self, files_with_states):
        self.folder_contents = {}

        for file_path, is_selected in files_with_states:
            rel_path = os.path.relpath(file_path, self.project_path)
            parts = rel_path.split(os.sep)

            # Processar cada nível do caminho
            current_path = ""
            for i, part in enumerate(parts[:-1]):
                parent_path = current_path
                current_path = os.path.join(current_path, part) if current_path else part

                # Criar entrada para a pasta se não existir
                if current_path not in self.folder_contents:
                    self.folder_contents[current_path] = {
                        'parent': parent_path,
                        'files': [],
                        'subfolders': set()
                    }

                # Adicionar à lista de subpastas do pai
                if parent_path in self.folder_contents:
                    self.folder_contents[parent_path]['subfolders'].add(current_path)

            # Adicionar o arquivo à última pasta do caminho
            if os.path.isfile(file_path):
                folder = os.path.dirname(rel_path)
                if folder not in self.folder_contents:
                    self.folder_contents[folder] = {
                        'parent': os.path.dirname(folder),
                        'files': [],
                        'subfolders': set()
                    }
                self.folder_contents[folder]['files'].append((file_path, parts[-1], is_selected))

    def create_folder_structure(self):
        # Primeiro, criar entradas para arquivos na raiz
        root_files = self.folder_contents.get('', {'files': []})['files']
        for file_path, file_name, is_selected in root_files:
            self.create_file_entry(file_path, file_name, is_selected, self.scrollable_frame)

        # Depois, processar as pastas do primeiro nível
        root_folders = {folder for folder, data in self.folder_contents.items()
                        if data['parent'] == '' and folder != ''}

        for folder in sorted(root_folders):
            self.create_folder_entry(folder)

    def create_folder_entry(self, folder_path, parent_frame=None):
        if parent_frame is None:
            parent_frame = self.scrollable_frame

        # Frame para a pasta
        folder_frame = ttk.Frame(parent_frame)
        folder_frame.pack(fill=X)

        # Frame para o conteúdo (agora criado depois do folder_frame)
        content_frame = ttk.Frame(parent_frame)
        self.folder_frames[folder_path] = content_frame

        # Botão de expansão
        toggle_btn = ttk.Button(
            folder_frame,
            text="►",
            width=2,
            bootstyle="link"
        )
        toggle_btn.pack(side=LEFT, padx=(len(folder_path.split(os.sep)) * 20, 0))

        # Checkbox da pasta
        is_ignored = any(ignore in folder_path.split(os.sep) for ignore in IGNORED_FOLDERS)
        var = IntVar(value=0 if is_ignored else 1)
        self.file_vars[os.path.join(self.project_path, folder_path)] = var

        folder_checkbox = ttk.Checkbutton(
            folder_frame,
            text=os.path.basename(folder_path),
            variable=var,
            bootstyle="round-toggle"
        )
        folder_checkbox.pack(side=LEFT)

        # Configurar botão de expansão
        def toggle_folder():
            if content_frame.winfo_manager():
                content_frame.pack_forget()
                toggle_btn.configure(text="►")
            else:
                # Posicionar content_frame logo após o folder_frame
                folder_frame_info = folder_frame.pack_info()
                content_frame.pack(fill=X, after=folder_frame)
                toggle_btn.configure(text="▼")

                # Criar conteúdo se ainda não existir
                if not content_frame.winfo_children():
                    folder_data = self.folder_contents[folder_path]

                    # Adicionar arquivos
                    for file_path, file_name, is_selected in folder_data['files']:
                        self.create_file_entry(file_path, file_name,
                                               0 if is_ignored else is_selected,
                                               content_frame)

                    # Adicionar subpastas
                    for subfolder in sorted(folder_data['subfolders']):
                        self.create_folder_entry(subfolder, content_frame)

        toggle_btn.configure(command=toggle_folder)
        folder_checkbox.configure(command=lambda: self.toggle_folder_selection(folder_path))

        # Retornar o frame da pasta para referência
        return folder_frame

    def create_file_entry(self, file_path, file_name, is_selected, parent_frame):
        file_frame = ttk.Frame(parent_frame)
        file_frame.pack(fill=X)

        var = IntVar(value=is_selected)
        self.file_vars[file_path] = var

        ttk.Checkbutton(
            file_frame,
            text=file_name,
            variable=var,
            bootstyle="round-toggle"
        ).pack(side=LEFT, padx=(20 + len(os.path.dirname(file_path).split(os.sep)) * 20, 0))

    def toggle_folder_selection(self, folder_path):
        is_selected = self.file_vars[os.path.join(self.project_path, folder_path)].get()
        folder_data = self.folder_contents[folder_path]

        # Atualizar arquivos
        for file_path, _, _ in folder_data['files']:
            if file_path in self.file_vars:
                self.file_vars[file_path].set(is_selected)

        # Atualizar subpastas recursivamente
        for subfolder in folder_data['subfolders']:
            full_subfolder_path = os.path.join(self.project_path, subfolder)
            if full_subfolder_path in self.file_vars:
                self.file_vars[full_subfolder_path].set(is_selected)
                self.toggle_folder_selection(subfolder)

    def confirm_selection(self, selection_window):
        self.selected_files = [file for file, var in self.file_vars.items()
                               if var.get() == 1 and os.path.isfile(file)]
        selection_window.destroy()

    def generate_pdf(self):
        if not self.selected_files:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado para geração do PDF.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not output_path:
            messagebox.showwarning("Aviso", "Destino não selecionado")
            return

        pdf_gen = PDFGenerator()
        pdf_gen.generate_pdf(self.selected_files, output_path, self.update_progress)
        messagebox.showinfo("Sucesso", f"PDF gerado em {output_path}")
        self.progress['value'] = 0
        self.root.update_idletasks()

    def update_progress(self, current, total):
        self.progress['value'] = (current / total) * 100
        self.root.update_idletasks()