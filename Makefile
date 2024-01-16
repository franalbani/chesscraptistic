USERNAME = someuser

BASEURL = https://api.chess.com/pub/player/$(USERNAME)/games

LAST_YEAR_MONTH = $(shell date -d "1 month ago" +%Y-%m)

# FIXME: do not generate unneded months
# FIXME: softcode last month
all: $(shell echo {2020..2023}_{01..12}.pgn)

eloevo.png: venv
	$(VENV)/python -c "from eloevo import eloevograph, load_games; eloevograph(load_games(), '$@')"

%.pgn:
	@wget -O $@ $(BASEURL)/$(shell echo $(@) | cut -d'_' -f 1)/$(shell echo $(@) | cut -d'_' -f 2 | cut -d. -f 1)/pgn


$(VENVDIR)/CACHEDIR.TAG: venv
	@echo Signature: 8a477f597d28d172789f06886806bc55 > $@

clean:
	rm -f *.pgn

.PHONY: all clean test

include Makefile.venv
