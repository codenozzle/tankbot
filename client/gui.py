import wx, httplib, base64, StringIO, datetime
from Config import Config

class GUI(wx.Frame):

    ID_FRAME_REFRESH = wx.NewId()

    def __init__(self):
        config = Config()
        
        wx.Frame.__init__(self, None, wx.ID_ANY, config.getAppTitle(), style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
        
        # Add a panel so it looks the correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()

        exitMenuItem = fileMenu.Append(wx.NewId(), "Quit", "Quit")
        self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)

        menuBar.Append(fileMenu, "&Robot")
        self.SetMenuBar(menuBar)
        
        # IP Camera
        self.Camera = DLink(config.getIPAddress(), config.getUserName(), config.getPassword())
        
        # Camera Panel
        self.CameraPanel = CameraPanel(self, self.Camera)
        
        # Frame timer
        self.Timer = wx.Timer(self, self.ID_FRAME_REFRESH)
        self.Timer.Start(1)
        wx.EVT_TIMER(self, self.ID_FRAME_REFRESH, self.Refresh)
        
        # Frame Sizer
        self.Sizer = None
        self.Size()
        
        # Show frame
        self.Show(True)
        
        # Attempt connection to Camera
        self.Camera.Connect()
        
    def Size(self):
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.CameraPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.Sizer)
        self.Fit()
        
    def Refresh(self, event):
        self.CameraPanel.Refresh()
        
    def onExit(self, event):
        self.Camera.Disconnect()
        self.Close()

class CameraPanel(wx.Panel):

    # Global Variables #
    CAMERA_SIZE_WIDTH = 640
    CAMERA_SIZE_HEIGHT = 480
    
    def __init__(self, parent, camera):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=wx.SIMPLE_BORDER)
        
        self.Camera = camera
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        
        self.SetSize((self.CAMERA_SIZE_WIDTH, self.CAMERA_SIZE_HEIGHT))
        
    def OnEraseBackground(self, event):
        pass
        
    def OnPaint(self, event):
        panel = wx.BufferedPaintDC(self)
        if self.Camera.Connected:
            try:
                stream = self.Camera.Update()
                if stream != None:
                    img = wx.ImageFromStream(stream)
                    bmp = wx.BitmapFromImage(img)
                    panel.DrawBitmap(bmp, 0, 0, True)
            except:
                pass
        else:
            panel.SetTextForeground(wx.WHITE)
            panel.SetFont(self.GetFont())
            panel.SetBackground(wx.BLACK_BRUSH)
            panel.Clear()
            panel.DrawBitmap(wx.Bitmap("splash.bmp"), 20, 40)
            panel.DrawText("Connecting...", 280, 400)

class DLink():

    def __init__(self, ip, username, password):
        self.IP = ip
        self.Username = username
        self.Password = password
        self.Connected = False
        
    def Connect(self):
        if self.Connected == False:
            try:
                print "Acquiring connection: " + self.Username + "@" + self.IP
                connection = httplib.HTTP(self.IP)
                connection.putrequest("GET", "/video/mjpg.cgi")
                connection.putheader("Authorization", "Basic %s" % base64.encodestring("%s:%s" % (self.Username, self.Password))[:-1])
                connection.endheaders()
                #errcode, ermsg, headers = connection.getreply()
                connection.getreply()
                self.File = connection.getfile()
                self.Connected = True
                print "Connection established:", datetime.datetime.now()
                print "Starting live stream...\n"
                
            except httplib.HTTPException, e:
                print "   Error: ", e
                self.Connected = False
        
    def Disconnect(self):
        self.Connected = False
        print "Shutting down\n"
        
    def Update(self):
        if self.Connected:
            s = self.File.readline()  # "--video boundary--'
            s = self.File.readline()  # "Content-Length: #####"
            framesize = int(s[16:])
            s = self.File.readline()  # "Date: ##-##-#### ##:##:## AM IO_00000000_PT_000_000"
            s = self.File.readline()  # "Content-type: image/jpeg"
            s = self.File.read(framesize)  # jpeg data
            while s[0] != chr(0xff):
                s = s[1:]
            return StringIO.StringIO(s)           

if __name__ == "__main__":
    app = wx.App(redirect=False)
    GUI()
    app.MainLoop()
