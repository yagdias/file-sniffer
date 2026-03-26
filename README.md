# GrimSniffer 💀

O **GrimSniffer** é uma ferramenta de linha de comando (CLI) leve e implacável para inspecionar, ceifar o vácuo e logar instantaneamente detalhes sobre arquivos e compilações (`.txt`, `.csv`, `.zip`, `.vcf`, `.gz`...). 

Sua arquitetura o torna perfeito para uso diário, lida transparentemente com formatos compactados extraindo apenas o necessário (através de `Geradores` limitados), desenha tudo em uma tela interativa via `rich` e preenche cadernos Markdown úteis para checkups manuais ou auditorias de qualidade em integrações contínuas!

## ⚙️ Instalação

Adicione na sua máquina usando um ambiente empacotado:
```bash
conda env create -f environment.yml
conda activate grimsniffer
pip install -e .
```

## 🚀 Uso Rápido (CLI)

1. **Inspeção Direta Ad-Hoc**:
Inspecione diretórios ou alvos manualmente direto do console.
```bash
grimsniffer run ./meu_output ./outra_pasta/amostras
```

2. **Template e Pipelines YAML**:
Para rodar inspeções controladas acopladas ao seu WDL / Nextflow / Github actions:
```bash
grimsniffer generate-template
```
Esse comando irá vomitar um modelo funcional `pipeline_conf.yml` no seu terminal atual. Edite as matrizes para alvos (`targets`) precisos e extensões restritas, testando dezenas de pastas ao mesmo tempo num só pulso!

Execute a varredura orientada ao yaml passando o flag especial `-c`:
```bash
grimsniffer run -c pipeline_conf.yml
```

3. **Validação Sanitária**:
Seus pipelines automatizados estão cuspindo YAMLs defeituosos?
```bash
grimsniffer validate pipeline_conf.yml
```

> Feito com ódio pelo vácuo de disco.