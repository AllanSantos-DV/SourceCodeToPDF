import logging
import threading
import time
from dataclasses import dataclass
from typing import Dict, Set, Optional

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class SelectionState:
    """Classe para armazenar o estado de seleção de um item"""
    is_selected: bool
    is_partial: bool = False  # Para pastas com seleção parcial
    last_updated: float = 0.0  # Timestamp da última atualização


class FileSelectionManager:
    """
    Gerenciador central de seleção de arquivos e pastas.
    Responsável por manter a consistência do estado de seleção.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._states: Dict[str, SelectionState] = {}
        self._folder_hierarchy: Dict[str, Set[str]] = {}  # pasta -> conjunto de itens
        self._parent_folders: Dict[str, str] = {}  # item -> pasta pai

    def register_item(self, path: str, parent_folder: Optional[str] = None) -> None:
        """
        Registra um novo item (arquivo ou pasta) no gerenciador.

        Args:
            path: Caminho do item
            parent_folder: Pasta pai do item (opcional)
        """
        with self._lock:
            if path not in self._states:
                self._states[path] = SelectionState(is_selected=False)

            if parent_folder:
                self._parent_folders[path] = parent_folder
                if parent_folder not in self._folder_hierarchy:
                    self._folder_hierarchy[parent_folder] = set()
                self._folder_hierarchy[parent_folder].add(path)

    def update_selection(self, path: str, is_selected: bool) -> None:
        """
        Atualiza o estado de seleção de um item e propaga as alterações.

        Args:
            path: Caminho do item
            is_selected: Novo estado de seleção
        """
        with self._lock:
            try:
                logger.debug(f"Atualizando seleção de {path} para {is_selected}")

                # Atualiza o estado do item
                self._states[path] = SelectionState(
                    is_selected=is_selected,
                    last_updated=time.time()
                )

                # Se for uma pasta, propaga para os filhos
                if path in self._folder_hierarchy:
                    self._propagate_to_children(path, is_selected)

                # Atualiza o estado das pastas pai
                self._update_parent_states(path)

            except Exception as e:
                logger.error(f"Erro ao atualizar seleção: {str(e)}")
                raise

    def _propagate_to_children(self, folder_path: str, is_selected: bool) -> None:
        """
        Propaga o estado de seleção para todos os itens dentro de uma pasta.

        Args:
            folder_path: Caminho da pasta
            is_selected: Estado de seleção a ser propagado
        """
        for item in self._folder_hierarchy[folder_path]:
            self._states[item] = SelectionState(
                is_selected=is_selected,
                last_updated=time.time()
            )
            if item in self._folder_hierarchy:  # Se o item é uma pasta
                self._propagate_to_children(item, is_selected)

    def _update_parent_states(self, path: str) -> None:
        """
        Atualiza o estado das pastas pai baseado nos estados dos filhos.

        Args:
            path: Caminho do item que teve seu estado alterado
        """
        current = path
        while current in self._parent_folders:
            parent = self._parent_folders[current]
            children_states = [
                self._states[child].is_selected
                for child in self._folder_hierarchy[parent]
            ]

            # Calcula o novo estado da pasta
            all_selected = all(children_states)
            any_selected = any(children_states)

            self._states[parent] = SelectionState(
                is_selected=all_selected,
                is_partial=any_selected and not all_selected,
                last_updated=time.time()
            )

            current = parent

    def get_state(self, path: str) -> SelectionState:
        """
        Retorna o estado atual de um item.

        Args:
            path: Caminho do item

        Returns:
            SelectionState atual do item
        """
        with self._lock:
            return self._states.get(path, SelectionState(is_selected=False))