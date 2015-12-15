# -*- coding:utf8 -*-

#A class that allows zoom and moving in matplotlib axes inside the figure limits.

class ZoomPan:
    def __init__(self, ax, func, lat0, lon0, elev, topography=0):
        self.press = None
        self.cur_xlim = ax.get_xlim()
        self.cur_ylim = ax.get_ylim()
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.func = func
        self.lon0 = lon0
        self.lat0 = lat0
        self.elev = elev
        self.xlim = None
        self.ylim = None
        self.call_echo = None
        self.topo = topography


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print event.button

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
            #deals with the figure limits
            if xdata - new_width*(1-relx) >= self.cur_xlim[0] and xdata \
            + new_width*(relx) <= self.cur_xlim[1]:
                ax.set_xlim([xdata - new_width*(1-relx), xdata + new_width*(relx)])
            if ydata - new_height*(1-rely) >= self.cur_ylim[0] and ydata \
            + new_height*(rely) <= self.cur_ylim[1]:
                ax.set_ylim([ydata - new_height*(1-rely), ydata + new_height*(rely)])
            ###
            self.xlim = ax.get_xlim()
            self.ylim = ax.get_ylim()
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press
            self.x1 = cur_xlim
            self.y1 = cur_ylim

        def onRelease(event):
            self.press = None
            if self.x1[0]==self.xlim[0]:
                if self.y1[0]==self.ylim[0]:
                    if self.topo==1:
                        axe = self.func(elev=self.elev,
                                        lat=self.lat0-self.ypress/60.,
                                        lon=self.lon0+self.xpress/60.,
                                        topography=self.topo,cbar=0)
                    else:
                        axe = self.func(elev=self.elev,
                                        lat=self.lat0-self.ypress/95.013,
                                        lon=self.lon0+self.xpress/95.013,
                                        topography=self.topo,cbar=0)
                    ax.set_xlim(self.xlim)
                    ax.set_ylim(self.ylim)
            ax.figure.canvas.draw()
            

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            #deals with the figure limits
            if cur_xlim[0] - dx >= self.cur_xlim[0] and cur_xlim[1] - dx \
            <= self.cur_xlim[1]:
                cur_xlim -= dx
            if cur_ylim[0] - dy >= self.cur_ylim[0] and cur_ylim[1] - dy \
            <= self.cur_ylim[1]:
                cur_ylim -= dy
            ###
            ax.set_xlim(cur_xlim)
            ax.set_ylim(cur_ylim)
            self.xlim = ax.get_xlim()
            self.ylim = ax.get_ylim()
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion
