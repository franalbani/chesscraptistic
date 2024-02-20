# chesscraptistic

Tools for scraping all chess.com user games and making statistics

## Instructions

This downloads just the list of available archives:
* `make USER=magnuscarlsen` (will take little time)

This downloads the actual pgn files (it may take a while):
* `make -C magnuscarlsen`

This creates the ELO evolution graph in `magnuscarlsen/eloevo.png`:
* `make USER=magnuscarlsen eloevo`
