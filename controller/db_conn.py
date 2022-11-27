import sqlite3


class DbConn(object):

    def __init__(self):
        super(DbConn, self).__init__()
        self.con = sqlite3.connect("datubase.db")  # konexioa ezarri
        self.cur = self.con.cursor()

        # "JOKALARIAK" Taula sortu:
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS JOKALARIAK(erabiltzailea, galdera, erantzuna, pasahitza, puntuazioa, partida, soinua, atzeko, botoiKol, paleta)")

        # "admin" erabiltzailea sortu eta taulan sartu:
        erabiltzaile_izena = "admin"
        query = self.cur.execute("SELECT * FROM JOKALARIAK WHERE erabiltzailea=(?)", (erabiltzaile_izena,))
        if query.fetchone() is None:
            galdera = "XXX"
            erantzuna = "XXX"
            pasahitza = "123"
            puntuazioa = "0"
            partida = "#"
            musika = "original"
            atzeko = "#7ec0ee"
            botoiKol = "#ffffff"
            paleta = 1
            self.cur.execute("INSERT INTO JOKALARIAK VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            erabiltzaile_izena, galdera, erantzuna, pasahitza, puntuazioa, partida, musika, atzeko, botoiKol, paleta))
            self.con.commit()

    def erabiltzailearen_pasahitza_lortu(self, id_erabiltzaile):
        res = self.cur.execute("SELECT pasahitza FROM JOKALARIAK WHERE erabiltzailea=(?)", (id_erabiltzaile,))
        pasahitza = res.fetchone()
        if pasahitza is None:
            return pasahitza
        else:
            return pasahitza[0]

    def erabiltzailea_idz_lortu(self, id_erabiltzaile):
        res = self.cur.execute("SELECT erabiltzailea FROM JOKALARIAK WHERE erabiltzailea=(?)", (id_erabiltzaile,))
        return res.fetchone()

    def erabiltzaile_berria_erregistratu(self, id_erabiltzaile, galdera, erantzuna, pasahitza, puntuazioa, partida,
                                         musika, atzeko, botoiKol, paleta):
        self.cur.execute("INSERT INTO JOKALARIAK VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (id_erabiltzaile, galdera, erantzuna, pasahitza, puntuazioa, partida, musika, atzeko, botoiKol, paleta))
        self.con.commit()  # Datu basean insert-aren commit-a egiten da

    def partida_gorde(self, id_erabiltzaile, partida, puntuazioa):
        self.cur.execute("UPDATE JOKALARIAK SET partida=(?), puntuazioa=(?) WHERE erabiltzailea=(?)",
                         (partida, puntuazioa, id_erabiltzaile))
        self.con.commit()

    def partida_kargatuta(self, id_erabiltzaile):
        res = self.cur.execute("SELECT partida FROM JOKALARIAK WHERE erabiltzailea=(?)", (id_erabiltzaile,))
        return res.fetchone()[0]

    def puntuazioa_lortu(self, id_erabiltzaile):
        res = self.cur.execute("SELECT puntuazioa FROM JOKALARIAK WHERE erabiltzailea=(?)", (id_erabiltzaile,))
        return res.fetchone()[0]

    def erabiltzaile_guztiak_lortu(self):
        return self.cur.execute("SELECT erabiltzailea FROM jokalariak").fetchall()

    def erabiltzaile_ezabatu(self, id_erabiltzaile):
        self.cur.execute("DELETE FROM jokalariak WHERE erabiltzailea=(?)", (id_erabiltzaile,))
        self.con.commit()

    def pasahitza_aldatu(self, id_erabiltzaile, pasahitza, galdera, erantzuna):
        self.cur.execute("UPDATE JOKALARIAK SET pasahitza=(?) WHERE erabiltzailea=(?)", (pasahitza, id_erabiltzaile,))
        self.cur.execute("UPDATE JOKALARIAK SET galdera=(?) WHERE erabiltzailea=(?)", (galdera, id_erabiltzaile,))
        self.cur.execute("UPDATE JOKALARIAK SET erantzuna=(?) WHERE erabiltzailea=(?)", (erantzuna, id_erabiltzaile,))
        self.con.commit()

    def galdera_lortu(self, id_erabiltzaile):
        res = self.cur.execute("SELECT galdera FROM JOKALARIAK WHERE erabiltzailea=(?)", (id_erabiltzaile,))
        return res.fetchone()[0]

    def erantzuna_ondo_dago(self, id_erabiltzaile, erantzuna):
        res = self.cur.execute("SELECT erantzuna FROM JOKALARIAK WHERE erabiltzailea=(?)", (id_erabiltzaile,))
        erantzun_zuzen = res.fetchone()[0]
        if (erantzun_zuzen.__eq__(erantzuna)):
            return True
        return False

    def pertsonalizazioa_aldatu(self, atzeko, adreilu, botoi, musika, erabiltzaile):
        # EZ BADA EZER ALDATU NAHI PARAMETROREN BATEAN EZ DIRA UPDATE-AK EGIN BEHAR -> if X is not None
        if musika is not None:
            self.cur.execute("UPDATE JOKALARIAK SET soinua=(?) WHERE erabiltzailea=(?)", (musika, erabiltzaile,))

        if atzeko is not None:
            self.cur.execute("UPDATE JOKALARIAK SET atzeko=(?) WHERE erabiltzailea=(?)", (atzeko, erabiltzaile,))

        if botoi is not None:
            self.cur.execute("UPDATE JOKALARIAK SET botoiKol=(?) WHERE erabiltzailea=(?)", (botoi, erabiltzaile,))

        if adreilu is not None:
            self.cur.execute("UPDATE JOKALARIAK SET paleta=(?) WHERE erabiltzailea=(?)", (adreilu, erabiltzaile,))

        self.con.commit()

    def get_jokalari_musika(self, erabiltzaile):
        if erabiltzaile is not None:
            emaitza = self.cur.execute("SELECT soinua FROM JOKALARIAK WHERE erabiltzailea=(?)", (erabiltzaile,))
            return emaitza.fetchone()[0]
        return "ez"

    def get_jokalari_fondoa(self, erabiltzaile):
        if erabiltzaile is not None:
            fondo = self.cur.execute("SELECT atzeko FROM JOKALARIAK WHERE erabiltzailea=(?)", (erabiltzaile,))
            #botKol = self.cur.execute("SELECT botoiKol FROM JOKALARIAK WHERE erabiltzailea=(?)", (erabiltzaile,))
            return fondo.fetchone()[0]
        return "#7ec0ee"

    def get_jokalari_botoi_kolor(self, erabiltzaile):
        if erabiltzaile is not None:
            botoi_kolor = self.cur.execute("SELECT botoiKol FROM JOKALARIAK WHERE erabiltzailea=(?)", (erabiltzaile,))
            return botoi_kolor.fetchone()[0]
        return "#ffffff"

    def paleta_lortu(self, erabiltzaile):
        if erabiltzaile is not None:
            print("paleta hartzera")
            emaitza = self.cur.execute("SELECT paleta FROM JOKALARIAK WHERE erabiltzailea=(?)", (erabiltzaile,))
            e = emaitza.fetchone()[0]
            print(e)
            return e
        else:
            print("Bat")
            return 1

    def konexioa_itxi(self):
        self.con.close()
