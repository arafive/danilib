
import os

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

