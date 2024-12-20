# main.py

import ttkbootstrap as ttk
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = ttk.Window(themename="cosmo")
    MainWindow(app)
    app.mainloop()
