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
        search = (SEARCH_URL * (key == "8")) + (SEARCH_SENTENCES_URL * (key == "9")) + (SEARCH_KANJI_DETAILS_URL * (key == "0"))
        url = aqt.qt.QUrl.fromEncoded(search % (urllib.quote(encoded)))
        aqt.qt.QDesktopServices.openUrl(url)
    else:
        return _old(self, evt)

aqt.reviewer.Reviewer._keyHandler = anki.hooks.wrap(aqt.reviewer.Reviewer._keyHandler, keyHandler, "around")