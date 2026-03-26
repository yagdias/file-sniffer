from fsniff.handlers.base import BaseHandler
from typing import List

class TextHandler(BaseHandler):
    def get_head(self, n_lines: int) -> List[str]:
        return self._read_lines(n_lines)

    def get_type_info(self) -> str:
        return "Plain Text"

class LogHandler(TextHandler):
    def get_type_info(self) -> str:
        return "Log File"
