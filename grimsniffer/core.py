import os
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

from rich.console import Console
from rich.table import Table
from rich.progress import track

from .handlers import get_handler

console = Console()

def read_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}

import random

def get_reaper_joke(size: int, is_valid: bool, ext: str) -> str:
    jokes = []
    if size == 0:
        jokes.extend([
            "Nem a poeira cósmica quis habitar aqui. Vácuo puro.",
            "Arquivo 100% ecológico: zero bytes de emissão de carbono.",
            "O vazio existencial deste arquivo me deu calafrios na espinha.",
            "Ceifar o nada... meu trabalho nunca foi tão fácil.",
            "Já vi almas mais pesadas que o conteúdo desse arquivo."
        ])
    elif size > 100 * 1024 * 1024:  # 100MB
        jokes.extend([
            "Mais de 100MB? Quem você acha que eu sou, um caminhão de mudança do além?",
            "Pesado demais... O que tem aqui dentro? O backup do universo inteiro?",
            "Um verdadeiro buraco negro consumindo meu precioso tempo de leitura.",
            "Se eu ceifar esse aqui, o pente de memória agradece.",
            "Tá carregando tijolo digital? Que arquivo colossal."
        ])
    else:
        if ext in ['.vcf', '.vcf.gz']:
            jokes.extend([
                "Muitas variantes aqui... espero que alguma cure a feiura desse dataset.",
                "O genoma não mente, mas esse bloco de texto me deixa com sérias dúvidas."
            ])
        elif size < 1024:
            jokes.extend([
                "Pequenininho, mal dá pra sujar a foice.",
                "Menos de 1KB? Esse arquivo tá obviamente fazendo dieta low-byte."
            ])
        else:
            jokes.extend([
                "Cheirinho de dados mortais normais... sem graça nenhuma.",
                "Tudo perece, e esse arquivo absolutamente certinho não é exceção."
            ])
    return random.choice(jokes)

def run_inspection(target_dirs: List[str], config: Optional[Dict] = None, sass_mode: bool = False):
    results = []
    
    files_to_inspect = []
    
    # Simple discovery based on passed directories or config target dirs
    paths_to_check = target_dirs.copy()
    if config and 'targets' in config:
        paths_to_check.extend(config['targets'])
        
    for d in paths_to_check:
        p = Path(d)
        if p.is_file():
            files_to_inspect.append(p)
        elif p.is_dir():
            files_to_inspect.extend(list(p.rglob("*")))
            
    # Filter files strictly if extensions are provided
    valid_extensions = config.get('extensions', []) if config else []
    if valid_extensions:
        filtered = []
        for f in files_to_inspect:
            if f.is_file():
                if any(f.name.endswith(ext) for ext in valid_extensions):
                    filtered.append(f)
        files_to_inspect = filtered
    else:
        files_to_inspect = [f for f in files_to_inspect if f.is_file()]
    
    table = Table(title="GrimSniffer - Inspeção e Ceifa de Arquivos")
    table.add_column("Arquivo", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Tamanho (bytes)", justify="right", style="green")
    
    report_title = config.get('report_title', 'GrimSniffer - Relatório de Inspeção') if config else 'GrimSniffer - Relatório de Inspeção'
    md_report = [f"# {report_title}", ""]
    
    from .handlers import ZipFileHandler
    import zipfile

    # Using tracking for visual progress
    for filepath in track(files_to_inspect, description="Inspecionando..."):
        handler = get_handler(filepath)
        size = handler.get_size()
        is_valid = handler.validate_content()
        status_icon = "✅" if is_valid else "❌"
        
        name_display = filepath.name
        if isinstance(handler, ZipFileHandler) and is_valid:
            try:
                with zipfile.ZipFile(filepath, 'r') as z:
                    inner_files = z.namelist()
                    if inner_files:
                        tree_items = [f"  ├── {f}" for f in inner_files[:-1]]
                        tree_items.append(f"  └── {inner_files[-1]}")
                        name_display = f"[bold cyan]{filepath.name}[/bold cyan]\n" + "\n".join(tree_items)
            except zipfile.BadZipFile:
                pass
                
        table.add_row(name_display, status_icon, str(size))
        
        # Build markdown part
        meta = handler.read_metadata()
        md_report.append(f"## `{filepath.name}`")
        md_report.append(f"- **Tamanho**: {size} bytes")
        md_report.append(f"- **Status**: {'Válido' if is_valid else 'Vazio / Inválido'}")
        
        if sass_mode:
            joke = get_reaper_joke(size, is_valid, filepath.suffix.lower())
            md_report.append(f"- **Comentário do Ceifador**: *{joke}*")
        
        md_report.append("- **Amostra / Cabeçalho**:")
        md_report.append("```text")
        md_report.append(meta)
        md_report.append("```")
        md_report.append("")
        
    console.print(table)
    
    output_report = config.get('output_report', 'grimsniffer_report.md') if config else 'grimsniffer_report.md'
    with open(output_report, "w", encoding='utf-8') as f:
        f.write('\n'.join(md_report))
        
    console.print(f"[bold green]Inspeção finalizada! Relatório salvo em {output_report}[/bold green]")
