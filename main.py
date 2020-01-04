import re, os, sys

import emoji
from PyQt4 import QtGui, QtCore

import emojix, tparser, elements

test1 = '''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been\
the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of\
type and scrambled it to make a type specimen book.'''
test2 = '''It is a long established fact that a reader will be distracted by the readable content of a page\
when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal\
distribution of letters, as opposed to using 'Content here, content here', making it look like readable English.'''
test3 = '''Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin\
literature from 45 BC, making it over 2000 years old.'''

class UIHandler(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Chatz')
        self.setMinimumSize(1000, 600)
        self.setWindowIcon(QtGui.QIcon(os.path.join('resources', 'images', 'chat.svg')))
        self.parser = tparser.TextParser()
        self.emoprovider = emojix.EmojiWindow(self.emojislot)
        self.userlist = ['Cagney.Carnation', 'Djimmi.The.Great', 'Baroness.Von.Bonbon', 'Grimm.MatchStick',
                         'King.Dice', 'Hilda.Berg', 'Wally.Warbles', 'Carla.Maria', 'Dr.Kahl']
        self.setCentralWidget(elements.AuthForm(self.credslot))

    def setup_ui(self):
        self.create_layouts()
        self.create_containers()
        self.create_containers2()
        self.create_elements()
        self.create_elements2()
        self.test_ui()

    def create_layouts(self):
        self.main_ly = QtGui.QHBoxLayout()
        self.users_ly = QtGui.QVBoxLayout()
        self.content_ly = QtGui.QVBoxLayout()
        self.ptlayout = QtGui.QHBoxLayout()
        self.ctlayout = QtGui.QHBoxLayout()
        self.btlayout = QtGui.QHBoxLayout()
        self.inlayout = QtGui.QHBoxLayout()
        self.ppcontain_ly = QtGui.QVBoxLayout()
        layouts = (self.main_ly, self.users_ly, self.content_ly, self.ctlayout)
        for layout in layouts:
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

    def create_containers(self):
        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(self.main_ly)
        self.users_frame = QtGui.QFrame()
        self.users_frame.setLayout(self.users_ly)
        self.users_frame.setFixedWidth(270)
        self.main_ly.addWidget(self.users_frame)
        self.pptitle_frame = QtGui.QFrame()
        self.pptitle_frame.setLayout(self.ptlayout)
        self.pptitle_frame.setFixedHeight(50)
        self.users_ly.addWidget(self.pptitle_frame)
        self.ppcontainer = QtGui.QWidget()
        self.ppcontainer.setLayout(self.ppcontain_ly)
        self.ppscroller = QtGui.QScrollArea()
        self.ppscroller.setWidget(self.ppcontainer)
        self.ppscroller.setWidgetResizable(True)
        self.users_ly.addWidget(self.ppscroller)

    def create_containers2(self):
        self.content_frame = QtGui.QFrame()
        self.content_frame.setLayout(self.content_ly)
        self.main_ly.addWidget(self.content_frame)
        self.cctitle_frame = QtGui.QFrame()
        self.cctitle_frame.setLayout(self.ctlayout)
        self.cctitle_frame.setFixedHeight(50)
        self.content_ly.addWidget(self.cctitle_frame)
        self.button_frame = QtGui.QFrame()
        self.button_frame.setLayout(self.btlayout)
        self.chcontainer = elements.ChatTab()
        self.chcontainer.new_chat('Group')
        self.content_ly.addWidget(self.chcontainer)
        self.input_frame = QtGui.QFrame()
        self.input_frame.setLayout(self.inlayout)
        self.input_frame.setFixedHeight(70)
        self.content_ly.addWidget(self.input_frame)

    def create_elements(self):
        self.emwindow = QtGui.QDockWidget('Emoji', self)
        self.emwindow.setWidget(self.emoprovider)
        self.emwindow.setFloating(True)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.emwindow)
        self.emwindow.hide()

    def create_elements2(self):
        pptitle = QtGui.QLabel('Participants')
        pptitle.setStyleSheet('font-size: 21px;')
        self.ptlayout.addWidget(pptitle)
        rfbutton = QtGui.QPushButton()
        rfbutton.setFixedSize(36, 36)
        rfbutton.setIcon(QtGui.QIcon(os.path.join('resources', 'images', 'refresh.svg')))
        rfbutton.setIconSize(QtCore.QSize(30, 30))
        rfbutton.setToolTip('Refresh participants list')
        rfbutton.setStyleSheet('.QPushButton{border-radius: 18px;}.QPushButton::hover{background-color: rgba(94, 94, 94, 150);}')
        self.ptlayout.addWidget(rfbutton)
        completer = QtGui.QCompleter(self.userlist)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        sbinput = elements.ButtonLineEdit(os.path.join('resources', 'images', 'arrow.svg'))
        sbinput.buttonClicked.connect(lambda: self.search(sbinput.text()))
        sbinput.setPlaceholderText('Search users...')
        sbinput.setCompleter(completer)
        sbinput.returnPressed.connect(sbinput.button.click)
        sbinput.setStyleSheet('font-size: 15px;')
        self.ctlayout.addWidget(sbinput, alignment = QtCore.Qt.AlignLeft)
        afbutton = QtGui.QPushButton()
        afbutton.setFixedSize(36, 36)
        afbutton.setIcon(QtGui.QIcon(os.path.join('resources', 'images', 'attach.svg')))
        afbutton.setIconSize(QtCore.QSize(30, 30))
        afbutton.setToolTip('Send a file')
        afbutton.setStyleSheet('.QPushButton{border-radius: 18px;}.QPushButton::hover{background-color: rgba(94, 94, 94, 150);}')
        self.btlayout.addWidget(afbutton)
        stbutton = QtGui.QPushButton()
        stbutton.setFixedSize(36, 36)
        stbutton.setIcon(QtGui.QIcon(os.path.join('resources', 'images', 'settings.svg')))
        stbutton.setIconSize(QtCore.QSize(30, 30))
        stbutton.setToolTip('Settings')
        stbutton.setStyleSheet('.QPushButton{border-radius: 18px;}.QPushButton::hover{background-color: rgba(94, 94, 94, 150);}')
        self.btlayout.addWidget(stbutton)
        lgbutton = QtGui.QPushButton()
        lgbutton.setFixedSize(36, 36)
        lgbutton.setIcon(QtGui.QIcon(os.path.join('resources', 'images', 'logoff.svg')))
        lgbutton.setIconSize(QtCore.QSize(30, 30))
        lgbutton.setToolTip('Sign Out')
        lgbutton.setStyleSheet('.QPushButton{border-radius: 18px;}.QPushButton::hover{background-color: rgba(94, 94, 94, 150);}')
        lgbutton.clicked.connect(self.closeslot)
        self.btlayout.addWidget(lgbutton)
        self.ctlayout.addWidget(self.button_frame, alignment = QtCore.Qt.AlignRight)
        embutton = QtGui.QPushButton()
        embutton.setFixedSize(52, 52)
        embutton.setIcon(QtGui.QIcon(os.path.join('resources', 'images', 'emoji.svg')))
        embutton.setIconSize(QtCore.QSize(32, 32))
        embutton.setToolTip('Open emoji picker')
        embutton.setStyleSheet('.QPushButton{border: 2px solid #91b7b0; border-radius: 25px; background-color: rgba(145, 163, 176, 200);}.QPushButton::hover{background-color: rgb(64, 64, 64);}')
        embutton.clicked.connect(self.emwindow.show)
        self.inlayout.addWidget(embutton)
        self.text_input = QtGui.QTextEdit()
        self.text_input.setStyleSheet('font-size: 15px;')
        shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Return"), self.text_input)
        shortcut.activated.connect(self.sendslot)
        self.inlayout.addWidget(self.text_input)
        sebutton = QtGui.QPushButton()
        sebutton.setFixedSize(52, 52)
        sebutton.setIcon(QtGui.QIcon(os.path.join('resources', 'images', 'send.svg')))
        sebutton.setIconSize(QtCore.QSize(32, 32))
        sebutton.setToolTip('Send a message (Ctrl+Enter)')
        sebutton.setStyleSheet('.QPushButton{border: 2px solid #08b7ff; border-radius: 25px; background-color: rgba(8, 129, 255, 200);}.QPushButton::hover{background-color: rgb(8, 99, 255);}')
        sebutton.clicked.connect(self.sendslot)
        self.inlayout.addWidget(sebutton)

    def test_ui(self):
        xc = elements.UserCard(self.nameslot)
        xc.render('Cagney.Carnation', 'Online', 1)
        self.ppcontain_ly.addWidget(xc)
        yc = elements.UserCard(self.nameslot)
        yc.render('Djimmi.The.Great', 'Online', 2)
        self.ppcontain_ly.addWidget(yc)
        zc = elements.UserCard(self.nameslot)
        zc.render('Baroness.Von.Bonbon', '23-12-2019 7:02am', 2)
        self.ppcontain_ly.addWidget(zc)
        xc = elements.UserCard(self.nameslot)
        xc.render('Wally.Warbles', 'Online', 3)
        self.ppcontain_ly.addWidget(xc)
        yc = elements.UserCard(self.nameslot)
        yc.render('Carla.Maria', 'Online', 3)
        self.ppcontain_ly.addWidget(yc)
        yc = elements.UserCard(self.nameslot)
        yc.render('King.Dice', 'Online', 3)
        self.ppcontain_ly.addWidget(yc)
        xc = elements.UserCard(self.nameslot)
        xc.render('Grimm.MatchStick', 'Today 3:30pm', 3)
        self.ppcontain_ly.addWidget(xc)
        zc = elements.UserCard(self.nameslot)
        zc.render('Hilda.Berg', 'Yesterday 12:52pm', 3)
        self.ppcontain_ly.addWidget(zc)
        zc = elements.UserCard(self.nameslot)
        zc.render('Dr.Kahl', 'Yesterday 12:52pm', 3)
        self.ppcontain_ly.addWidget(zc)
        #
        bb = elements.Bubble()
        bb.render('Welcome to Chatz 1.0 chatroom! Feel at home!')
        self.chcontainer.chats['Group'].layout.addWidget(bb, alignment = bb.align)
        bb = elements.Bubble()
        bb.render('King.Dice', test1, '10:42pm')
        self.chcontainer.chats['Group'].layout.addWidget(bb, alignment = bb.align)
        bb = elements.Bubble()
        bb.render(test2, '10:50pm')
        self.chcontainer.chats['Group'].layout.addWidget(bb, alignment = bb.align)
        bb = elements.Bubble()
        bb.render('Dr.Kahl', test3, '10:55pm')
        self.chcontainer.chats['Group'].layout.addWidget(bb, alignment = bb.align)

    def search(self, who):
        for x in range(self.ppcontain_ly.count()):
            if self.ppcontain_ly.itemAt(x).widget().alias == who:
                self.ppscroller.ensureWidgetVisible(self.ppcontain_ly.itemAt(x).widget())
                self.ppcontain_ly.itemAt(x).widget().blink()

    def refresh_users(self, users):
        self.userlist = []
        for user in users:
            self.userlist.append(user)
            entry = elements.UserCard(self.nameslot)
            entry.render(user, utils.toDateStr(users[user][2]), users[user][1])
            self.ppcontain_ly.addWidget(entry)

    def display_error(self, text):
        dialog = QtGui.QMessageBox()
        dialog.setIcon(QtGui.QMessageBox.Critical)
        dialog.setText(text)
        dialog.setWindowIcon(self.windowIcon())
        dialog.setWindowTitle('Error')
        dialog.exec_()

    def closeslot(self):
        while self.main_ly.count():
            child = self.main_ly.takeAt(0)
            if child.widget(): child.widget().deleteLater()
        self.setCentralWidget(elements.AuthForm(self.credslot))

    def credslot(self, creds):
        alias = creds[1]
        if re.match(r'^[\.\-\$_!<>a-zA-Z0-9]+$', alias): pass
        else:
            msg = 'Accepted characters in alias: a-z, A-Z, numbers, symbols in brackets(._-$!<>), NO spaces, tabs or unicode characters!'
        try:
            dialog = QtGui.QMessageBox()
            dialog.setIcon(QtGui.QMessageBox.Warning)
            dialog.setText(msg)
            dialog.setWindowIcon(self.windowIcon())
            dialog.setWindowTitle('Illegal Alias')
            dialog.exec_()
            return None
        except: pass
        self.setup_ui()
        self.setCentralWidget(self.main_widget)

    def sendslot(self):
        self.parser.feed(str(self.text_input.toHtml()))
        message = self.parser.produce()
        actual = emoji.emojize(message[0], use_aliases = True)#this is what we'll send
        if len(actual) > 0:
            rcp = self.chcontainer.get_chat()
            bb = elements.Bubble()
            bb.render(message[1], '10:46pm')
            self.chcontainer.chats[rcp].layout.addWidget(bb, alignment = bb.align)
            self.text_input.clear()
            #actually send message, username is -> self.chcontainer.get_chat()

    def recvslot(self, type_, mesg):
        entry = elements.Bubble()
        sender, message, time = mesg
        if type_ == 1:#server message
            entry.render(message)
            self.chcontainer.chats['Group'].layout.addWidget(entry, alignment = entry.align)
        elif type_ == 2:#group message
            entry.render(sender, message, time)
            self.chcontainer.chats['Group'].layout.addWidget(entry, alignment = entry.align)
        elif type_ == 3:#direct message
            entry.render(sender, message, time)
            if sender not in self.chcontainer.chats: self.nameslot(sender)
            self.chcontainer.chats[sender].layout.addWidget(entry, alignment = entry.align)
        else: pass

    def nameslot(self, uname):
        self.chcontainer.new_chat(uname)

    def emojislot(self, filename, pointer):
        pathx = os.path.join('resources', 'emoji', pointer, filename)
        formatted = '<img src = {} />'.format(pathx)
        self.text_input.insertHtml(formatted)

app = QtGui.QApplication(sys.argv)

pixmap = QtGui.QPixmap(os.path.join('resources', 'images', 'splash.png'))
splash = QtGui.QSplashScreen(pixmap, QtCore.Qt.WindowStaysOnTopHint)
splash.show()

app.processEvents()
    
win = UIHandler()
win.show()

splash.finish(win)

sys.exit(app.exec_())
