# webutil.py

from sgmllib import SGMLParser


class WebExtractor(SGMLParser):

    def parse(self, s):
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        SGMLParser.__init__(self, verbose)
        self.hyperlinks = []

    def start_a(self, attributes):
        for name, value in attributes:
            if name == 'href':
                self.hyperlinks.append(value)

    def get_hyperlinks(self):
        return self.hyperlinks
