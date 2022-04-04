import matplotlib.pyplot as plt

class MyPlot(object):

    def makePlot(self):
        self.fig = plt.figure('Test', figsize=(10, 8))
        ax = plt.subplot(111)
        x = range(0, 100, 10)
        y = (5,)*10
        ax.plot(x, y, '-', color='red')
        ax.plot(x, y, 'o', color='blue', picker=5)
        self.highlight, = ax.plot([], [], 'o', color='yellow')
        self.cid = plt.connect('pick_event', self.onPick)
        plt.show()

    def onPick(self, event=None):
        this_point = event.artist
        x_value = this_point.get_xdata()
        y_value = this_point.get_ydata()
        ind = event.ind
        self.highlight.set_data(x_value[ind+1][0],y_value[ind][0])
        self.fig.canvas.draw_idle()

if __name__ == '__main__':
    app = MyPlot()
    app.makePlot()