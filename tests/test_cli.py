from click.testing import CliRunner
from grimsniffer.cli import cli

def test_cli_generate_template():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['generate-template'])
        assert result.exit_code == 0
        assert "gerado com sucesso" in result.output
        
        # Test validation of the newly generated template
        res_val = runner.invoke(cli, ['validate', 'pipeline_conf.yml'])
        assert res_val.exit_code == 0
        assert "Válida" in res_val.output

def test_cli_run_without_args():
    runner = CliRunner()
    result = runner.invoke(cli, ['run'])
    # By design, the CLI just prints a message and exits properly
    assert result.exit_code == 0
    assert "Forneça arquivos" in result.output
