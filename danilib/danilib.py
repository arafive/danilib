
import os
import sys
import logging

import pandas as pd
import xarray as xr
from datetime import timedelta
from typing import Optional, List, Any


def f_buongiorno():
    logger = f_logger()
    logger.info('Buongiorno :)', stacklevel=2)


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
    logger = f_logger()
    os.makedirs(percorso_cartella, exist_ok=True)
    logger.info(f'Creata cartella {percorso_cartella}', stacklevel=2)

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

    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def f_settaggio_db_arpal():
    """
    Ritorna il settaggio per il collegamento al database.

    Returns
    -------
    connessione : cx_Oracle.Connection
        Connessione da passare a pd.read_sql().

    """
    import cx_Oracle
    dsnStr = cx_Oracle.makedsn('cfmi_db.regione.liguria.it', '1522', 'cfmi')
    connessione = cx_Oracle.connect(user='cmi', password='cmi', dsn=dsnStr)
    
    return connessione


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def f_log_ciclo_for(lista_di_liste: List[List[Any]]) -> None:
    """
    Logga lo stato di avanzamento di un ciclo for su più liste.

    Ogni elemento di `lista_di_liste` deve essere una lista di 3 elementi:
        1. Descrizione (str)
        2. Elemento corrente
        3. Lista iterata

    Il messaggio log mostrerà per ogni elemento:
        "{descrizione}{elemento} [posizione_corrente/numero_totale]"  
    separato da ' · '.
    
    Esempio di uso:
        import numpy as np
        a = np.arange(4)
        for i in a:
            f_log_ciclo_for([['a ', i, a]])

        >>> a 0 [1/4]
        >>> a 1 [2/4]
        >>> a 2 [3/4]
        >>> a 3 [4/4]
        
    Parameters
    ----------
    lista_di_liste : List[List[Any]]
        Lista di liste contenenti descrizione, elemento corrente e lista iterata.

    Returns
    -------
    None
    """
    logger = f_logger()
    output_parts = []

    for n, item in enumerate(lista_di_liste, 1):
        if len(item) != 3:
            raise ValueError(f"L'elemento {n} non ha 3 elementi: {item}")

        descrizione, elemento, lista_iterata = item

        # Assicurati che lista_iterata sia realmente una lista
        if not isinstance(lista_iterata, list):
            lista_iterata = list(lista_iterata)

        posizione = lista_iterata.index(elemento) + 1
        totale = len(lista_iterata)

        output_parts.append(f"{descrizione}{elemento} [{posizione}/{totale}]")

    logger.info(" · ".join(output_parts))
    
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    
def f_dataframe_ds_variabili(lista_ds: List[xr.Dataset]) -> pd.DataFrame:
    """
    Costruisce un DataFrame che associa ogni variabile ai suoi attributi e all'indice del dataset di origine.

    Parameters
    ----------
    lista_ds : List[xarray.Dataset]
        Lista di dataset xarray.

    Returns
    -------
    pd.DataFrame
        DataFrame con:
        - index: nome variabile
        - colonne: attributi della variabile + id del dataset
    """
    records = []

    # Costruzione lista (molto più efficiente di concat in loop)
    for i, ds in enumerate(lista_ds):
        for var in ds.data_vars:
            attrs = ds[var].attrs.copy()
            record = {"variabile": var, "id_ds": i, **attrs}
            records.append(record)

    df = pd.DataFrame.from_records(records).set_index("variabile")

    # Rimuove colonne costanti
    df = df.loc[:, df.nunique(dropna=False) > 1]

    # Colonne da rimuovere (solo se esistono)
    colonne_da_rimuovere = [
        "long_name",
        "standard_name",
        "GRIB_cfName",
        "units",
        "GRIB_shortName",
        "GRIB_cfVarName",
    ]
    df = df.drop(columns=[c for c in colonne_da_rimuovere if c in df.columns], errors="ignore")

    # Gestione GRIB_dataType
    if "GRIB_dataType" not in df.columns:
        df["GRIB_dataType"] = "fc"

    return df
