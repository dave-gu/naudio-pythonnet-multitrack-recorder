#import pythomcom
#pythomcom.CoInitialize()
import ctypes
ctypes.windll.ole32.CoInitialize(None)

import clr #pythonnet
import sys
print(sys.path)
import pdb
import threading
import wx
#poly wav version info:
#check just one ASIO device and click the third toolbar button to record a timestamped wav to the local directory.

#USAGE: python 3+, pip install wxpython, pip install pythonnet, pip install pdb, cmd /k python.exe -i %thisscript%
#recording inputs are displayed, check boxes for which ones will be recorded, timestamped wavs recorded to same directory, close app to finish recording.
#haven't implemented the monitoring things that are reflected on the UI yet... although it isn't really necessary
#if you go into the windows audio control panel there is an checkbox to toggle to monitor called "listen to this device"
#compared to the earlier version the difference in behavior is that this supports up to 11 inputs and doesn't record anything for unchecked inputs.
#TODO: add config for stereo/mono & sampling rate.. currently just stereo and 44.1 khz
from System import Environment
name = Environment.MachineName
print(name)
from System import Console
#clr.AddReference('Microsoft.VisualStudio.Tools.Office.Excel.HostAdapter.v10.0.dll')
clr.AddReference('NAudio') #ildasm used on NAudio.dll showed this was the namespace
import NAudio as NAudio
from System import EventHandler, EventArgs
#https://stackoverflow.com/questions/52612651/pythonnet-delegate-method-with-generics-not-being-called
########
class FileMgr(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self,parent,569,title,(50,50),(800,300))
        self.sb = self.CreateStatusBar()
        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        bt1 = tb.AddTool(701,"Rec",wx.Bitmap("icon.png"))
        bt2 = tb.AddTool(702,"PDB",wx.Bitmap("icon.png"))
        bt3 = tb.AddTool(703,"DBG",wx.Bitmap("icon.png"))
        self.Bind(wx.EVT_TOOL,gorecordA,bt1)
        self.Bind(wx.EVT_TOOL,gorecordA,bt2)
        self.Bind(wx.EVT_TOOL,mytest2,bt3)
        tb.Realize()
        
        self.topsplitter = wx.SplitterWindow(self,808,pos=wx.Point(0,0),size=wx.Size(400,400),style=wx.SP_BORDER,name="TopSplitter")
        self.AudioChecker = AudioCheckList(self.topsplitter, 777)
        self.recdevct = self.AudioChecker.Count
        #self.MonitorChoice = MonitorChoice(self.topsplitter, 888)
        self.rightside = MonitorPanel(self.topsplitter,999,self.recdevct)
        #self.splitter = wx.SplitterWindow(self.topsplitter, ID_SPLITTER,pos=wx.Point(0,0),size=wx.Size(400,400),style=wx.SP_BORDER,name="Splitter")
        self.topsplitter.SplitVertically(self.AudioChecker,self.rightside)
    def OnExit(self,e):
        self.Close(True)
        
class AudioCheckList(wx.CheckListBox):
    def __init__(self, parent, id):
        devicecount = NAudio.Wave.WaveIn.DeviceCount
        devicelist = []
        for n in range(devicecount):
            devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
        wx.CheckListBox.__init__(self, parent, id,(0,0),(50,50),devicelist)
        #https://docs.wxpython.org/gallery.html shows most widgets

#class ASIOChoice(wx.Choice):
#lol
class ASIOChoice(wx.CheckListBox):
    def __init__(self, parent, id, pos, size):
        global availables
        availables = NAudio.Wave.AsioOut.GetDriverNames()
        #global asiolist
        global asiolist
        asiolist = []
        for n in range(10):
            try:
                asiolist.append(availables.Get(n))
            except:
                pass
        print('asiolist?')
        print(asiolist)
        wx.CheckListBox.__init__(self, parent, id, pos,size, asiolist)

class MonitorChoice(wx.Choice):
    #def __init__(self,parent,id):
    def __init__(self,parent,id,pos,size):
        devicecount = NAudio.Wave.WaveOut.DeviceCount
        devicelist = []
        for n in range(devicecount):
            devicelist.append(NAudio.Wave.WaveOut.GetCapabilities(n).ProductName)
        #wx.Choice.__init__(self, parent, id, (0,0), (50,50), devicelist)
        wx.Choice.__init__(self, parent, id, pos, size, devicelist)
        
class MonitorPanel(wx.Panel):
    def __init__(self,parent,id, countt):
        wx.Panel.__init__(self,parent,id, (0,0), (50,50), 0, "Monitor-Panel")
        for xx in range(countt):
            globals()["mon" + str(xx)] = MonitorChoice(self, 1200 + xx, (0+(xx*5),0+(xx*23)), (120,23))
        for xx in range(countt):
            globals()["monbt" + str(xx)] = wx.CheckBox(self,1400 + xx, "mon"+str(xx), (127+(xx*5),0+(xx*23)), (70,23))
        
        global asiochoice
        asiochoice = ASIOChoice(self, 5678,(220,0),(200,200))
########
def gorecordA(shelf):
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    devicelist = []
    for n in range(devicecount):
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    print(devicelist)
    
    traceyesno = 0
    if traceyesno == 0:
        pass
    elif traceyesno == 1:
        pdb.set_trace()
    
    checkedlist = filething.AudioChecker.GetChecked()
    print(checkedlist)
    #pdb.set_trace()
    #filething.rightside.
    
    #for xx in range(devicecount):
        #global globals()["waveIn" + str(xx)] 
        
    ## replacing range devicecount with for xx in checkedlist:
    for xx in checkedlist:
        globals()["waveIn" + str(xx)] = NAudio.Wave.WaveIn()
    for xx in checkedlist:
        globals()["waveIn" + str(xx)].DeviceNumber = xx
    ##global waveIn
    ##global waveIn2
    ##global waveIn3
    ###waveIn = NAudio.Wave.WaveIn()
    ###waveIn2 = NAudio.Wave.WaveIn()
    ###waveIn3 = NAudio.Wave.WaveIn()
    ####waveIn.DeviceNumber = 0
    ####waveIn2.DeviceNumber = 1
    ####waveIn3.DeviceNumber = 2
    fourfour = 44100
    foureight = 48000
    channels = 2
    for xx in checkedlist:
        globals()["waveIn" + str(xx)].WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #####waveIn.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #####waveIn2.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    #####waveIn3.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    import datetime
    timestampz = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    for xx in checkedlist:
        globals()["writer" + str(xx)] = NAudio.Wave.WaveFileWriter(timestampz + "." + str(xx) + '.wav', globals()["waveIn" + str(xx)].WaveFormat)
    
    ##writer1 = NAudio.Wave.WaveFileWriter(timestampz + ".1.wav", waveIn.WaveFormat)
    ##writer2 = NAudio.Wave.WaveFileWriter(timestampz + ".2.wav", waveIn2.WaveFormat)
    ##writer3 = NAudio.Wave.WaveFileWriter(timestampz + ".3.wav", waveIn3.WaveFormat)
    
    def wave0write(sender, e):
        if 1 == 1:
            writer0.WriteData(e.Buffer,0,e.BytesRecorded)
            writer0.Flush()
    def wave1write(sender, e):
        if 1 == 1:
            writer1.WriteData(e.Buffer,0,e.BytesRecorded)
            writer1.Flush()
    def wave2write(sender, e):
        if 1 == 1:
            writer2.WriteData(e.Buffer,0,e.BytesRecorded)
            writer2.Flush()
    def wave3write(sender, e):
        if 1 == 1:
            writer3.WriteData(e.Buffer,0,e.BytesRecorded)
            writer3.Flush()
    def wave4write(sender, e):
        if 1 == 1:
            writer4.WriteData(e.Buffer,0,e.BytesRecorded)
            writer4.Flush()
    def wave5write(sender, e):
        if 1 == 1:
            writer5.WriteData(e.Buffer,0,e.BytesRecorded)
            writer5.Flush()
    def wave6write(sender, e):
        if 1 == 1:
            writer6.WriteData(e.Buffer,0,e.BytesRecorded)
            writer6.Flush()
    def wave7write(sender, e):
        if 1 == 1:
            writer7.WriteData(e.Buffer,0,e.BytesRecorded)
            writer7.Flush()
    def wave8write(sender, e):
        if 1 == 1:
            writer8.WriteData(e.Buffer,0,e.BytesRecorded)
            writer8.Flush()
    def wave9write(sender, e):
        if 1 == 1:
            writer9.WriteData(e.Buffer,0,e.BytesRecorded)
            writer9.Flush()
    def wave10write(sender, e):
        if 1 == 1:
            writer10.WriteData(e.Buffer,0,e.BytesRecorded)
            writer10.Flush()
    

    
    #for xx in range(devicecount):
        #globals()["waveIn" + str(xx)].DataAvailable += locals()["wave"+str(xx)+"write"]
    ##for xx in range(devicecount):
    '''
    if 'waveIn0' in globals():
        waveIn0.DataAvailable += wave0write
        waveIn0.StartRecording()
    '''
        
    if 0 in checkedlist:
        waveIn0.DataAvailable += wave0write
        waveIn0.StartRecording()
    if 1 in checkedlist:
        waveIn1.DataAvailable += wave0write
        waveIn1.StartRecording()
    if 2 in checkedlist:
        waveIn2.DataAvailable += wave0write
        waveIn2.StartRecording()
    if 3 in checkedlist:
        waveIn3.DataAvailable += wave0write
        waveIn3.StartRecording()
    if 4 in checkedlist:
        waveIn4.DataAvailable += wave0write
        waveIn4.StartRecording()
    if 5 in checkedlist:
        waveIn5.DataAvailable += wave0write
        waveIn5.StartRecording()
    if 6 in checkedlist:
        waveIn6.DataAvailable += wave0write
        waveIn6.StartRecording()
    if 7 in checkedlist:
        waveIn7.DataAvailable += wave0write
        waveIn7.StartRecording()
    if 8 in checkedlist:
        waveIn8.DataAvailable += wave0write
        waveIn8.StartRecording()
    if 9 in checkedlist:
        waveIn9.DataAvailable += wave0write
        waveIn9.StartRecording()
    if 10 in checkedlist:
        waveIn10.DataAvailable += wave0write
        waveIn10.StartRecording()

    #waveIn.DataAvailable += wave1write
    #waveIn2.DataAvailable += wave2write
    #waveIn3.DataAvailable += wave3write

    #waveIn.StartRecording()
    #waveIn2.StartRecording()
    #waveIn3.StartRecording()
    filething.sb.SetStatusText("recording started")
'''
def gorecord(shelf): #unused. for reference.
    devicecount = NAudio.Wave.WaveIn.DeviceCount
    devicelist = []
    for n in range(devicecount):
        devicelist.append(NAudio.Wave.WaveIn.GetCapabilities(n).ProductName)
    print(devicelist)

    waveIn = NAudio.Wave.WaveIn()
    waveIn2 = NAudio.Wave.WaveIn()
    waveIn3 = NAudio.Wave.WaveIn()

    waveIn.DeviceNumber = 0
    waveIn2.DeviceNumber = 1
    waveIn3.DeviceNumber = 2

    fourfour = 44100
    foureight = 48000
    channels = 2
    waveIn.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    waveIn2.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)
    waveIn3.WaveFormat = NAudio.Wave.WaveFormat(fourfour,channels)

    import datetime
    timestampz = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    writer1 = NAudio.Wave.WaveFileWriter(timestampz + ".1.wav", waveIn.WaveFormat)
    writer2 = NAudio.Wave.WaveFileWriter(timestampz + ".2.wav", waveIn2.WaveFormat)
    writer3 = NAudio.Wave.WaveFileWriter(timestampz + ".3.wav", waveIn3.WaveFormat)

    def wave1write(sender, e):
        if 1 == 1:
            #print('ifone')
            ##print(e.Buffer)
            ##print(e.BytesRecorded)
            writer1.WriteData(e.Buffer,0,e.BytesRecorded)
            writer1.Flush()
    def wave2write(sender, e):
        #print('okay2')
        if 1 == 1:
            writer2.WriteData(e.Buffer,0,e.BytesRecorded)
            writer2.Flush()
    def wave3write(sender, e):
        #print('okay3')
        if 1 == 1:
            writer3.WriteData(e.Buffer,0,e.BytesRecorded)
            writer3.Flush()
    
    waveIn.DataAvailable += wave1write
    waveIn2.DataAvailable += wave2write
    waveIn3.DataAvailable += wave3write

    waveIn.StartRecording()
    waveIn2.StartRecording()
    waveIn3.StartRecording()
'''    
def debog(shelf):
    pdb.set_trace()
#https://markheath.net/category/naudio   
def mytest(shelf):
    filething.sb.SetStatusText(str(filething.AudioChecker.GetCheckedItems()))
def asio1write(sender, e):
    samples = e.GetAsInterleavedSamples()
    asio1writer.WriteSamples(samples,0,samples.Length)
    asio1writer.Flush()
def mytest2(shelf):
    filething.sb.SetStatusText(str(asiochoice.GetCheckedStrings() ) )
    global asiodev
    asiodev = NAudio.Wave.AsioOut(asiochoice.GetCheckedStrings()[0])
    #stathreadattribute needed > https://github.com/pythonnet/pythonnet/issues/108
    asiodev_channelcount = asiodev.DriverInputChannelCount #6 for Zoom H6
    #https://github.com/naudio/NAudio/blob/master/Docs/AsioRecording.md
    asiodev.InitRecordAndPlayback(None, asiodev_channelcount, 44100)
    import datetime
    timestampz = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    #asiowaveformat = NAudio.Wave.WaveFormat(44100,24,asiodev_channelcount)
    asiowaveformat = NAudio.Wave.WaveFormat(44100,16,asiodev_channelcount)
    global asio1writer
    asio1writer = NAudio.Wave.WaveFileWriter(timestampz + "." + 'poly' + '.wav', asiowaveformat)
    asiodev.AudioAvailable += asio1write
    asiodev.Play()
    #pdb.set_trace()
    
#https://markheath.net/post/how-to-record-and-play-audio-at-same
#https://archive.codeplex.com/?p=naudio
#https://github.com/naudio/NAudio/wiki
app=wx.App(0)
filething = FileMgr(None,420,'Simultaneous Multi Wav Recorder')
filething.Show(True)
##pdb.set_trace()
app.MainLoop()
#http://pythonnet.github.io/
#https://channel9.msdn.com/coding4fun/articles/NET-Voice-Recorder
