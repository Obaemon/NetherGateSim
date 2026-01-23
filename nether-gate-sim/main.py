import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nether Gate Simulator")
        # self.setMinimumSize(800, 600)

        figure = Figure()
        self.canvas = FigureCanvasQTAgg(figure)
        self.setCentralWidget(self.canvas)

        self.ax = figure.add_subplot(111)
        self.ax.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.ax.grid(True)
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal', adjustable='box')

        self.ax.axhline(0, linewidth=2, color='black')
        self.ax.axvline(0, linewidth=2, color='black')
        

        self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.tick_params(axis='x', direction='in', pad=-15)
        self.ax.tick_params(axis='y', direction='in', pad=-25)

        self.press_event = None

        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("motion_notify_event", self.on_move)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("scroll_event", self.on_scroll)

        self.ax.plot([0,1,2,3,4,5,6,7,8,9,10], [0,1,0,1,2,1,2,3,2,3,6])
        self.ax.invert_yaxis()

        self.canvas.draw()
    
    def on_press(self, event):
        if event.button != 1:
            return
        
        self.press_event = {
            "x": event.xdata,
            "y": event.ydata,
            "xlim": self.ax.get_xlim(),
            "ylim": self.ax.get_ylim()
        }

    def on_move(self, event):
        if self.press_event is None:
            return
        if event.xdata is None or event.ydata is None:
            return
        
        xpress = self.press_event["x"]
        ypress = self.press_event["y"]
        xmin, xmax = self.press_event["xlim"]
        ymin, ymax = self.press_event["ylim"]
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        self.ax.set_xlim(xmin - dx, xmax - dx)
        self.ax.set_ylim(ymin - dy, ymax - dy)

        self.canvas.draw_idle()
        
    def on_release(self, event):
        self.press_event = None

    def on_scroll(self, event):
        if event.inaxes != self.ax:
            return
        
        base_scale = 1.2

        if event.button == 'up':
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            scale_factor = 1

        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()
        xdata = event.xdata
        ydata = event.ydata

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        self.ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * relx])
        self.ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * rely])
        self.canvas.draw_idle()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
