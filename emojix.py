import os, sys

from PyQt4 import QtCore, QtGui

class EmojiLabel(QtGui.QLabel):
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)

    def mouseReleaseEvent(self, event):
        self.emit(QtCore.SIGNAL('clicked()'))

class EmojiFragment(QtGui.QScrollArea):
    def __init__(self, emoji_hook):
        QtGui.QScrollArea.__init__(self)
        self.widget = QtGui.QWidget()
        self.setWidget(self.widget)
        self.setWidgetResizable(True)
        self.setStyleSheet('''QScrollArea{border: none;}''')
        self.widget.setStyleSheet('''QWidget{background: #fff;}''')
        self.emoji = {'people':[], 'food':[], 'nature':[], 'things':[]}
        self.populate()
        self.emoji_hook = emoji_hook

    def populate(self):
        for item in self.emoji:
            path = os.path.join('resources', 'emoji', 'lists', '{}.txt'.format(item))
            with open(path, 'r') as handle:
                self.emoji[item] = [line.strip() for line in handle]

    def get_rows(self, columns, length):
        rows = length/columns
        if length % columns > 0: rows += 1
        return rows

    def ret_code(self, layout, pointer):
        which = self.sender()
        index = layout.indexOf(which)
        fname = self.emoji[pointer][index]
        self.emoji_hook(fname, pointer)

    def load_emoji(self, pointer, cols):
        counter = 0
        length = len(self.emoji[pointer])
        pith = os.path.join('resources', 'emoji', pointer)
        layout = QtGui.QGridLayout(self.widget)
        rows = self.get_rows(cols, length)
        for row in range(rows):
            for column in range(cols):
                path = os.path.join(pith, self.emoji[pointer][counter])
                pixmap = QtGui.QPixmap(path)
                label = EmojiLabel(self)
                label.setPixmap(pixmap)
                label.setStyleSheet('''QLabel::hover{background: #dcdcdc;}''')
                self.connect(label, QtCore.SIGNAL('clicked()'), lambda: self.ret_code(layout, pointer))
                layout.addWidget(label, row, column)
                if counter == length - 1: break
                else: counter += 1

class EmojiWindow(QtGui.QTabWidget):
    def __init__(self, receiver):
        QtGui.QTabWidget.__init__(self)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setStyleSheet('''QTabWidget::tab-bar{alignment: center;}QTabWidget::pane{border: none;}''')
        self.load_emoji(receiver)
        self.setup_tabs()

    def load_emoji(self, receiver):
        self.pfrag = EmojiFragment(receiver)
        self.pfrag.load_emoji('people', 10)
        self.ffrag = EmojiFragment(receiver)
        self.ffrag.load_emoji('food', 10)
        self.nfrag = EmojiFragment(receiver)
        self.nfrag.load_emoji('nature', 10)
        self.tfrag = EmojiFragment(receiver)
        self.tfrag.load_emoji('things', 10)

    def setup_tabs(self):
        path = os.path.join('resources', 'emoji', 'icons')
        self.addTab(self.pfrag, QtGui.QIcon(os.path.join(path, 'people.svg')), '')
        self.addTab(self.ffrag, QtGui.QIcon(os.path.join(path, 'food.svg')), '')
        self.addTab(self.nfrag, QtGui.QIcon(os.path.join(path, 'nature.svg')), '')
        self.addTab(self.tfrag, QtGui.QIcon(os.path.join(path, 'things.svg')), '')
