import pytest

@pytest.fixture
def tmp_files(tmp_path):
    valid_txt = tmp_path / "valido.txt"
    valid_txt.write_text("Linha 1\nLinha 2\nTeste do GrimSniffer.", encoding="utf-8")
    
    empty_txt = tmp_path / "vazio.txt"
    empty_txt.write_text("", encoding="utf-8")
    
    valid_vcf = tmp_path / "exemplo.vcf"
    valid_vcf.write_text("##fileformat=VCFv4.2\n##source=my_source\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n1\t100\t.\tA\tT\t100\tPASS\t.", encoding="utf-8")
    
    return {
        'valid_txt': valid_txt,
        'empty_txt': empty_txt,
        'valid_vcf': valid_vcf
    }
