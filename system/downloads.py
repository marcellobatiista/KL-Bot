def download_tesseract(output='tesseract.rar'):
    import os
    import gdown

    empty = None
    try:
        # Remove a pasta vazia para dar lugar ao arquivo baixado
        os.rmdir('comp_out/tesseract')
        empty = True
    except FileNotFoundError:
        # Se não existir, cria a pasta vazia
        os.makedirs('comp_out/tesseract')
        empty = True
    except OSError:
        # Se existir e estiver somente com o arquivo empty, remove
        if os.path.isfile('comp_out/tesseract/empty'):
            os.remove('comp_out/tesseract/empty')
            download_tesseract()
        else:
            empty = False

    if empty:
        # download
        url = 'https://drive.google.com/uc?id=1AgCfsPPDVmrELV95R1mzgkZZA0Z2LKeX'
        gdown.download(url, output, quiet=False)

        # extract
        import patoolib
        patoolib.extract_archive(output, outdir='comp_out/')
        os.remove(output)

