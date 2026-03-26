import click
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from fsniff.utils import find_files, process_file

console = Console()

@click.group(help="Ferramenta para inspecionar conteúdo de arquivos, checar integridade e gerar relatórios.")
def main():
    pass

@main.command(help="Gera um modelo de arquivo de configuração YAML.")
@click.option('--output', '-o', default='fsniff_config.yaml', help="Nome do arquivo de saída.")
def init(output):
    config = {
        'settings': {
            'default_head': 10,
            'report_name': 'report.md',
            'calc_md5': True
        },
        'targets': [
            {
                'pattern': 'data/*.csv',
                'head': 5,
                'type': 'csv',
                'md5': 'opcional_md5_esperado'
            },
            {
                'pattern': 'logs/**/*.log',
                'head': 10,
                'recursive': True
            },
            {
                'pattern': 'archives/*.zip',
                'recursive_zip': True,
                'include': ['*.txt', '*.log']
            }
        ]
    }
    with open(output, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    console.print(f"[green]Modelo de configuração gerado em: {output}[/green]")

@main.command(help="Executa a inspeção dos arquivos baseada no arquivo de configuração.")
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--dir', '-d', default='.', help="Diretório base para busca de arquivos (padrão: atual).")
@click.option('--report', '-r', help="Caminho do relatório Markdown de saída.")
def run(config_file, dir, report):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    base_dir = Path(dir)
    targets = config.get('targets', [])

    if not targets:
        console.print("[yellow]Nenhum alvo de busca definido no YAML.[/yellow]")
        return

    # 1. Busca arquivos
    found_files = find_files(base_dir, targets)
    if not found_files:
        console.print("[red]Nenhum arquivo encontrado para os padrões informados.[/red]")
        return

    # 2. Processa arquivos
    results = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Processando arquivos...", total=len(found_files))
        for item in found_files:
            res = process_file(item['path'], item['config'])
            results.append(res)
            progress.update(task, advance=1)

    # 3. Exibe Tabela Rich
    table = Table(title="Resumo da Inspeção (File Sniffer)")
    table.add_column("Arquivo", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Tipo", style="magenta")
    table.add_column("Tamanho", justify="right")
    table.add_column("MD5 Match", justify="center")

    total_files = 0
    failures = 0

    def add_result_to_table(res):
        nonlocal total_files, failures
        total_files += 1
        status = "[green]✔[/green]" if res['has_content'] else "[red]X[/red]"
        if not res['has_content']: failures += 1

        md5_status = "-"
        if res.get('md5_match') is True:
            md5_status = "[green]OK[/green]"
        elif res.get('md5_match') is False:
            md5_status = "[red]FAIL[/red]"
            failures += 1

        table.add_row(
            str(res['name']),
            status,
            res['type_info'],
            f"{res['size']} bytes",
            md5_status
        )

        # Arquivos internos do zip
        for internal in res.get('internal_files', []):
            total_files += 1
            i_status = "[green]✔[/green]" if internal['has_content'] else "[red]X[/red]"
            if not internal['has_content']: failures += 1

            table.add_row(
                f"  └─ {internal['name']}",
                i_status,
                internal['type_info'],
                f"{internal['size']} bytes",
                "-"
            )

    for r in results:
        add_result_to_table(r)

    console.print(table)
    console.print(f"\n[bold]Resumo:[/bold] Total de {total_files} arquivos checados. {failures} falhas detectadas.")

    # 4. Gera Relatório Markdown
    report_path = report or config.get('settings', {}).get('report_name', 'report.md')
    generate_markdown_report(results, report_path)
    console.print(f"\n[green]Relatório completo gerado em: {report_path}[/green]")

def generate_markdown_report(results, report_path):
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Relatório de Inspeção de Arquivos (fsniff)\n\n")

        for res in results:
            write_file_section(f, res)
            for internal in res.get('internal_files', []):
                write_file_section(f, internal, level=3)

def write_file_section(f, res, level=2):
    prefix = "#" * level
    f.write(f"{prefix} Arquivo: {res['name']}\n")
    f.write(f"- **Tipo:** {res['type_info']}\n")
    f.write(f"- **Tamanho:** {res['size']} bytes\n")
    f.write(f"- **MD5:** `{res['md5']}`\n")
    if res.get('md5_match') is not None:
        f.write(f"- **MD5 Check:** {'✅ OK' if res['md5_match'] else '❌ FALHOU'}\n")

    f.write("\n**Head (Conteúdo):**\n")
    f.write("```\n")
    if res['head']:
        for line in res['head']:
            f.write(f"{line}\n")
    else:
        f.write("[Arquivo Vazio ou Erro de Leitura]\n")
    f.write("```\n\n---\n\n")

if __name__ == '__main__':
    main()
