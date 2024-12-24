import ttkbootstrap as ttk

from ui.main_window import MainWindow

if __name__ == "__main__":
    app = ttk.Window(themename="cosmo")

    # Centralizar a janela
    MainWindow.center_window(app, 400, 300)

    MainWindow(app)
    app.mainloop()
