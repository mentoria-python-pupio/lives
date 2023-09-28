#!/usr/bin/env python
# pylint: disable=unused-argument, import-error
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.

This Bot uses the Application class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

Note:
To use the JobQueue, you must install PTB via
`pip install "python-telegram-bot[job-queue]"`
"""

import logging
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from desafio_chaos import main as gera_chaos_data_main
from utils import remove_nome_comando

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

dict_comandos_agendados = {}

def add_comando_agendado(funcao):
    return dict_comandos_agendados.setdefault(
        funcao.__name__, funcao
    )

dict_comandos= {}
def add_comando(funcao):
    return dict_comandos.setdefault(
        funcao.__name__, funcao
    )

# Define a few command handlers. These usually take the two arguments update and
# context.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text(
        "Hi! Use /set <seconds> to set a timer\n" \
        "/chaos <n_threads>\n" \
        "/unset_job <comando>\n" \
        "/set_job <comando> <intervalo_minutos> *<args>"


            # await update.effective_message.reply_text("Você deve passar um comando: /set <comando> <intervalo> <*args>")

    )

@add_comando
async def chaos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""

    n_threads = remove_nome_comando(update.message.text)
    
    try:
        n_threads = int(n_threads)
    
        await update.message.reply_text(
            f"Comando recebido! Executado chaos com {n_threads} threads!"
        )
    except ValueError:
        await update.message.reply_text(
            "Uso inadequado, é esperado /chaos <n_threads> para rodar o chaos. n_threads deve ser um numero!"
        )
        return None

    t1 = time.time()

    gera_chaos_data_main(n_threads)

    await update.message.reply_text(
        f"Chaos Executado com sucesso em {(time.time() - t1):.2f}"
    )

# @add_comando
async def show_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """TODO: VERIFICAR SE ISSO É POSSIVEL"""
    job = context.job
    current_jobs = [_job.name for _job in context.job_queue.jobs()]

    context.bot.send_message(
        job.chat_id,
        text="Você tem os seguintes jobs agendados:\n\n" + "\n".join(current_jobs)
    )

@add_comando_agendado
async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")

@add_comando_agendado
async def chaos_update(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""

    job = context.job

    n_threads_default = 40
    if not job.data:
        await context.bot.send_message(f"Job Schedulado NÃO recebeu o n_threads. JOB ESTA SENDO EXECUTADO com {n_threads_default}!!!")
        n_threads = n_threads_default
    else:
        try:
            n_threads = int(job.data[0])
        except ValueError:
            await context.bot.send_message(f"Job Schedulado recebeu o n_threads incompativel '{job.data[0]}' não é um inteiro!. JOB ESTA SENDO EXECUTADO com {n_threads_default}!!!")
            n_threads = n_threads_default
    
    t1 = time.time()

    gera_chaos_data_main(n_threads)

    await context.bot.send_message(
        f"Chaos Executado com sucesso em {(time.time() - t1):.2f}"
    )


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

@add_comando
async def set_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    # Para garantir um aproveitamento em outros grupos e chats sem interferencia nos jobs
    chat_id = update.effective_message.chat_id

    try:
        # args[0] should contain the time for the timer in seconds
        comando = str(context.args[0].strip())
        intervalo = int(context.args[1].strip())
        args = context.args[2:]
        
        if comando not in dict_comandos_agendados.keys():
            await update.effective_message.reply_text(f"Comando '{comando}' inexistente, opcoes disponiveis sao: {str(list(dict_comandos_agendados.keys()))[1:-1]}")
            # await update.effective_message.reply_text("Você deve passar um comando: /set <comando> <intervalo> <*args>")
            return

        job_removed = remove_job_if_exists(str(chat_id)+ "_" + comando, context)
        context.job_queue.run_repeating(dict_comandos_agendados[comando], intervalo*60, chat_id=chat_id, name=str(chat_id)+ "_" + comando, data=args)

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")

@add_comando
async def unset_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    
    try:
        comando = str(context.args[0].strip())
    except IndexError:
        await update.message.reply_text("É necessario passar o nome do comando a ser removido! Ex: /unset_job <comando>")
    
    job_removed = remove_job_if_exists(str(chat_id) + "_" + comando, context)
    text = "Comando successfully cancelled!" if job_removed else "Nenhum comando encontrado."
    await update.message.reply_text(text)

# async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Add a job to the queue."""
#     chat_id = update.effective_message.chat_id
#     try:
#         # args[0] should contain the time for the timer in seconds
#         due = float(context.args[0])
#         if due < 0:
#             await update.effective_message.reply_text("Sorry we can not go back to future!")
#             return

#         job_removed = remove_job_if_exists(str(chat_id), context)
#         context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

#         text = "Timer successfully set!"
#         if job_removed:
#             text += " Old one was removed."
#         await update.effective_message.reply_text(text)

#     except (IndexError, ValueError):
#         await update.effective_message.reply_text("Usage: /set <seconds>")


# async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Remove the job if the user changed their mind."""
#     chat_id = update.message.chat_id
#     job_removed = remove_job_if_exists(str(chat_id), context)
#     text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
#     await update.message.reply_text(text)


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("<SEU TOKEN>").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    # application.add_handler(CommandHandler("set", set_timer))
    # application.add_handler(CommandHandler("unset", unset))
    # application.add_handler(CommandHandler("set_job", set_job))
    # application.add_handler(CommandHandler("unset_job", unset_job))
    # application.add_handler(CommandHandler("chaos", chaos))


    # Define os comandos
    for nome, func in dict_comandos.items():
        application.add_handler(CommandHandler(nome, func))


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()