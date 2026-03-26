from pathlib import Path
from typing import Dict, Any, Type, Optional
import io
from fsniff.handlers.base import BaseHandler
from fsniff.handlers.text import TextHandler, LogHandler
from fsniff.handlers.csv import CSVHandler
from fsniff.handlers.zip import ZipHandler

class HandlerFactory:
    _handlers: Dict[str, Type[BaseHandler]] = {
        ".csv": CSVHandler,
        ".txt": TextHandler,
        ".log": LogHandler,
        ".zip": ZipHandler,
        "default": TextHandler
    }

    @classmethod
    def register_handler(cls, suffix: str, handler_class: Type[BaseHandler]):
        cls._handlers[suffix.lower()] = handler_class

    @classmethod
    def get_handler(cls, filepath: Optional[Path], config: Optional[Dict[str, Any]] = None, stream: Optional[io.IOBase] = None, filename: Optional[str] = None) -> BaseHandler:
        config = config or {}

        # Determina o suffix a partir do path ou do nome do arquivo (se for dentro do zip)
        suffix = ""
        if filepath:
            suffix = filepath.suffix.lower()
        elif filename:
            suffix = Path(filename).suffix.lower()

        handler_class = cls._handlers.get(suffix, cls._handlers["default"])

        if config.get("type"):
            type_mapping = {
                "csv": CSVHandler,
                "text": TextHandler,
                "log": LogHandler,
                "zip": ZipHandler
            }
            handler_class = type_mapping.get(config["type"].lower(), handler_class)

        return handler_class(filepath, config, stream=stream)
