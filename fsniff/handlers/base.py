import hashlib
import io
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

class BaseHandler(ABC):
    def __init__(self, filepath: Optional[Path], config: Dict[str, Any], stream: Optional[io.IOBase] = None, size: int = 0):
        self.filepath = filepath
        self.config = config
        self.stream = stream
        self._size = size if stream else (filepath.stat().st_size if filepath else 0)
        self._cached_md5 = None

    def get_size(self) -> int:
        return self._size

    def calculate_md5(self) -> str:
        if self._cached_md5:
            return self._cached_md5

        hash_md5 = hashlib.md5()
        if self.stream:
            # Garante que estamos no início se for um stream reaproveitável
            if self.stream.seekable():
                self.stream.seek(0)
            for chunk in iter(lambda: self.stream.read(4096), b""):
                if isinstance(chunk, str):
                    chunk = chunk.encode('utf-8')
                hash_md5.update(chunk)
            if self.stream.seekable():
                self.stream.seek(0)
        elif self.filepath:
            with open(self.filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)

        self._cached_md5 = hash_md5.hexdigest()
        return self._cached_md5

    def check_md5(self, expected_md5: Optional[str]) -> bool:
        if not expected_md5:
            return True
        return self.calculate_md5() == expected_md5

    @abstractmethod
    def get_head(self, n_lines: int) -> List[str]:
        pass

    @abstractmethod
    def get_type_info(self) -> str:
        pass

    def _read_lines(self, n_lines: int) -> List[str]:
        """Helper para ler linhas de stream ou arquivo."""
        lines = []
        try:
            if self.stream:
                if self.stream.seekable():
                    self.stream.seek(0)
                # Stream do zip costuma ser bytes
                for _ in range(n_lines):
                    line = self.stream.readline()
                    if not line: break
                    if isinstance(line, bytes):
                        line = line.decode('utf-8', errors='replace')
                    lines.append(line.rstrip())
                if self.stream.seekable():
                    self.stream.seek(0)
            elif self.filepath:
                with open(self.filepath, 'r', encoding='utf-8', errors='replace') as f:
                    for _ in range(n_lines):
                        line = f.readline()
                        if not line: break
                        lines.append(line.rstrip())
        except Exception as e:
            lines.append(f"Error reading: {str(e)}")
        return lines
