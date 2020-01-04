import os
from HTMLParser import HTMLParser

class TextParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._pretty = ''
        self._textout = ''
        self.paragraph = False

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for x in attrs:
                if x[0] == 'src':
                    self._pretty += '<img src="{}" />'.format(x[1])
                    self._textout += ':{}:'.format(x[1].split(os.path.sep)[-1].split('.')[0])
        elif tag == 'p':
            self.paragraph = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self._pretty += '\n'
            self._textout += '\n'
            self.paragraph = False

    def handle_data(self, data):
        if self.paragraph:
            self._pretty += data
            self._textout += data

    def produce(self):
        temp = self._textout.strip()
        temp2 = self._pretty.strip()
        self._pretty = ''
        self._textout = ''
        return temp, temp2
