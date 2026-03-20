
import os

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


