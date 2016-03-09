"""
An add-on that provides extra functionality for studying Japanese using Anki.

Press 7 to search Jisho.org for the text following ';' in the answer field of the current card.

Press 8 to search Jisho.org for the text in the question field of the current card.
Press 9 to search Jisho for sentences containing the question text.
Press 0 to search Jisho for kanji details for the question text.

Also adds option in context menu to search Jisho for the currently highlighted text.
(I used the 'Search Google Images for selected words' add-on as a starting point: https://ankiweb.net/shared/info/800190862)
"""

SEARCH_URL = 'http://jisho.org/search/%s'
SEARCH_SENTENCES_URL = 'http://jisho.org/search/%s%%20%%23sentences'
SEARCH_KANJI_DETAILS_URL = 'http://jisho.org/search/%s%%20%%23kanji'

from aqt import reviewer, mw
from aqt.webview import AnkiWebView
from aqt.qt import *
from aqt.utils import tooltip
import anki.hooks
import urllib

def keyHandler(self, evt, _old):
    key = unicode(evt.text())
    if key == "7":
        a = mw.reviewer.card.a()
        a_start_index = a.rfind(">") + 1
        answer = a[a_start_index:]
        sentence_start_index = answer.find(";") + 1
        if sentence_start_index <= 0:
            raise Exception('No sample sentence found')
        answer = answer[sentence_start_index:]

        encoded = answer.encode('utf8', 'ignore')
        search = SEARCH_URL
        url = QUrl.fromEncoded(search % (urllib.quote(encoded)))
        QDesktopServices.openUrl(url)

    elif key == "8" or key == "9" or key == "0":
        q = mw.reviewer.card.q()
        q_start_index = q.rfind(">") + 1
        question = q[q_start_index:]
        
        """
        unicode ranges:
        (excludes punctuation)
        hex           dec         character type
        U+4E00-U+9FBF 19968-40895 kanji
        U+3041-U+3096 12353-12438 hiragana
        U+30A1-U+30FA 12449-12538 katakana
        """

        q_end_index = 0
        num = ord(unicode(question[0]))
        while (19968 <= num <= 40895) or (12353 <= num <= 12438) or (12449 <= num <= 12538):
            q_end_index = q_end_index + 1
            if q_end_index >= len(question):
                break
            num = ord(unicode(question[q_end_index]))

        encoded = question[:q_end_index].encode('utf8', 'ignore')
        if key == "8":
          search = SEARCH_URL
        elif key == "9":
          search = SEARCH_SENTENCES_URL
        else:
          search = SEARCH_KANJI_DETAILS_URL
        url = QUrl.fromEncoded(search % (urllib.quote(encoded)))
        QDesktopServices.openUrl(url)

    else:
        return _old(self, evt)

reviewer.Reviewer._keyHandler = anki.hooks.wrap(reviewer.Reviewer._keyHandler, keyHandler, "around")



def selected_text_as_query(web_view):
    sel = web_view.page().selectedText()
    return " ".join(sel.split())

def on_search_for_selection(web_view):
    sel_encode = selected_text_as_query(web_view).encode('utf8', 'ignore')
    #need to do this the long way around to avoid double % encoding
    url = QUrl.fromEncoded(SEARCH_URL % (urllib.quote(sel_encode)))
    QDesktopServices.openUrl(url)


def contextMenuEvent(self, evt):
    # lazy: only run in reviewer
    import aqt
    if aqt.mw.state != "review":
        return
    m = aqt.qt.QMenu(self)
    a = m.addAction(_("Copy"))
    a.connect(a, aqt.qt.SIGNAL("triggered()"),
              lambda: self.triggerPageAction(QWebPage.Copy))
    #Only change is the following statement
    anki.hooks.runHook("AnkiWebView.contextMenuEvent",self,m)
    m.popup(QCursor.pos())

def insert_search_menu_action(anki_web_view,m):
    selected = selected_text_as_query(anki_web_view)
    truncated = (selected[:40] + '..') if len(selected) > 40 else selected
    a = m.addAction('Search for "%s" on Jisho ' % truncated)
    a.connect(a, SIGNAL("triggered()"),
         lambda wv=anki_web_view: on_search_for_selection(wv))


AnkiWebView.contextMenuEvent = contextMenuEvent
anki.hooks.addHook("AnkiWebView.contextMenuEvent", insert_search_menu_action)