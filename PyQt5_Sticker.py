import sys, time, threading
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie

class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size=1.0, on_top=False):
        super(Sticker, self).__init__()

        self.img_path = img_path
        self.xy = xy
        self.from_xy = xy
        self.to_xy = xy
        self.speed = 60
        self.direction = [0, 0] # x: 0(left), 1(right), y: 0(up), 1(down)
        self.size = size
        self.on_top = on_top
        self.setupUi()
        self.show()

    def walk(self, from_xy, to_xy, speed=60):
        self.from_xy = from_xy
        self.to_xy = to_xy
        self.speed = speed

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.__walkHandler)
        self.timer.start(1000 / self.speed)

    def __walkHandler(self):
        if self.xy[0] >= self.to_xy[0]:
            self.direction[0] = 0
        elif self.xy[0] < self.from_xy[0]:
            self.direction[0] = 1

        if self.direction[0] == 0:
            self.xy[0] -= 1
        else:
            self.xy[0] += 1

        if self.xy[1] >= self.to_xy[1]:
            self.direction[1] = 0
        elif self.xy[1] < self.from_xy[1]:
            self.direction[1] = 1

        if self.direction[1] == 0:
            self.xy[1] -= 1
        else:
            self.xy[1] += 1

        self.move(*self.xy)

    def setupUi(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint if self.on_top else QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.img_path)
        label.setMovie(movie)
        movie.start()
        movie.stop()

        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))

        movie.start()
        self.setGeometry(self.xy[0], self.xy[1], w, h)

        self.del_label = QtWidgets.QLabel(centralWidget)
        self.del_movie = QMovie('gif/Boom3.gif')
        self.del_label.setMovie(self.del_movie)

        self.del_movie.setScaledSize(QtCore.QSize(w, h))
        self.del_movie.start()
        self.del_label.hide()

        self.setGeometry(self.xy[0], self.xy[1], w, h)


    def mouseDoubleClickEvent(self, e):

        creat_time= time.time()

        def sec_timer():
            click_time = time.time()
            while True:
                if (time.time() - click_time) > 0.75:

                    QtWidgets.qApp.quit()
                    break
                    
        self.del_label.show()
        self.del_movie.start()
         
        t = threading.Thread(target=sec_timer)
        t.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    baloon = Sticker('gif/giphy.gif', xy=[2881, -369], size=0.35, on_top=True)
    Joo = Sticker('gif/jw_emo.gif', xy=[2849, -400], size=0.1, on_top=True)
    Loading = Sticker('gif/loading.gif', xy=[1953, -145], size=0.5, on_top=False)
    #Loading.walk(from_xy=[1927, -145], to_xy=[1975, -145])

    sys.exit(app.exec_())