# chesscraptistic

Tools for scraping all chess.com user games and making statistics

## Instructions

This will download just the list of available archives:
* `make USER=magnuscarlsen` (will take little time)

And this will download the actual pgn files and may take a while:
* `make -C magnuscarlsen`

This creates a pickle with all the games:
* `make USER=magnuscarlsen magnuscarlsen/games.pickle`
    * This will be improved

This creates the ELO evolution graph:
* `make USER=magnuscarlsen magnuscarlsen/eloevo.png`
    * This will be improved
