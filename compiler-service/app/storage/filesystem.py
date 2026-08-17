from pathlib import Path


class FileStorage:
    def __init__(self, root: Path):
        self._root = root

    def get(self, filename: str) -> Path:
        path = (self._root / filename).resolve()

        if not path.is_relative_to(self._root.resolve()):
            raise ValueError("Недопустимый путь к файлу")

        if not path.exists():
            raise FileNotFoundError(
                f"Файл не найден: {filename}"
            )

        if not path.is_file():
            raise ValueError(
                f"Указанный путь не является файлом: {filename}"
            )

        return path
