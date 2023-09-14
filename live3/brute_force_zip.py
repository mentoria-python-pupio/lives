import multiprocessing
import time

import zipfile


def generate_pass(n_char: int = 6, offset: int = 0, stop: int = None) -> int:
    if not stop:
        stop = 10**n_char
    for pwd in range(offset, stop):
        yield str(pwd).zfill(n_char)
    
def try_pwd(n_char: int, offset: int, stop: int, shared_condition: multiprocessing.Manager) -> None:
    gerador = generate_pass(n_char, offset, stop)
    for pwd in gerador:
        try:
            with zipfile.ZipFile("teste.zip", mode="r") as zip_file:
                bytes_pwd = bytes(pwd, encoding="utf-8")
                zip_file.extractall(pwd=bytes_pwd)
                print(f"[+] password: {pwd}")
                shared_condition.value = int(pwd)
                break
        except Exception:
            continue


def main(n_threads: int = 4):
    print("INICIANDO BRUTE FORCE!")
    ### - MULTI PROCESSING
    init = time.time()
    N_THREADS = n_threads

    manager = multiprocessing.Manager()
    shared_condition = manager.Value('i', 0)

    tamanho_senhas = 6
    
    possibilidade_senhas = 10 ** tamanho_senhas

    senhas_por_thread = possibilidade_senhas // N_THREADS  

    workers = []
    for i in range(1, N_THREADS+ 1):
        print(f"Iniciando Processo {i}")
        offset = (i - 1) * senhas_por_thread
        stop = i * senhas_por_thread
        processo = multiprocessing.Process(
            target=try_pwd,
            args=(
                tamanho_senhas,
                offset,
                stop,
                shared_condition
            )
        )
        workers.append(processo)
        processo.start()


    while True:
        if shared_condition.value != 0:
            if any([
                worker.is_alive() for worker in workers
            ]):
                for worker in filter(lambda worker: worker.is_alive(), workers):
                    worker.kill()
            else:
                print("Todos os processos foram encerrados!")
                break
        else:
            time.sleep(1)

    for worker in workers:
        worker.join()

    print(f"Parallel time: {(time.time() -init):.2f}s")

    print("FIM DO PROGRAMA!")

if __name__ == "__main__":
    main()

    