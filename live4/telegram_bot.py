import requests
from datetime import datetime
# Necessario criar o bot no BotFather
# Necessario Iniciar o bot com /start (no chat com o proprio bot)
# Se for mandar msg num grupo, adicionar o bot no grupo
TOKEN = "<SEU TOKEN>"
CHAT_ID = "<SEU CHAT>"
lista_chats = [CHAT_ID]

TELEGRAM_URL = "https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML"


def notifica_telegram(msg= str) -> None:
    for chat in lista_chats:
        response = requests.get(
            TELEGRAM_URL.format(
                token=TOKEN,
                chat_id=chat,
                msg=msg
            ), timeout=20
        )
        if not response.status_code == 200:
            print(f"CRITICAL -  MENSAGEM NAO FOI ENVIADA PARA CHAT {chat}!!!")
