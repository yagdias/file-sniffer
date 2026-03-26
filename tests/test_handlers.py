from grimsniffer.handlers import get_handler, TextFileHandler, VCFFileHandler

def test_text_handler_valid(tmp_files):
    handler = get_handler(tmp_files['valid_txt'])
    assert isinstance(handler, TextFileHandler)
    assert handler.validate_content() is True
    assert handler.get_size() > 0
    meta = handler.read_metadata()
    assert "Linha 1" in meta
    
def test_text_handler_empty(tmp_files):
    handler = get_handler(tmp_files['empty_txt'])
    assert handler.validate_content() is False
    assert handler.get_size() == 0
    assert handler.read_metadata() == "Arquivo vazio."

def test_vcf_handler_valid(tmp_files):
    handler = get_handler(tmp_files['valid_vcf'])
    assert isinstance(handler, VCFFileHandler)
    assert handler.validate_content() is True
    meta = handler.read_metadata()
    assert "##fileformat=VCFv4.2" in meta
    assert "#CHROM" in meta
