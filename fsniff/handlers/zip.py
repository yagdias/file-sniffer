import zipfile
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from fsniff.handlers.base import BaseHandler

class ZipHandler(BaseHandler):
    def get_head(self, n_lines: int) -> List[str]:
        try:
            with zipfile.ZipFile(self.filepath, 'r') as zf:
                files = zf.namelist()
                return [f"Zip contains {len(files)} files:", *files[:n_lines]]
        except Exception as e:
            return [f"Error reading zip: {str(e)}"]

    def get_type_info(self) -> str:
        try:
            with zipfile.ZipFile(self.filepath, 'r') as zf:
                return f"ZIP Archive ({len(zf.infolist())} items)"
        except:
            return "ZIP Archive"

    def extract_internal_files(self) -> List[Dict[str, Any]]:
        # Essa lógica será usada pelo processador principal para tratar cada arquivo dentro do zip
        results = []
        try:
            with zipfile.ZipFile(self.filepath, 'r') as zf:
                for member in zf.infolist():
                    if not member.is_dir():
                        results.append({
                            "name": member.filename,
                            "size": member.file_size,
                            "is_zip_member": True,
                            "zip_path": self.filepath,
                            "content_reader": lambda m=member: zf.open(m).read()
                        })
        except:
            pass
        return results
