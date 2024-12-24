import os
from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *

from src.core.file_manager import FileManager
from src.pdf.generator import PDFGenerator
from src.ui.dialogs.file_selection import FileSelectionDialog


class MainWindow:
    """
    Janela principal da aplicação de conversão de código para PDF.
    Gerencia a seleção de pasta e geração do PDF.
    """

    def __init__(self, root):
        """
        Inicializa a janela principal.

        Args:
            root: Janela raiz da aplicação
        """
        self.root = root
        self.root.title("Conversor de Código-Fonte para PDF")
        self.project_path = ""
        self.selected_files = []
        self.create_widgets()

    def create_widgets(self):
        """Cria os componentes da interface principal"""
        self._create_title()
        self._create_folder_selection()
        self._create_progress_bar()
        self._create_generate_button()

    def _create_title(self):
        """Cria o título da aplicação"""
        title = ttk.Label(
            self.root,
            text="Conversor de Código-Fonte para PDF",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=10)

    def _create_folder_selection(self):
        """Cria os componentes de seleção de pasta"""
        select_btn = ttk.Button(
            self.root,
            text="Selecionar Pasta",
            command=self.select_folder,
            bootstyle=PRIMARY
        )
        select_btn.pack(pady=10)

        self.folder_label = ttk.Label(
            self.root,
            text="Nenhuma pasta selecionada.",
            font=("Helvetica", 10),
            wraplength=300,
            justify="center"
        )
        self.folder_label.pack(pady=10)

    def _create_progress_bar(self):
        """Cria a barra de progresso"""
        self.progress = ttk.Progressbar(
            self.root,
            mode='determinate',
            bootstyle=SUCCESS
        )
        self.progress.pack(pady=10)

    def _create_generate_button(self):
        """Cria o botão de geração de PDF"""
        generate_btn = ttk.Button(
            self.root,
            text="Gerar PDF",
            command=self.generate_pdf,
            bootstyle=SUCCESS
        )
        generate_btn.pack(pady=10)

    def select_folder(self):
        """Gerencia a seleção de pasta e exibição do diálogo de seleção de arquivos"""
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

        dialog = FileSelectionDialog(self.root, folder)
        dialog.populate_tree(self._organize_files(files))
        self.selected_files = dialog.get_selected_files()

    @staticmethod
    def center_window(dialog, window_width, window_height):
        """Centraliza a janela na tela."""
        dialog.update_idletasks()  # Garante que as dimensões da janela sejam atualizadas
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()

        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        dialog.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    def show_pdf_format_dialog(self):
        """Exibe um diálogo para o usuário selecionar o formato do PDF."""
        dialog = Toplevel(self.root)
        dialog.title("Escolher Formato do PDF")
        dialog.resizable(False, False)
        dialog.grab_set()
        MainWindow.center_window(dialog, 300, 200)

        ttk.Label(dialog, text="Escolha o formato do PDF:", font=("Helvetica", 12)).pack(pady=10)

        def select_format(format_option):
            dialog.destroy()
            self._generate_pdf_with_format(format_option)

        ttk.Button(dialog, text="Texto Simples", command=lambda: select_format("texto_simples"), width=15).pack(pady=5)
        ttk.Button(dialog, text="Texto Indentado", command=lambda: select_format("texto_indentado"), width=15).pack(
            pady=5)

    def _generate_pdf_with_format(self, format_option):
        """Gera o PDF baseado no formato selecionado."""
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

        if format_option == "texto_simples":
            pdf_gen.generate_simple_pdf(self.selected_files, self.project_path, output_path, self.update_progress)
        elif format_option == "texto_indentado":
            pdf_gen.generate_indented_pdf(self.selected_files, self.project_path, output_path, self.update_progress)

        messagebox.showinfo("Sucesso", f"PDF gerado em {output_path}")
        self.progress['value'] = 0
        self.root.update_idletasks()

    def generate_pdf(self):
        """Gerencia a geração do PDF mostrando o diálogo de seleção de formato."""
        self.show_pdf_format_dialog()

    def update_progress(self, current, total):
        """Atualiza a barra de progresso"""
        self.progress['value'] = (current / total) * 100
        self.root.update_idletasks()

    def _organize_files(self, files_with_states):
        """
        Organiza os arquivos em uma estrutura hierárquica.

        Args:
            files_with_states: Lista de tuplas (caminho, estado)

        Returns:
            dict: Estrutura de dados organizada por pasta
        """
        folder_contents = {}

        for file_path, is_selected in files_with_states:
            rel_path = os.path.relpath(file_path, self.project_path)
            parts = rel_path.split(os.sep)

            current_path = ""
            for i, part in enumerate(parts[:-1]):
                parent_path = current_path
                current_path = os.path.join(current_path, part) if current_path else part

                if current_path not in folder_contents:
                    folder_contents[current_path] = {
                        'parent': parent_path,
                        'files': [],
                        'subfolders': set()
                    }

                if parent_path in folder_contents:
                    folder_contents[parent_path]['subfolders'].add(current_path)

            if os.path.isfile(file_path):
                folder = os.path.dirname(rel_path)
                if folder not in folder_contents:
                    folder_contents[folder] = {
                        'parent': os.path.dirname(folder),
                        'files': [],
                        'subfolders': set()
                    }
                folder_contents[folder]['files'].append(
                    (file_path, parts[-1], is_selected)
                )

        return folder_contents