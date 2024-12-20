# config/settings.py

from reportlab.lib.pagesizes import letter

SUPPORTED_EXTENSIONS = ('.java', '.py', '.js', '.html', '.css',
                        '.xml', '.json', '.md', '.txt', 'yaml', 'yml', 'sh', '.bat', '.cmd')
PAGE_SIZE = letter
DEFAULT_FONT_SIZE = 12
IGNORED_FOLDERS = ('properties', '.venv', '.config',
                   '__pycache__', '.git', '.idea', '.vscode', 'node_modules')
