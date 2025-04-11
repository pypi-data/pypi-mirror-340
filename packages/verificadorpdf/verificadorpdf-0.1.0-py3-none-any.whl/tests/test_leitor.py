from verificadorpdf.leitor import verificar_palavra_em_pdf

def test_verificacao_basica():
    assert verificar_palavra_em_pdf('exemplo.pdf', 'solteiro') == True