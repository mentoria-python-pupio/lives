import traceback

if __name__ == "__main__":
    print("INICIO DA EXECUCAO DO PROGRAMA!")

    try:
        print("Excutando o que eu preciso...")
        assert False, "Nao Retornou dados"
    except AssertionError:
        traceback_str = traceback.format_exc()
        print(f"Registrando no Log o erro: {traceback_str}")

    print("FIM DA EXECUCAO DO PROGRAMA!")