import click
import yaml
from .core import run_inspection, read_config

@click.group()
def cli():
    """GrimSniffer - Inspetor implacável e Ceifador de Arquivos"""
    pass

@cli.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
@click.option('--config', '-c', type=click.Path(exists=True), help="Caminho para o arquivo YAML de configuração")
@click.option('--sass', is_flag=True, hidden=True)
def run(paths, config, sass):
    """Inicia a inspeção mortífera nos arquivos e diretórios informados."""
    if not paths and not config:
        click.echo("Erro: Forneça arquivos/diretórios ou um arquivo de configuração.")
        return
        
    cfg = {}
    if config:
        cfg = read_config(config)
        
    run_inspection(list(paths), cfg, sass_mode=sass)

@cli.command()
def generate_template():
    """Gera um arquivo de modelo YAML base na hora."""
    template = {
        'targets': ['./samples'],
        'extensions': ['.txt', '.vcf', '.csv', '.gz', '.zip'],
        'output_report': 'grimsniffer_report.md',
        'report_title': 'Relatório Oficial de Inspeção'
    }
    with open('pipeline_conf.yml', 'w', encoding='utf-8') as f:
        yaml.dump(template, f, default_flow_style=False)
    click.echo("Modelo 'pipeline_conf.yml' gerado com sucesso!")

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
def validate(config_file):
    """Verifica se a configuração passada (YAML) é válida."""
    try:
        read_config(config_file)
        click.echo("✅ Configuração Válida e bem formatada.")
    except Exception as e:
        click.echo(f"❌ Configuração Inválida: {e}")

if __name__ == '__main__':
    cli()
