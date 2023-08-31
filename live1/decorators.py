def log_decorator(func):
    """Funcao de coradora para log

    Args:
        func (funcao): funcao a ser decorada
    """
    def wrapper(*args, **kwargs) -> int:
        # Fazer qualquer coisa antes de executar a funcao
        args = [i * 10 for i in args]
        print("ANTES DE EXECUTAR A FUNCAO")
        
        resultado = func(*args, **kwargs)

        if resultado > 10:
            print("ACHEI UM BUG!!!!")
        return resultado
    return wrapper

@log_decorator(log_level="Warning")
def funcao_critica(a, b):
    print("fazendo uma conta...")
    return a * b

