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
# from Tkinter import * # TODO: figure this out

def keyHandler(self, evt, _old):
    key = unicode(evt.text())
    if key == "8" or key == "9" or key == "0":
        q = aqt.mw.reviewer.card.q()
        start_index = q.rfind(">") + 1
        question = q[start_index:]

        """
        unicode ranges:
        (excludes punctuation)
        hex           dec         character type
        U+4E00-U+9FBF 19968-40895 kanji
        U+3041-U+3096 12353-12438 hiragana
        U+30A1-U+30FA 12449-12538 katakana
        """

        end_index = 0
        num = ord(unicode(question[0]))
        while (19968 <= num <= 40895) or (12353 <= num <= 12438) or (12449 <= num <= 12538):
            end_index = end_index + 1
            if end_index >= len(question):
                break
            num = ord(unicode(question[end_index]))

        encoded = question[:end_index].encode('utf8', 'ignore')
        if key == "8":
        	search = SEARCH_URL
        elif key == "9":
        	search = SEARCH_SENTENCES_URL
        else:
        	search = SEARCH_KANJI_DETAILS_URL
        url = aqt.qt.QUrl.fromEncoded(search % (urllib.quote(encoded)))
        aqt.qt.QDesktopServices.openUrl(url)
    # elif key == "7":
    # 	clipb = Tk()
    # 	q = clipb.selection_get(selection == "CLIPBOARD")
    # 	encoded = q.encode('utf8', 'ignore')
    # 	url = aqt.qt.QUrl.fromEncoded(SEARCH_URL % (urllib.quote(encoded)))
    #     aqt.qt.QDesktopServices.openUrl(url)
    else:
        return _old(self, evt)

aqt.reviewer.Reviewer._keyHandler = anki.hooks.wrap(aqt.reviewer.Reviewer._keyHandler, keyHandler, "around")