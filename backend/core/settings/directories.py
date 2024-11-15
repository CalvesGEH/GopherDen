import shutil
from pathlib import Path


class AppDirectories:
    def __init__(self, data_dir: Path) -> None:
        self.DATA_DIR = data_dir
        self.USER_DIR = data_dir.joinpath("users")
        self.TEMP_DIR = data_dir.joinpath(".temp")
        self.IMG_DIR = data_dir.joinpath("img")
        self.DB_DIR = data_dir.joinpath("db")
        self.ensure_directories()

    def ensure_directories(self):
        required_dirs = [
            self.TEMP_DIR,
            self.IMG_DIR,
            self.USER_DIR,
            self.DB_DIR,
        ]

        for dir in required_dirs:
            dir.mkdir(parents=True, exist_ok=True)
