SUBDIRS = LC_MESSAGES

PO_FILES = mousetrap.po

MO_FILES = $(PO_FILES:.po=.mo)

$(MO_FILES): %.mo: %.po
	msgfmt.py -o $@ $<

all: $(MO_FILES)
