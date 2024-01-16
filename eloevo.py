from chess import pgn as pgnlib
from glob import glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List
from datetime import datetime
import pickle
import matplotlib.pyplot as plt


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


def eloevograph(games, img_path: Path, user, show: bool = False):
    rapid = filter(lambda g: g['TimeControl'] == '600', games)
    eloevo = sorted(map(lambda g: (str2date(g['EndDate']), int(g['WhiteElo'] if g['White'] == user else g['BlackElo'])), rapid))
    plt.plot([d for d, _ in eloevo], [e for _, e in eloevo])
    plt.grid()
    if show:
        plt.show()
    plt.savefig(img_path)


def load_games(pickle_path: Path = 'games.pickle'):
    try:
        with open(pickle_path, 'rb') as f:
            games = pickle.load(f)
        log(f'Loadad {len(games)} games from {pickle_path}.')
    except (FileNotFoundError, EOFError):
        log(f'No pickle found.')
        pgn_paths = list(glob('*.pgn'))
        games = pgns2games(pgn_paths)
        with open(pickle_path, 'wb') as f:
            pickle.dump(games, f)
        log(f'Saved {len(games)} games to {pickle_path}.')
    return games

if __name__ == '__main__':
    eloevograph(load_games(), '/tmp/eloevo.png', show=True)
