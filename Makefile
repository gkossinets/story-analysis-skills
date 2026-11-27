# Build upload-ready zips of each skill for claude.ai (Customize -> Skills).
# Each zip has the skill folder as its top level, as the uploader requires.

SKILLS := crews-analysis crews-cards
ZIPS := $(SKILLS:%=dist/%.zip)

.PHONY: zips clean

zips: $(ZIPS)

dist/%.zip: $(shell find $(SKILLS) -type f)
	@mkdir -p dist
	@rm -f $@
	zip -rq $@ $* -x "*.DS_Store" "*/__pycache__/*"

clean:
	rm -rf dist
