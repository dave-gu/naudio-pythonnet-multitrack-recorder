import clr #pythonnet
import sys
print(sys.path)
import pdb
import threading
import wx

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
        wx.Frame.__init__(self,parent,569,title,(50,50),(300,300))
        self.sb = self.CreateStatusBar()
        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        bt1 = tb.AddTool(701,"Rec",wx.Bitmap("icon.png"))
        bt2 = tb.AddTool(702,"PDB",wx.Bitmap("icon.png"))
        self.Bind(wx.EVT_TOOL,gorecord,bt1)
        self.Bind(wx.EVT_TOOL,debog,bt2)
        tb.Realize()
    def OnExit(self,e):
        self.Close(True)
########
def gorecord(shelf):
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
    
def debog(shelf):
    pdb.set_trace()

app=wx.App(0)
filething = FileMgr(None,420,'Recorder')
filething.Show(True)
app.MainLoop()

#http://pythonnet.github.io/
#https://channel9.msdn.com/coding4fun/articles/NET-Voice-Recorder
