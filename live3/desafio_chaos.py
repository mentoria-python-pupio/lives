import os
import threading
import time
import zipfile
from os.path import exists

import requests

# Missão 1: Pegar o Index.js do chaos - OK
# Missão 2: Filtrar apenas bouty==True - OK

# AQUI CABE A PARALELIZACAO
# Missão 3: Fazer Download do ZIP 
# Missão 4: Extrair o ZIP 
# Missão 5: Salvar txts numa pastinha de resultados

def get_json_data_from_chaos(only_bount: bool = True):
    # URL para buscar a lista de programas
    url = "https://chaos-data.projectdiscovery.io/index.json"
    # OBtendo a lista de programas
    response = requests.request("GET", url, data={})
    # Filtrando os programas que tem bounty == True
    if only_bount:
        dados = list(filter(lambda x: x["bounty"], response.json()))
    else:
        dados = response.json()
    return dados


def unzip_and_read_text_files(zip_file_path: str):
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall()

        extracted_files = zip_ref.namelist()
        lista_dominios = []
        # iteramos por todos os arquivos extraidos
        for file_name in extracted_files:
            with open(file_name, "r", encoding="utf-8") as _file:
                content = _file.readlines()
                lista_dominios.extend(content)
            # Removemos os arquivos extraidos
            os.remove(file_name)
    
    # Validacao para remover dominios e sub duplicados

    # EXEMPLO DE TRATATIVA EXTRA: 
    # REMOVER TODO MUNDO QUE COMECA COM TESTE
    # lista_dominios = list(filter(lambda x: not x.startswith("teste-"), lista_dominios))

    lista_dominios_tratado = sorted(set(lista_dominios))

    txt_file = "results/" + zip_file_path.split("/")[-1].split(".")[0] + ".txt"

    with open(txt_file, "w", encoding="utf-8") as _txt_file:
        _txt_file.writelines(lista_dominios_tratado)



def download_file(list_urls: list = []):
    for url in list_urls:
        output_file = url.split("/")[-1]
        response = requests.get(url=url, timeout=20)
        with open("zip/" + output_file, "wb") as file:
            file.write(response.content)

        unzip_and_read_text_files("zip/" +output_file)
    

def split_list(input_list, num_chunks):
    avg_chunk_size = len(input_list) // num_chunks
    remainder = len(input_list) % num_chunks
    chunks = []
    current_index = 0
    for _ in range(num_chunks):
        chunk_size = avg_chunk_size + 1 if remainder > 0 else avg_chunk_size
        chunks.append(input_list[current_index:current_index + chunk_size])
        current_index += chunk_size
        remainder -= 1
    return chunks

def main(n_threads: int = 40):
    t1 = time.time()
    # Missao 1 e 2:
    print(f"Iniciando Download dos dados base com {n_threads} Threads")
    dados = get_json_data_from_chaos(only_bount=True)

    lista_urls = [
        dado["URL"] for dado in dados
    ]
    
    if not os.path.exists("results"):
        os.mkdir("results")
    if not os.path.exists("zip"):
        os.mkdir("zip")
    

    N_THREADS = n_threads
    
    # Gerando uma carga balanceada para cada thread
    carga_balanceada = split_list(lista_urls, N_THREADS)

    # Missao 3
    # Definindo o paralelismo de download.
    threads = []
    print("Iniciando Threads")
    for i, chunk_urls in enumerate(carga_balanceada, start=1):
        print(f"Iniciando Threads: {i}", end="\r")
        thread = threading.Thread(
            target=download_file,
            args=(chunk_urls,)
        )
        threads.append(thread)
        thread.start()

    print()
    # Espera as threads terminarem
    print("Aguardando Encerramento das Threads")
    for thread in threads:
        thread.join()

    t2 = time.time()
    print(f"FIM DE PROGRAMA: {(t2 -t1):.2f}s")

if __name__ == "__main__":
    main()
    
    # # Missão 4 e 5
    # for dado in dados:
    #     files = extrai_zip(dado)

    #     # movendo os arquivos para resultados
    #     files


    # 
