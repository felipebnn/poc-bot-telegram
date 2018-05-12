from db import ConnectionCM


class AgendaDao:
    def insertAgenda(self, user_id, title):
        with ConnectionCM() as conn:
            with conn:
                conn.execute("INSERT INTO agenda (user_id, title) VALUES (?, ?)", (user_id, title))

    def listAgendas(self, user_id):
        with ConnectionCM() as conn:
            c = conn.cursor()
            return [row[0] for row in c.execute("SELECT (title) FROM agenda WHERE user_id=?", (user_id,))]
