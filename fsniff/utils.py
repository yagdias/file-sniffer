import yaml
import glob
import os
import zipfile
import hashlib
import io
from pathlib import Path
from typing import List, Dict, Any, Optional
from fsniff.factory import HandlerFactory

def load_config(config_path: Path) -> Dict[str, Any]:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def find_files(base_dir: Path, targets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    all_found = []
    for target in targets:
        pattern = target.get('pattern', '*')
        recursive = target.get('recursive', '**' in pattern)
        paths = list(base_dir.glob(pattern)) if not recursive else list(base_dir.rglob(pattern))
        for p in paths:
            if p.is_file():
                all_found.append({'path': p, 'config': target})
    return all_found

def process_file(filepath: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    handler = HandlerFactory.get_handler(filepath, config)

    head_lines = config.get('head', 5)
    size = handler.get_size()
    md5 = handler.calculate_md5()
    head = handler.get_head(head_lines)
    type_info = handler.get_type_info()

    expected_md5 = config.get('md5')
    md5_match = handler.check_md5(expected_md5) if expected_md5 else None

    has_content = size > 0

    result = {
        'name': filepath.name,
        'rel_path': filepath, # Removido is_relative_to por compatibilidade e simplicidade
        'size': size,
        'md5': md5,
        'md5_match': md5_match,
        'head': head,
        'type_info': type_info,
        'has_content': has_content,
        'internal_files': []
    }

    if filepath.suffix.lower() == '.zip' and config.get('recursive_zip', True):
        try:
            with zipfile.ZipFile(filepath, 'r') as zf:
                include_patterns = config.get('include', ['*'])
                for member in zf.infolist():
                    if not member.is_dir():
                        matches = any(Path(member.filename).match(p) for p in include_patterns)
                        if matches:
                            with zf.open(member) as member_stream:
                                # Usamos o HandlerFactory para o arquivo interno!
                                # Passamos um BytesIO do conteúdo para o handler para evitar múltiplos reads de zip
                                content_bytes = member_stream.read()
                                internal_stream = io.BytesIO(content_bytes)

                                internal_handler = HandlerFactory.get_handler(
                                    None,
                                    config,
                                    stream=internal_stream,
                                    filename=member.filename
                                )

                                result['internal_files'].append({
                                    'name': f"{filepath.name} > {member.filename}",
                                    'size': member.file_size,
                                    'md5': internal_handler.calculate_md5(),
                                    'head': internal_handler.get_head(head_lines),
                                    'has_content': member.file_size > 0,
                                    'type_info': f"Inside Zip: {internal_handler.get_type_info()}"
                                })
        except Exception as e:
            result['error'] = f"Error processing zip internals: {str(e)}"

    return result
