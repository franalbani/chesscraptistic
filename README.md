# chesscraptistic

Tools for scraping all chess.com user games and making statistics

## Instructions

This will download just the list of available archives:
* `make USER=magnuscarlsen` (will take little time)

And this will download the actual pgn files and may take a while:
* `make -C magnuscarlsen`

This creates the ELO evolution graph in `magnuscarlsen/eloevo.png`:
* `make USER=magnuscarlsen eloevo`
