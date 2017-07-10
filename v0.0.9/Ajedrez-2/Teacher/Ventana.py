import gtk
import cv2


class Ventana:

    def on_open_clicked(self, button):
        print "\"Open\" button was clicked"

    def on_close_clicked(self, button):
        print "Closing application"
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window()
        self.window.connect('delete-event', gtk.main_quit)

        self.box = gtk.Box()
        self.window.add(self.box)

        self.button = gtk.Button(label='Open')
        self.button.connect("clicked", self.on_open_clicked)

        self.box.pack_start(self.button, True, True, 0)

        self.button = gtk.Button(label='Cerrar')
        self.button.connect("clicked", self.on_close_clicked)

        self.box.pack_start(self.button, True, True, 0)

        self.window.show_all()
        gtk.main()


class OpenCV:
    def __init__(self, cam):
        pass

    @staticmethod
    def ventana(winName, x, y, width, height):
        cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
        cv2.moveWindow(winName, x, y)
        cv2.resizeWindow(winName, width, height)
