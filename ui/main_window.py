from tkinter import filedialog, messagebox, Toplevel, IntVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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
        # Abrir diálogo para selecionar pasta
        folder = filedialog.askdirectory(title="Selecione a pasta do projeto")
        if not folder:
            messagebox.showwarning("Aviso", "Nenhuma pasta selecionada")
            return

        # Atualiza o caminho da pasta no rótulo
        self.project_path = folder
        self.folder_label.config(text=f"Pasta selecionada:\n{folder}")

        # Obter arquivos da pasta
        files = FileManager.list_files_in_directory_with_ignored(folder)
        if not files:
            messagebox.showinfo("Aviso", "Nenhum arquivo encontrado na pasta selecionada.")
            return

        # Abrir janela de seleção de arquivos
        self.show_file_selection_window(files)

    def show_file_selection_window(self, files_with_states):
        selection_window = Toplevel(self.root)
        selection_window.title("Seleção de Arquivos")
        selection_window.geometry("600x600")

        file_vars = {}  # Dicionário para armazenar o estado dos checkboxes
        frame = ttk.Frame(selection_window)
        frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

        canvas = ttk.Canvas(frame)
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Exibir arquivos na lista geral
        for file, is_selected in files_with_states:
            var = IntVar(value=1 if is_selected else 0)
            file_vars[file] = var
            ttk.Checkbutton(
                scrollable_frame,
                text=file,
                variable=var,
                bootstyle="round-toggle"
            ).pack(anchor=W, padx=10, pady=2)

        def confirm_selection():
            # Atualizar a lista de arquivos selecionados
            self.selected_files = [file for file, var in file_vars.items() if var.get() == 1]
            selection_window.destroy()

        confirm_btn = ttk.Button(
            selection_window,
            text="Confirmar Seleção",
            command=confirm_selection,
            bootstyle=SUCCESS
        )
        confirm_btn.pack(pady=10)

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

    def update_progress(self, current, total):
        self.progress['value'] = (current / total) * 100
        self.root.update_idletasks()
