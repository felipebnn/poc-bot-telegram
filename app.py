import logging
import sqlite3
import sys

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class ConnectionCM:
    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite')

    def __enter__(self):
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.close()

def init_db(token):
    with ConnectionCM() as conn:
        with conn:
            with open('db.sqlite.sql', 'r') as f:
                conn.executescript(f.read())

            conn.execute("INSERT INTO token (token) VALUES (?)", (token,))

def getToken():
    with ConnectionCM() as conn:
        c = conn.cursor()
        c.execute("SELECT (token) FROM token")
        return c.fetchone()[0]

class AgendaDao:
    def insertAgenda(self, user_id, title):
        with ConnectionCM() as conn:
            with conn:
                conn.execute("INSERT INTO agenda (user_id, title) VALUES (?, ?)", (user_id, title))

    def listAgendas(self, user_id):
        with ConnectionCM() as conn:
            c = conn.cursor()
            return [row[0] for row in c.execute("SELECT (title) FROM agenda WHERE user_id=?", (user_id,))]

class Main:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        try:
            self.updater = Updater(token=getToken())
            self.dispatcher = self.updater.dispatcher

            self.dispatcher.add_handler(MessageHandler(Filters.text, self.message))
            self.dispatcher.add_handler(CommandHandler('start', self.start))
            self.dispatcher.add_handler(CommandHandler('new_agenda', self.new_agenda, pass_args=True))
            self.dispatcher.add_handler(CommandHandler('list_agendas', self.list_agendas))
        except sqlite3.OperationalError:
            print("The database was not initialized\n\tRun app.py -init_db TOKEN", file=sys.stderr)
            sys.exit(1)

    def run(self):
        self.updater.start_polling()

    def send_message(self, bot, update, msg):
        bot.send_message(chat_id=update.message.chat_id, text=msg)

    def message(self, bot, update):
        self.send_message(bot, update, update.message.text)

    def start(self, bot, update):
        self.send_message(bot, update, "I'm a bot, please talk to me!")

    def new_agenda(self, bot, update, args):
        user_id = update.message.from_user.id
        title = ' '.join(args)
        try:
            AgendaDao().insertAgenda(user_id, title)

            logging.info('Agenda {} criada por {}'.format(title, user_id))
            self.send_message(bot, update, "Your new agenda is now created!")
        except sqlite3.IntegrityError:
            self.send_message(bot, update, "You already have an agenda with that name!")
        except:
            self.send_message(bot, update, "Unexpected error has occurred...")

    def list_agendas(self, bot, update):
        user_id = update.message.from_user.id

        agendas = AgendaDao().listAgendas(user_id)

        bot.send_message(chat_id=update.message.chat_id, text='Agendas:')
        for agenda in agendas:
            bot.send_message(chat_id=update.message.chat_id, text='-> {}'.format(agenda))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-init_db':
        if len(sys.argv) != 3:
            print("usage: app.py [-init_db key]", file=sys.stderr)
            sys.exit(1)

        init_db(sys.argv[2])
    else:
        Main().run()
