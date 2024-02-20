# To use this file you always need to provide the USER.
# E.g.:
# 	make USER=magnus

BASEURL = https://api.chess.com/pub/player
ARCHIVES := $(USER)/archives.json
USER_MKF := $(USER)/Makefile
USER_PKL := $(USER)/games.pickle
USER_EVO := $(USER)/eloevo.png

# The goal of this rule is to save you from having to
# type:
# 	make USER=magnus magnus/archive.json magnus/Makefile
# which is suspicious and prone to error.
default: $(ARCHIVES) $(USER_MKF)
	@echo "$(ARCHIVES) downloadad and $(USER_MKF) generated"

$(ARCHIVES):
	@mkdir -p $(dir $@)
	@wget -q -O $@ $(BASEURL)/$(USER)/games/archives || rm -f $@

# This rule creates a "sub" Makefile for each user
# TODO: should we omit the last month?
$(USER_MKF): $(ARCHIVES)
	@echo -n "MONTHS := " > $@
	@jq -r '.archives[]' $< | cut -d '/' -f 7- | xargs -Ix echo x.pgn | xargs >> $@
	@echo >> $@
	@echo "all: \$$(MONTHS)" >> $@
	@echo >> $@
	@echo "\$$(MONTHS):" >> $@
	@echo -e "\t@mkdir -p \$$(dir \$$@)" >> $@
	@echo -e "\t@echo \$$@" >> $@
	@echo -e "\t@wget -q -O \$$@ $(BASEURL)/$(USER)/\$$(shell echo \$$@ | cut -d. -f 1)/pgn" >> $@


$(USER_PKL): | venv
	$(VENV)/python eloevo.py games2pickle $(USER)

eloevo: $(USER_EVO)

$(USER_EVO): eloevo.py $(USER_PKL) | venv
	$(VENV)/python eloevo.py eloevograph $(USER) $@

# This is handy for telling backup programs to omit the venv dir:
# https://bford.info/cachedir/
$(VENVDIR)/CACHEDIR.TAG: | venv
	@echo Signature: 8a477f597d28d172789f06886806bc55 > $@

cachedirtag: $(VENVDIR)/CACHEDIR.TAG

.PHONY: default eloevo cachedirtag

# This includes Python's venv tools:
include Makefile.venv
