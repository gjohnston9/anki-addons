"""
An add-on that provides extra functionality for studying Japanese using Anki.
Press 8 to search Jisho.org for the text in the question field of the current card.
Press 9 to search Jisho for sentences containing the question text.
Press 0 to search Jisho for kanji details for the question text.
"""

SEARCH_URL = 'http://jisho.org/search/%s'
SEARCH_SENTENCES_URL = 'http://jisho.org/search/%s%%20%%23sentences'
SEARCH_KANJI_DETAILS_URL = 'http://jisho.org/search/%s%%20%%23kanji'

import aqt.qt
import anki.hooks
import aqt.reviewer
import urllib

def keyHandler(self, evt, _old):
    key = unicode(evt.text())
    if key == "8" or key == "9" or key == "0":
        q = aqt.mw.reviewer.card.q()
        encoded = q[q.rfind(">") + 1:].encode('utf8', 'ignore') # search term is the portion of card.q() following the last occurrence of ">"
        if key == "8":
        	search = SEARCH_URL
        elif key == "9":
        	search = SEARCH_SENTENCES_URL
        else:
        	search = SEARCH_KANJI_DETAILS_URL
        url = aqt.qt.QUrl.fromEncoded(search % (urllib.quote(encoded)))
        aqt.qt.QDesktopServices.openUrl(url)
    else:
        return _old(self, evt)

aqt.reviewer.Reviewer._keyHandler = anki.hooks.wrap(aqt.reviewer.Reviewer._keyHandler, keyHandler, "around")