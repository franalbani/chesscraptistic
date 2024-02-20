from chess import pgn as pgnlib
from glob import glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List
from datetime import datetime
import pickle
import matplotlib.pyplot as plt
from typer import Typer


app = Typer()


def log(s):
    now = datetime.utcnow()
    print(f'[{now:%H.%M.%S}] {s}')


def read_pgn(pgn_path: Path) -> List[pgnlib.Game]:
    games = []
    with open(pgn_path) as pgn:
        while (game := pgnlib.read_game(pgn)):
            games.append(game)
    return games


def pgns2games(pgn_paths):
    log(f'Processing {len(pgn_paths)} pgns...')

    # with ProcessPoolExecutor(max_workers=8) as executor: # RecursionError
    # This takes a minute...
    with ThreadPoolExecutor(max_workers=8) as executor:
        rs = list(executor.map(read_pgn, pgn_paths))

    games = [dict(g.headers) for r in rs for g in r]
    log(f'Loadad {len(games)} games.')
    return games


def str2date(s):
    return datetime.fromisoformat(s.replace('.', '-'))


@app.command()
def eloevograph(user_path: Path, img_path: Path, show: bool = False):
    games = load_games(user_path)
    # bullet = filter(lambda g: g['TimeControl'] in ['60+1', '60'], games)
    rapid = filter(lambda g: g['TimeControl'] == '600', games)
    user = user_path.as_posix()
    eloevo = sorted(map(lambda g: (str2date(g['EndDate']), int(g['WhiteElo'] if g['White'] == user else g['BlackElo'])), rapid))
    fechas = [d for d, _ in eloevo]
    elo = [e for _, e in eloevo]
    plt.plot(fechas, elo)
    plt.xlabel('Fecha')
    plt.ylabel('ELO')
    plt.title(f'{user_path} Rapid')
    plt.axis([min(fechas), max(fechas), 0, max(elo)*1.1])
    plt.grid()
    if show:
        plt.show()
    plt.savefig(img_path)


def load_games(user_path: Path):
    try:
        with open(user_path / 'games.pickle', 'rb') as p:
            games = pickle.load(p)
        log(f'Loadad {len(games)} games from {user_path}.')
        return games
    except (FileNotFoundError, EOFError):
        log(f'No pickle found for {pickle_path}.')
        games2pickle(user_path)
        return load_games(user_path)


@app.command()
def games2pickle(user_path: Path):
    pgn_paths = list(glob((user_path / 'games/*/*.pgn').as_posix()))
    games = pgns2games(pgn_paths)
    with open(user_path / 'games.pickle', 'wb') as p:
        pickle.dump(games, p)
    log(f'Saved {len(games)} games to {user_path}.')


#    eloevograph(load_games(), '/tmp/eloevo.png', show=True)
app() if __name__ == '__main__' else None
