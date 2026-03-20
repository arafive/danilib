
import os
import sys
import logging

from datetime import timedelta
from typing import Optional


def f_buongiorno():
    print('Buongiorno :)')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def f_crea_cartella(percorso_cartella: str):
    """
    Crea una cartella, printa per conferma e ritorna il percorso passato.

    Parameters
    ----------
    percorso_cartella : str
        Percorso della cartella da creare.

    Returns
    -------
    percorso_cartella : str
        Percorso della cartella creata.

    """
    os.makedirs(percorso_cartella, exist_ok=True)
    print(f'Creata cartella {percorso_cartella}')

    return percorso_cartella

    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def f_printa_tempo_trascorso(
        t_inizio: float,
        t_fine: float,
        nota: Optional[str] = None
        ) -> str:
    """
    Calcola e formatta il tempo trascorso tra due istanti.

    Parameters
    ----------
    t_inizio : float
        Tempo iniziale (es. time.time()).
    t_fine : float
        Tempo finale.
    nota : str, optional
        Testo opzionale da aggiungere al messaggio.

    Returns
    -------
    str
        Stringa formattata del tempo trascorso.
    """
    elapsed_tempo = timedelta(seconds=t_fine - t_inizio)
    
    giorni = f'{elapsed_tempo.days:01}'
    ore = f'{elapsed_tempo.seconds//3600:02}'
    minuti = f'{elapsed_tempo.seconds//60%60:02}'
    secondi = f'{elapsed_tempo.seconds%60:02}'
    millisecondi = elapsed_tempo.microseconds / 1000
    
    msg = f'{int(secondi)}.{int(millisecondi)} sec'
    
    if int(minuti) > 0:
        msg = f'{minuti}:{secondi} min'
    
    if int(ore) > 0:
        msg = f'{ore}:{minuti}:{secondi} ore'
    
    if int(giorni) > 0:
        if int(giorni) == 1:
            msg = f'{giorni} giorno, {ore}:{minuti}:{secondi} ore'
        else:
            msg = f'{giorni} giorni, {ore}:{minuti}:{secondi} ore'
    
    if nota:
        msg = f'{nota}: {msg}'
        
    return msg

    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt: str, level_width: int = 8):
        super().__init__(fmt)
        self.fmt = fmt
        self.level_width = level_width

        self.reset = '\033[0m'
        self.colors = {
            logging.DEBUG: '\033[3;36m',
            logging.INFO: '\033[32m',
            logging.WARNING: '\033[5;33m',
            logging.ERROR: '\033[1;31m',
            logging.CRITICAL: '\033[35m',
        }

    def format(self, record):
        color = self.colors.get(record.levelno, '')
        original = record.levelname

        aligned = f"{original:<{self.level_width}}"
        record.levelname = f"{color}{aligned}{self.reset}"

        formatter = logging.Formatter(self.fmt)
        result = formatter.format(record)

        record.levelname = original
        return result


def f_logger(level: int = logging.INFO) -> logging.Logger:
    """
    Crea e configura un logger con output colorato su terminale.

    Parameters
    ----------
    level : int
        Livello di logging (es. logging.DEBUG).

    Returns
    -------
    logging.Logger
    """
    logger = logging.getLogger("mio_logger")

    # Evita duplicazione handler se chiamata più volte
    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    level_width = 8
    fmt = f"%(asctime)s  %(levelname)-{level_width}s  %(filename)s:%(lineno)s  %(message)s"

    if sys.stdout.isatty():
        handler = logging.StreamHandler()
        handler.setFormatter(ColorFormatter(fmt, level_width))
    else:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))

    handler.setLevel(level)
    logger.addHandler(handler)

    return logger


































