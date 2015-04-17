import ConfigParser

class Config:
    
    configFileName = 'configs.ini'
    
    def __init__(self):
        self.parser = ConfigParser.SafeConfigParser()
        self.parse()
        
    def parse(self):
        self.parser.read(self.configFileName)
        self.app_title = self.parser.get('app', 'title')
        self.gamepad_inverted = self.parser.get('gamepad', 'inverted')
        self.ip_address = self.parser.get('camera_params', 'ip_address')
        self.username = self.parser.get('camera_params', 'username')
        self.password = self.parser.get('camera_params', 'password')
        self.com_port = self.parser.get('serial_params', 'com_port')
        self.baud_rate = self.parser.get('serial_params', 'baud_rate')   
            
    def printAll(self):
        print 'App Title: ', self.app_title
        print 'Gamepad Inverted:', self.gamepad_inverted
        print 'Camera Params:', self.ip_address, self.username, self.password
        print 'Serial Params:', self.com_port, self.baud_rate
        
    def save(self):
        newConfig = ConfigParser.RawConfigParser()
        
        newConfig.add_section('app')
        newConfig.set('app', 'title', self.getAppTitle())
        
        newConfig.add_section('gamepad')
        newConfig.set('gamepad', 'inverted', self.getGamePadInverted())
        
        newConfig.add_section('camera_params')
        newConfig.set('camera_params', 'ip_address', self.getIPAddress())
        newConfig.set('camera_params', 'username', self.getUserName())
        newConfig.set('camera_params', 'password', self.getPassword())
        
        newConfig.add_section('serial_params')
        newConfig.set('serial_params', 'com_port', self.getComPort())
        newConfig.set('serial_params', 'baud_rate', self.getBaudRate())
        
        with open(self.configFileName, 'wb') as configfile:
            newConfig.write(configfile)
        
    def getAppTitle(self):
        return self.app_title
    
    def setAppTitle(self, appTitle):
        self.app_title = appTitle
    
    def getGamePadInverted(self):
        return self.gamepad_inverted
    
    def setGamePadInverted(self, gamePadInverted):
        self.gamepad_inverted = gamePadInverted
    
    def getIPAddress(self):
        return self.ip_address
    
    def setIPAddress(self, ipAddress):
        self.ip_address = ipAddress
    
    def getUserName(self):
        return self.username
    
    def setUserName(self, username):
        self.username = username
    
    def getPassword(self):
        return self.password
    
    def setPassword(self, password):
        self.password = password
    
    def getComPort(self):
        return self.com_port
    
    def setComPort(self, comPort):
        self.com_port = comPort
    
    def getBaudRate(self):
        return self.baud_rate
    
    def setBaudRate(self, baudRate):
        self.baud_rate = baudRate
        
        
        
        
        