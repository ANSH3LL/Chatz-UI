import os, re
from PyQt4 import QtGui, QtCore

class ButtonLineEdit(QtGui.QLineEdit):
    buttonClicked = QtCore.pyqtSignal(bool)
    def __init__(self, icon_file, parent = None):
        super(ButtonLineEdit, self).__init__(parent)

        self.button = QtGui.QToolButton(self)
        self.button.setIcon(QtGui.QIcon(icon_file))
        self.button.setToolTip('Go')
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.buttonClicked.emit)

        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.setStyleSheet('.QLineEdit {padding-right: %dpx;}' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth*2 + 2),
                            max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth*2 + 2))

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),
                         (self.rect().bottom() - buttonSize.height() + 1)/2)
        super(ButtonLineEdit, self).resizeEvent(event)

class UserCard(QtGui.QFrame):
    def __init__(self, name_hook):
        QtGui.QFrame.__init__(self)
        self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setFixedSize(233, 90)
        self.__style_me()
        self.setLayout(self.layout)
        self.name_hook = name_hook

    def mouseReleaseEvent(self, event):
        self.name_hook(self.alias)

    def __style_me(self):
        self.setStyleSheet('UserCard{border-radius: 10px; background-color: #dadada;}UserCard::hover{background-color: #a0a0a0;}')

    def blink(self):
        self.setStyleSheet('UserCard{border-radius: 10px; background-color: #a0a0a0;}')
        QtCore.QTimer.singleShot(150, self.__style_me)

    def render(self, alias, lastseen, access):
        self.alias = alias
        self.setToolTip('{0} >> {1}'.format(alias, access))
        layout2 = QtGui.QHBoxLayout()
        layout2.setContentsMargins(10, 10, 0, 0)
        layout2.setSpacing(0)
        layout3 = QtGui.QHBoxLayout()
        layout3.setContentsMargins(0, 0, 10, 10)
        layout3.setSpacing(0)
        frame1 = QtGui.QFrame()
        frame1.setLayout(layout2)
        self.layout.addWidget(frame1)
        frame2 = QtGui.QFrame()
        frame2.setLayout(layout3)
        self.layout.addWidget(frame2, alignment = QtCore.Qt.AlignRight)
        self.piclabel = QtGui.QLabel()
        self.piclabel.setText(alias[0])
        self.piclabel.setAlignment(QtCore.Qt.AlignCenter)
        self.piclabel.setFixedSize(50, 50)
        self.piclabel.setStyleSheet('border-radius: 25px; background-color: #f092de; font-size: 20px;')
        layout2.addWidget(self.piclabel)
        self.namelabel = QtGui.QLabel(alias)
        if access == 1:
            self.namelabel.setStyleSheet('font-size: 20px; margin-left: 3px; color: #0f9000;')
        elif access == 2:
            self.namelabel.setStyleSheet('font-size: 20px; margin-left: 3px; color: #0020ff;')
        else:
            self.namelabel.setStyleSheet('font-size: 20px; margin-left: 3px;')
        layout2.addWidget(self.namelabel)
        self.seenlabel = QtGui.QLabel()
        self.seenlabel.setFixedSize(16, 16)
        if lastseen == 'Online':
            self.seenlabel.setStyleSheet('border-radius: 8px; background-color: #00f700;')
        else:
            self.seenlabel.setStyleSheet('border-radius: 8px; background-color: #fd0000;')
        layout3.addWidget(self.seenlabel)
        self.timelabel = QtGui.QLabel(lastseen)
        self.timelabel.setStyleSheet('font-size: 15px; margin-left: 1px;')
        layout3.addWidget(self.timelabel)

class Bubble(QtGui.QFrame):
    def __init__(self):
        QtGui.QFrame.__init__(self)
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.define_styles()

    def define_styles(self):
        self.sent = '''
        Bubble{
            border: 2px solid #08b7ff;
            border-top-right-radius: 10px;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
            background-color: rgba(54, 183, 190, 200)
        }
        '''
        self.received = '''
        Bubble{
            border: 2px solid #02dfa5;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            border-bottom-left-radius: 10px;
            background-color: rgba(0, 191, 165, 200)
        }
        '''
        self.status = '''
        Bubble{
            border: 2px solid #91b7b0;
            border-top-right-radius: 10px;
            border-top-left-radius: 10px;
            border-bottom-right-radius: 10px;
            border-bottom-left-radius: 10px;
            background-color: rgba(145, 163, 176, 200)
        }
        '''

    def adjust(self, message):
        length = len(message)
        emoji = re.findall(r'<img[^>]+.*?>', message)
        if emoji:
            ln = 0
            weight = len(emoji) * 5
            for em in emoji: ln += len(em)
            length -= ln
            length += weight
        self.mlabel.setMaximumWidth(600)
        if re.match(r'<img[^>]+title.*?>', message): pass
        elif length > 50: self.mlabel.setMinimumWidth(500)
        elif length > 40: self.mlabel.setMinimumWidth(400)
        elif length > 30: self.mlabel.setMinimumWidth(300)
        elif length > 20: self.mlabel.setMinimumWidth(200)
        elif length > 10: self.mlabel.setMinimumWidth(100)
        else: pass

    def createR(self, sender, message, time):
        self.style = 'received'
        self.slabel = QtGui.QLabel()
        self.slabel.setAlignment(QtCore.Qt.AlignLeft)
        self.slabel.setText(sender)
        self.slabel.setStyleSheet('font-size: 13px;')
        self.layout.addWidget(self.slabel)

        self.mlabel = QtGui.QLabel()
        self.mlabel.setWordWrap(True)
        self.mlabel.setText(message)
        self.mlabel.setStyleSheet('font-size: 14px;')
        self.adjust(message)
        self.layout.addWidget(self.mlabel)

        self.tlabel = QtGui.QLabel()
        self.tlabel.setAlignment(QtCore.Qt.AlignRight)
        self.tlabel.setText(time)
        self.tlabel.setStyleSheet('font-size: 11px;')
        self.layout.addWidget(self.tlabel)
        self.align = QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft

    def createS(self, message, time):
        self.style = 'sent'
        self.mlabel = QtGui.QLabel()
        self.mlabel.setWordWrap(True)
        self.mlabel.setText(message)
        self.mlabel.setStyleSheet('font-size: 14px;')
        self.adjust(message)
        self.layout.addWidget(self.mlabel)

        self.tlabel = QtGui.QLabel()
        self.tlabel.setAlignment(QtCore.Qt.AlignRight)
        self.tlabel.setText(time)
        self.tlabel.setStyleSheet('font-size: 11px;')
        self.layout.addWidget(self.tlabel)
        self.align = QtCore.Qt.AlignTop|QtCore.Qt.AlignRight

    def createT(self, message):
        self.style = 'status'
        self.mlabel = QtGui.QLabel()
        self.mlabel.setWordWrap(True)
        self.mlabel.setText(message)
        self.mlabel.setStyleSheet('font-size: 14px;')
        self.adjust(message)
        self.layout.addWidget(self.mlabel)
        self.align = QtCore.Qt.AlignTop|QtCore.Qt.AlignCenter

    def set_style(self):
        if self.style == 'sent': selected = self.sent
        elif self.style == 'received': selected = self.received
        elif self.style == 'status': selected = self.status
        else: return None
        self.setStyleSheet(selected)

    def render(self, *args):
        if len(args) == 1: self.createT(args[0])
        elif len(args) == 2: self.createS(args[0], args[1])
        elif len(args) == 3: self.createR(args[0], args[1], args[2])
        else: return None
        self.set_style()
        self.setFixedSize(self.layout.sizeHint())

class ChatFragment(QtGui.QScrollArea):
    def __init__(self):
        QtGui.QScrollArea.__init__(self)
        self.widget = QtGui.QWidget()
        self.setWidget(self.widget)
        self.setWidgetResizable(True)
        self.layout = QtGui.QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.verticalScrollBar().rangeChanged.connect(self.scroll_down)
        self.widget.setStyleSheet('.QWidget{background-image: url(resources/images/background.svg); background-repeat: repeat-xy; background-color: #dfdbe5;}')

    @QtCore.pyqtSlot(int, int)
    def scroll_down(self, minimum, maximum):
        self.verticalScrollBar().setSliderPosition(maximum)

class ChatTab(QtGui.QTabWidget):
    def __init__(self):
        QtGui.QTabWidget.__init__(self)
        self.setStyleSheet('''QTabWidget::tab-bar{alignment: center;}QTabWidget::pane{border: none;}''')
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.del_chat)
        self.chats = {}
        self.new_chat('Group')

    def new_chat(self, alias):
        if alias in self.chats: pass
        else:
            chatwin = ChatFragment()
            self.chats[alias] = chatwin
            self.addTab(chatwin, alias)
        self.setCurrentIndex(self.indexOf(self.chats[alias]))

    def del_chat(self, index):
        alias = str(self.tabText(index))
        if alias in self.chats and alias != 'Group':
            self.widget(index).deleteLater()
            self.removeTab(index)
            del(self.chats[alias])
        else:
            print 'cannot close tab number {0}: {1}'.format(index, alias)

    def get_chat(self):
        return str(self.tabText(self.currentIndex()))

class AuthForm(QtGui.QFrame):
    def __init__(self, cred_hook):
        QtGui.QFrame.__init__(self)
        self.setStyleSheet('AuthForm{background-color: #d3d3d3;}')
        self.create_layout()
        self.create_frames()
        self.create_elements()
        self.create_elements2()
        self.cred_hook = cred_hook

    def create_layout(self):
        self.main_ly = QtGui.QVBoxLayout()
        self.sign_in_ly = QtGui.QFormLayout()
        self.sign_up_ly = QtGui.QFormLayout()
        self.logo_ly = QtGui.QVBoxLayout()
        self.sizer_ly = QtGui.QVBoxLayout()

    def create_frames(self):
        self.setLayout(self.main_ly)
        self.sign_in_fr = QtGui.QFrame()
        self.sign_in_fr.setLayout(self.sign_in_ly)
        self.sign_in_fr.setStyleSheet('.QFrame{background-color: #303030;}')
        self.sign_up_fr = QtGui.QFrame()
        self.sign_up_fr.setLayout(self.sign_up_ly)
        self.sign_up_fr.setStyleSheet('.QFrame{background-color: #303030;}')
        self.logo_fr = QtGui.QFrame()
        self.logo_fr.setLayout(self.logo_ly)
        self.sizer_fr = QtGui.QFrame()
        self.sizer_fr.setFixedHeight(490)
        self.sizer_fr.setLayout(self.sizer_ly)
        limage = QtGui.QLabel()
        limage.setPixmap(QtGui.QIcon(os.path.join('resources', 'images', 'chat.svg')).pixmap(QtCore.QSize(64, 64)))
        self.logo_ly.addWidget(limage)
        ltext = QtGui.QLabel('Chatz')
        ltext.setStyleSheet('font-size: 22px;')
        self.logo_ly.addWidget(ltext)
        self.tab_fr = QtGui.QTabWidget()
        self.tab_fr.setFixedSize(330, 314)
        self.tab_fr.addTab(self.sign_in_fr, 'Sign In')
        self.tab_fr.addTab(self.sign_up_fr, 'Sign Up')
        self.tab_fr.setStyleSheet('''QTabBar::tab{color: #f1f1f1; width: 165px; height: 28px; font-size: 22px;}QTabBar::tab:!selected{background-color: #202020;}
                                     QTabBar::tab:selected{background-color: #3a6ff0;}QTabWidget::pane{border: none;}''')
        self.sizer_ly.addWidget(self.tab_fr, alignment = QtCore.Qt.AlignTop)
        self.main_ly.addWidget(self.logo_fr, alignment = QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter)
        self.main_ly.addWidget(self.sizer_fr, alignment = QtCore.Qt.AlignCenter)

    def create_elements(self):
        sidlbl = QtGui.QLabel('Connect URL')
        sidlbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.sid = QtGui.QLineEdit()
        self.sid.setPlaceholderText('srv.haloserver.io:10950')
        self.sid.setStyleSheet('font-size: 15px;')
        self.sign_in_ly.addRow(sidlbl)
        self.sign_in_ly.addRow(self.sid)
        alslbl = QtGui.QLabel('Username')
        alslbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.als = QtGui.QLineEdit()
        self.als.setPlaceholderText('John.Doe')
        self.als.setStyleSheet('font-size: 15px;')
        self.sign_in_ly.addRow(alslbl)
        self.sign_in_ly.addRow(self.als)
        psslbl = QtGui.QLabel('Password')
        psslbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.pss = QtGui.QLineEdit()
        self.pss.setPlaceholderText('p4ssw0rd!')
        self.pss.setEchoMode(QtGui.QLineEdit.Password)
        self.pss.returnPressed.connect(self.signin)
        self.pss.setStyleSheet('font-size: 15px;')
        self.sign_in_ly.addRow(psslbl)
        self.sign_in_ly.addRow(self.pss)
        spc = QtGui.QLabel('')
        self.sign_in_ly.addRow(spc)
        self.sbm = QtGui.QPushButton('Connect And Sign In')
        self.sbm.setFixedHeight(35)
        self.sbm.setDefault(True)
        self.sbm.setStyleSheet('font-size: 15px;')
        self.sbm.clicked.connect(self.signin)
        self.sign_in_ly.addRow(self.sbm)

    def create_elements2(self):
        sidlbl = QtGui.QLabel('Connect URL')
        sidlbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.sid2 = QtGui.QLineEdit()
        self.sid2.setPlaceholderText('srv.haloserver.io:10950')
        self.sid2.setStyleSheet('font-size: 15px;')
        self.sign_up_ly.addRow(sidlbl)
        self.sign_up_ly.addRow(self.sid2)
        alslbl = QtGui.QLabel('Username')
        alslbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.als2 = QtGui.QLineEdit()
        self.als2.setPlaceholderText('John.Doe')
        self.als2.setStyleSheet('font-size: 15px;')
        self.sign_up_ly.addRow(alslbl)
        self.sign_up_ly.addRow(self.als2)
        psslbl = QtGui.QLabel('Password')
        psslbl.setStyleSheet('font-size: 15px; color: #f1f1f1;')
        self.pss2 = QtGui.QLineEdit()
        self.pss2.setPlaceholderText('p4ssw0rd!')
        self.pss2.setEchoMode(QtGui.QLineEdit.Password)
        self.pss2.returnPressed.connect(self.signup)
        self.pss2.setStyleSheet('font-size: 15px;')
        self.sign_up_ly.addRow(psslbl)
        self.sign_up_ly.addRow(self.pss2)
        spc = QtGui.QLabel('')
        self.sign_up_ly.addRow(spc)
        self.sbm2 = QtGui.QPushButton('Connect And Sign Up')
        self.sbm2.setFixedHeight(35)
        self.sbm2.setDefault(True)
        self.sbm2.setStyleSheet('font-size: 15px;')
        self.sbm2.clicked.connect(self.signup)
        self.sign_up_ly.addRow(self.sbm2)

    def signin(self):
        server = str(self.sid.text())
        uname = str(self.als.text())
        passwd = str(self.pss.text())
        creds = (server, uname, passwd)
        self.cred_hook(creds)

    def signup(self):
        server = str(self.sid2.text())
        uname = str(self.als2.text())
        passwd = str(self.pss2.text())
        creds = (server, uname, passwd)
        self.cred_hook(creds)
