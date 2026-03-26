import os
import gzip
import zipfile
from pathlib import Path
from typing import Iterator, Optional, Tuple, List, Generator

class BaseFileHandler:
    """Base interface for dealing with specific file types."""
    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)
    
    def get_size(self) -> int:
        return self.filepath.stat().st_size
        
    def validate_content(self) -> bool:
        """Return True if file is valid/has content, False otherwise (empty/corrupted)."""
        raise NotImplementedError
        
    def read_metadata(self) -> str:
        """Extract header/metadata from the file."""
        raise NotImplementedError

class TextFileHandler(BaseFileHandler):
    """Handler for standard text files."""
    def __init__(self, filepath: str | Path, header_lines: int = 10):
        super().__init__(filepath)
        self.header_lines = header_lines
        
    def validate_content(self) -> bool:
        """Returns True if file has at least 1 byte/character, False if empty."""
        return self.get_size() > 0

    def _open_file(self):
        """Helper to open different file extensions transparently if needed."""
        return open(self.filepath, 'rt', encoding='utf-8', errors='replace')
        
    def read_metadata(self) -> str:
        if self.get_size() == 0:
            return "Arquivo vazio."
            
        lines = []
        try:
            with self._open_file() as f:
                for i, line in enumerate(f):
                    if i >= self.header_lines:
                        break
                    lines.append(line.rstrip('\n'))
            return '\n'.join(lines)
        except Exception as e:
            return f"Erro de leitura: {e}"

class VCFFileHandler(TextFileHandler):
    """Specific handler for VCF files to capture metadata and column headers."""
    def __init__(self, filepath: str | Path):
        super().__init__(filepath, header_lines=0) # header_lines ignored directly
        
    def read_metadata(self) -> str:
        if self.get_size() == 0:
            return "VCF vazio."
            
        meta_lines = []
        try:
            with self._open_file() as f:
                for line in f:
                    clean_line = line.rstrip('\n')
                    meta_lines.append(clean_line)
                    if not clean_line.startswith('##'):
                        # Should be the #CHROM line
                        break
            
            # VCFs can have hundreds of meta lines. Just return first few and the columns.
            if len(meta_lines) > 8:
                return '\n'.join(meta_lines[:5] + ["..."] + [meta_lines[-1]])
            return '\n'.join(meta_lines)
        except Exception as e:
            return f"Erro lendo VCF: {e}"

class GzTextFileHandler(TextFileHandler):
    def _open_file(self):
        return gzip.open(self.filepath, 'rt', encoding='utf-8', errors='replace')
        
class GzVCFFileHandler(VCFFileHandler):
    def _open_file(self):
        return gzip.open(self.filepath, 'rt', encoding='utf-8', errors='replace')

class ZipFileHandler(BaseFileHandler):
    """Handler that extracts information about contents of a Zip archive."""
    def validate_content(self) -> bool:
        if self.get_size() == 0:
            return False
            
        try:
            with zipfile.ZipFile(self.filepath, 'r') as z:
                return len(z.infolist()) > 0
        except zipfile.BadZipFile:
            return False
            
    def read_metadata(self) -> str:
        if self.get_size() == 0:
            return "Zip vazio."
            
        try:
            with zipfile.ZipFile(self.filepath, 'r') as z:
                info = z.infolist()
                if not info:
                    return "Zip não contem arquivos internamente."
                
                output = []
                for i in info:
                    output.append(f"📦 {i.filename} ({i.file_size} bytes):")
                    if i.file_size > 0 and not i.is_dir():
                        try:
                            with z.open(i) as f:
                                lines = []
                                for _ in range(5):
                                    line = f.readline()
                                    if not line: break
                                    lines.append("  " + line.decode('utf-8', errors='replace').rstrip('\n'))
                                output.append('\n'.join(lines))
                        except Exception:
                            output.append("  [Conteúdo binário ou ilegível]")
                    elif i.is_dir():
                        output.append("  [Pasta]")
                    else:
                        output.append("  [Vazio]")
                    output.append("") # Quebra de linha entre arquivos
                return '\n'.join(output).strip()
        except Exception as e:
            return f"Erro de leitura Zip: {e}"

def get_handler(filepath: str | Path) -> BaseFileHandler:
    """Factory to instantiate the appropriate handler based on file extension."""
    filepath = Path(filepath)
    name = filepath.name.lower()
    
    if name.endswith('.vcf'):
        return VCFFileHandler(filepath)
    elif name.endswith('.vcf.gz') or name.endswith('.vcf.bgz'):
        return GzVCFFileHandler(filepath)
    elif name.endswith('.gz'):
        return GzTextFileHandler(filepath)
    elif name.endswith('.zip'):
        return ZipFileHandler(filepath)
    else:
        # Padrão: TextFileHandler
        return TextFileHandler(filepath)
