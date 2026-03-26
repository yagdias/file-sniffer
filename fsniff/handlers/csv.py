import csv
import io
from fsniff.handlers.text import TextHandler
from typing import List

class CSVHandler(TextHandler):
    def get_head(self, n_lines: int) -> List[str]:
        lines = []
        try:
            if self.stream:
                if self.stream.seekable(): self.stream.seek(0)
                content = self.stream.read().decode('utf-8', errors='replace')
                f = io.StringIO(content)
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if i >= n_lines: break
                    lines.append(", ".join(row))
                if self.stream.seekable(): self.stream.seek(0)
            elif self.filepath:
                with open(self.filepath, 'r', newline='', encoding='utf-8', errors='replace') as f:
                    reader = csv.reader(f)
                    for i, row in enumerate(reader):
                        if i >= n_lines: break
                        lines.append(", ".join(row))
        except Exception as e:
            return [f"Error reading CSV: {str(e)}"]
        return lines

    def get_type_info(self) -> str:
        try:
            if self.stream:
                if self.stream.seekable(): self.stream.seek(0)
                content = self.stream.read(4096).decode('utf-8', errors='replace')
                f = io.StringIO(content)
                reader = csv.reader(f)
                header = next(reader)
                if self.stream.seekable(): self.stream.seek(0)
                return f"CSV (Columns: {', '.join(header)})"
            elif self.filepath:
                with open(self.filepath, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    return f"CSV (Columns: {', '.join(header)})"
        except:
            pass
        return "CSV File"
