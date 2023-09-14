import argparse
import json
import time
import psutil
import logging

from functools import wraps

from brute_force_zip import main as brute_force_main
from desafio_chaos import main as gera_chaos_data_main

logging.basicConfig(
        filename="log_file.log",
        format="%(asctime)s %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
        force=True,
    )

dict_modos_disponiveis = {}

def add_modos(funcao):
    return dict_modos_disponiveis.setdefault(
        funcao.__name__, funcao
    )

def show_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        init = time.time()

        result = func(*args, **kwargs)

        execution_diff = time.time() - init

        print(f"[+] {func.__name__} -> {int(execution_diff*1000)}ms")
        logging.debug(f"Executando {func.__name__} duracao {int(execution_diff*1000)}ms")
        return result
    return wrapper


def setup_arguments() -> argparse.ArgumentParser:
    parser =  argparse.ArgumentParser(
        description="Parser dos argumentos passados no script"
    )
    parser.add_argument(
        "--mode", "-m", required=True, choices=dict_modos_disponiveis.keys(), type=str, help="Define um mode de execucao do script"
    )
    parser.add_argument(
        "--n_threads", "-nt", type=int, help="Define um numero de threads", default=1
    )
    parser.add_argument(
        "--output", "-o", type=argparse.FileType("w+"), default="output.txt",
        nargs="?", help="Define arquivo output"
    )
    parser.add_argument(
        "--loglevel", "-ll", choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"), help="Define um numero de threads", default=1
    
    )
    parser.add_argument(
        "--n_gpu", "-ng", type=int, help="Define um numero de GPUs", default=None
    )
    return parser

@add_modos
@show_execution_time
def env_metrics(*args, **kwargs):
    print("EXECUTANDO env_metrics")
    metrics = {}
    metrics["CPU Usage"]= psutil.cpu_percent(interval=1)
    metrics["Memory total"]= psutil.virtual_memory().total
    metrics["Memory Disponivel"]= psutil.virtual_memory().available
    
    if metrics["CPU Usage"] > 15:
        logging.critical(f"ALTO CONSUMO DE CPU: {metrics['CPU Usage']}%")
    
    print(json.dumps(metrics, indent=4))

@add_modos
@show_execution_time
def brute_force(n_threads, *args, **kwargs):
    print("EXECUTANDO BRUTE FORCE!")
    brute_force_main(n_threads)

@add_modos
@show_execution_time
def busca_chaos_bounty(n_threads, *args, **kwargs):
    print("Buscando todos os dominios com bounty")
    gera_chaos_data_main(n_threads)


if __name__ == "__main__":
    args = setup_arguments().parse_args()

    print(f"NUMERO DE THREADS DEFINIDAS: {args.n_threads}", )

    kwargs = {
        "n_threads": args.n_threads,
    }

    if args.mode in dict_modos_disponiveis.keys():
        dict_modos_disponiveis[args.mode](**kwargs)

