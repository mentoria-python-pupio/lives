variavel =  "avsca"

numero = 15
pi = 3.14
name = "assdasdj".split("s")

boolean = True or False

listas = [1,2,3,4,5,6, ...]
listas.append(7)

coordinates = (1,)

class A:
    pass

def funcA(parametro):
    print("RECEBI PARAMETRO: ", parametro)



dict_func = {
    "opA": funcA
}


dict_ = {
    1: 1,
    "key": A(),
}

None # null

if [1]:
    print("NOK")
else:
    print("OK")

set([1,2,3,4,5,6,7,7,7,7,7,7,7])
{1,2,3,4,5,6,7,7,7,7,7,7,7} | {4}

# Paralelo da leitura em arquivo

with open("teste.txt", "r") as txt:
    text = txt.readlines()

# GERADORES


gerador = iter(range(0,10,2)) #[0, 2, 4, 6, 8]

for i in gerador:
    print(i)

import sys
sys.getsizeof("10000000")

quantidade_de_itens = (46 + 10 + 12) ** 8

memoria_utilizada_pela_lista= (8 * quantidade_de_itens // (1024 ** 5)) + (28* quantidade_de_itens // (1024 ** 5))
quantidade_de_itens_para_3GB_memoria = 3 * (1024 ** 3) // (28 + 8)

lista_de_3GB = [i for i in range(quantidade_de_itens_para_3GB_memoria)]

gerador = range(89478485)

gerador2 = iter(gerador)

for i in gerador2:
    continue

for i in list(range(894784850000)):
    continue

for i in range(894784850000):
    continue

sys.getsizeof(range(894784850000))

def lista_burra(n_chars: list = [7]) -> list:
    lista_pwds = []
    for n_char in n_chars:
        for pwd in range(10 ** n_char):
            lista_pwds.append(str(pwd).zfill(n_char))
    return lista_pwds

def lista_inteligente(n_chars: list = [7]) -> list:
    for n_char in n_chars:
        for pwd in range(10 ** n_char):
            yield str(pwd).zfill(n_char)

a = lista_inteligente([8])

from datetime import datetime

for i in a:
    print(f"Estou na senha {i}, hoje eh dia: {datetime.now().strftime('%Y-%m-%d')}", end="\r")


for contador, item in enumerate(a):
    print(f"Estou na senha {contador} - Valor: {item}, hoje eh dia: {datetime.now().strftime('%Y-%m-%d')}", end="\r")


try:
   print("Somei!")
   print("Somei!")
   print("Somei!")
   print("Somei!")
   print("Somei!")
   a = "dasdas" + 12
   print("Somei!")
except TypeError as Error:
    b = Error
    print(f"Deu ruim na soma de string: {b.with_traceback()}")
except ValueError as Error:
    ...
except ZeroDivisionError as Error:
    ...
except Exception:

    print("Cenario X aconteceu tal coisa > errors bizarros.txt")
else:
    print("Deu bom!")
finally:
    print("Foda-se Tudo")



if (True and False) or (False):
    print()
elif False or True :
    print()

dir()
# Super basicas
int(...)
str(...)
list(...)
set(...)

func_lixo = lambda x: x ** 2

a = map(lambda x: x.split("//")[-1], ["http://....", "https://.....", "http://....."])
a = list(map(lambda x: x.split("//")[-1], ["http://....", "https://.....", "http://....."]))
filtro = filter(lambda x: "https" in x, ["http://....", "https://.....", "http://....."])

#
sorted(map(lambda x: x.split("//")[-1], ["http://....", "https://.....", "http://....."]))

"abcd"[::-1]

any([0,0,0,0,0,0,0,0,])
if not any([a,b,c,d,e])

all([1,1,1,1,0,1,1,1,1,1])

lista_a = [1,2,3,4]

b = lista_a

b.append(5)
lista_a.remove(2)

del b

b = lista_a.copy()
b = lista_a[::]
lista_a[::]

tuplas = (1,2,3,5)

def funcao(ip, url, *args, **kwargs):
    print("Args: ", args)
    print("KWArgs: ", kwargs)
