import signal
import sys
import argparse
import asyncio

import telebot
from reddit import get_subreddits

# ------------------------------------------------------------------------------
def signal_handler(_, __):
    '''Handles the Ctrl+C in the console so the application can quit elegantly.
    '''
    print('The OciosDoOficio Telegram Bot was stopped.')
    sys.exit(0)

# ------------------------------------------------------------------------------
def _get_reddit_data(subreddits):
    '''Gets the data for the given subreddits.

    Parameters
    ----------
        subreddits (list). List of strings with the subreddits to query.

    Returns
    -------
        text (str). The formatted text with the data queried for the subreddits
        and ready to be sent back to the Telegram via a new (or reply) message.
        Important: This text might be very large, so you should break it up
        into chunks of a maximum length of 3000 bytes in order to send back
        to Telegram without impairing the system.
    '''
    data = asyncio.run(get_subreddits(subreddits))
    text = '=' * 30 + '\n'
    text += 'O QUE "BOMBA" NO REDDIT HOJE' + '\n'
    text += '=' * 30 + '\n'

    for item in data:
        text += f'ASSUNTO: {item["subreddit"]}' + '\n'
        text += '-' * 30 + '\n'
        text += '\n'

        if len(item['threads']) > 0:
            for thread in item['threads']:
                text += f'TÍTULO: {thread["title"]}' + '\n'
                text += f'PONTUAÇÃO: {thread["score"]}' + '\n'
                text += f'URL: {thread["url"]}' + '\n'
                text += f'COMENTÁRIOS: {thread["url_comments"]}' + '\n'
                text += '\n'
        else:
            text += '\tAinda não há threads "bombando" para esse assunto' + '\n'
            text += '\n'

    text += '=' * 30 + '\n'
    return text 

# ------------------------------------------------------------------------------
def main(argv):
    '''Main entry function, called at the beginning of this script.

    Parameters
    ----------
        argv (list). List of string arguments received from the command line.

    Returns
    -------
        status (int). Status code to be returned to the command line. A negative
        value indicates an error, and 0 indicates success.
    '''
    args = parseCommandLine(argv)

    bot = telebot.TeleBot(args.token)

    # Handler of the /start command (simply introduces the bot)
    @bot.message_handler(commands=['start'])
    def welcome_handler(message):
        bot.reply_to(message, 'Olá, eu sou o bot Ócios do Ofício. Nome da hora, '
        'diz aí? hehe Enfim, seja bem vindo(a)!\n\nEu existo pra ajudar quem '
        'está ocioso (eu usava outro termo antes, mas o chefe pediu pra eu ser '
        'mais agradável). Posso ajudar você a se divertir ou a aprender algo de '
        'útil ao invés de ficar aí moscando.\n\nPra começar, você pode usar o '
        'comando /NadaPraFazer, ou arregar e pedir ajuda com o comando /help. '
        'Eu prometo que não julgo (o chefe também pediu pra não fazer mais '
        'isso).')

    # Handler of the /help command (presents the available commands)
    @bot.message_handler(commands=['help'])
    def help_handler(message):
        bot.reply_to(message, 'Assim como você, eu também não tenho nadica de '
        'nada pra fazer. Então, eu vou te ajudar, vai.\nEis o que você pode me '
        'pedir:\n\n/NadaPraFazer algo[;algo mais;outro algo;...] Exibe uma '
        'lista das threads mais bombadas (isto é, com mais de 5 mil pontos) lá '
        'do Reddit no dia de hoje, para as subreddits (nomes ou categorias) que '
        'você informar separadas por ponto-e-vírgula.')

    # Handler of the /NadaPraFazer command (gets top threads for subreddits)
    @bot.message_handler(commands=['NadaPraFazer'])
    def nothing_to_do_handler(message):
        parts = message.text.split()
        if len(parts) > 2:
            bot.reply_to(message, 'Você tentou /help? Esse comando requer '
            'apenas um parâmetro, que é uma lista de '
            'assuntos do Reddit separados por '
            'ponto-e-vírgula. Tenta de novo. Você '
            'consegue!')
            return

        if len(parts) == 1:
            quote =  'Mesmo sem nada pra fazer, você tem preguiça até mesmo de '
            quote += 'digitar um nome de algo que te interessa. Ok, como eu gosto '
            quote += 'de gatos, segue aí as threads "bombando" no Reddit no último '
            quote += 'dia para o tema "cats":\n\n'
            subreddits = ['cats']
        else:
            quote =  'Eis as threads "bombando" no Reddit no último dia, para os '
            quote += 'assuntos que você pediu:\n\n'
            subreddits = parts[1].split(';')
        
        whole_text = quote + _get_reddit_data(subreddits)

        # Split the message text in blocks of 3000 characters (so Telegram can
        # properly handle it)
        splitted_text = telebot.util.split_string(whole_text, 3000)
        for text in splitted_text:
            bot.send_message(message.chat.id, text)

    # Handler of the all other commands (presents feedback on error)
    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def command_default(message):
        parts = message.text.split()
        if parts[0].upper() == '/NADAPRAFAZER':
            rest = ' '.join([p for i, p in enumerate(parts) if i > 0])
            bot.send_message(message.chat.id, f'Você quis dizer /NadaPraFazer {rest}?')
        else:
            bot.send_message(message.chat.id, 'Cuma? Não entendi. Tente a ajuda '
            'em /help.')

    signal.signal(signal.SIGINT, signal_handler)
    print('The OciosDoOficio Telegram bot server is started.')
    print('Press Ctrl+C to stop.')

    bot.polling()
    return 0

#---------------------------------------------
def parseCommandLine(argv):
    '''Parses the command line of this script.
    This function uses the argparse package to handle the command line
    arguments. In case of command line errors, the application will be
    automatically terminated.

    Parameters
    ----------
        argv (list). List of strings with the arguments received from the 
        command line.

    Returns
    -------
        args (object). Object with the parsed arguments as attributes
        (refer to the documentation of the argparse package for details).
    '''
    parser = argparse.ArgumentParser(description='Implementation of the '
    'Telegram Bot named @OciosDoOficioBot. Created by Luiz C. Vieira for the '
    'IDWall Challenge (2018).')

    parser.add_argument('-t', '--token', metavar='digits',
    help='The token created by the @BotFather and used to command the '
    'OciosDoOficioBot bot.', required=True)

    args = parser.parse_args()

    return args

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))