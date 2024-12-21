import ttkbootstrap as ttk
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = ttk.Window(themename="cosmo")

    # Centralizar a janela
    app_width = 400  # Largura da janela
    app_height = 250  # Altura da janela
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    position_x = (screen_width // 2) - (app_width // 2)
    position_y = (screen_height // 2) - (app_height // 2)
    app.geometry(f"{app_width}x{app_height}+{position_x}+{position_y}")

    MainWindow(app)
    app.mainloop()
