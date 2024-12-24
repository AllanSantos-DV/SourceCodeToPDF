# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('src/ui/*.py', 'ui'),
    ('src/core/*.py', 'core'),
    ('src/config/*.py', 'config'),
    ('src/pdf/*.py', 'pdf')
]

a = Analysis(
    ['src/main.py'],  # Script principal
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
        'ttkbootstrap',
        'pdfkit',
        'pygments',
        'reportlab',
        'pygments.lexers',
        'pygments.formatters',
        'pygments.styles',
        'core',
        'ui',
        'pdf',
        'config',
        'ui.main_window',
        'ui.components',
        'ui.dialogs',
        'core.file_handler',
        'core.file_manager',
        'core.selection_manager',
        'pdf.generator',
        'config.settings'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SourceCodeToPDF',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Altere para True se deseja que a aplicação seja executada em modo console
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/assets/pdf.ico'  # Certifique-se que o ícone existe neste caminho
)