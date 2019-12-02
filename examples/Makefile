# Makefile for iptable

# utilities
RM=/bin/rm
PANDOC=/usr/bin/pandoc
FILTER=../pandoc_imagine.py
DEFAULTS=defaults.yaml

INPFILES:= $(sort $(wildcard *.md))
DEMOS:= $(INPFILES:%.md=%)

.PHONY: clean help all

help:
	@echo "make all        -- builds all pdf's"
	@echo "make clean      -- removes all pdf's"
	@echo "make <name>     -- build <name>.pdf"
	@echo "possible <name>'s:"
	@echo $(foreach DEMO, $(DEMOS), "\n - $(DEMO)")
	@echo ""

all: $(DEMOS) $(DEFAULTS)

$(DEMOS): $(DEFAULTS)
	@echo "\n---------  $@  ---------"
	$(PANDOC) --filter $(FILTER) $@.md $(DEFAULTS) -o $@.pdf
	@echo ""

clean:
	@$(RM) -f *.pdf
	@echo "removed all pdf's"

purge:
	@$(RM) -f *.pdf
	@$(RM) -rf pd-images
	@echo "removed all PDF's and pd-images subdir"
