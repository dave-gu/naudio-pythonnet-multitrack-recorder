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
        wx.Frame.__init__(self,parent,569,title,(50,50),(1020,300))
        #originally (800,300) on last size param but expanded to 1020 for m0p version.
        self.sb = self.CreateStatusBar()
        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        bt1 = tb.AddTool(701,"Rec",wx.Bitmap("icon.png"))
        bt2 = tb.AddTool(702,"Rec",wx.Bitmap("icon.png"))
        #bt3 = tb.AddTool(703,"DBG",wx.Bitmap("icon.png"))
        bt3 = tb.AddTool(703,"ASIO",wx.Bitmap("icon.png"))
        
        bt4 = tb.AddTool(704,"LPBK",wx.Bitmap("icon.png"))
        
        bt5 = tb.AddTool(705,"RL",wx.Bitmap("icon.png"))
        
        self.Bind(wx.EVT_TOOL,gorecordA,bt1)
        self.Bind(wx.EVT_TOOL,gorecordA,bt2)
        self.Bind(wx.EVT_TOOL,mytest2,bt3)
        self.Bind(wx.EVT_TOOL,goLPBK,bt4)
        self.Bind(wx.EVT_TOOL,DOWASAPI,bt5)
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
        
        ###
        #clr.AddReference("System")
        
        ##https://docs.microsoft.com/en-us/dotnet/api/system.string?view=netcore-3.1
        
        #import System
        #from System import String
        #pdb.set_trace() 
        
        ###
        
        #global asiolist
        global asiolist
        asiolist = []
        try:
            #for n in range(10):
            for n in range(10):
                try:
                    #asiolist.append(availables.Get(n))
                    asiolist.append(availables[n])
                except:
                    pass
        except:
            pass
        #print('asiolist?')
        #print(asiolist)
        wx.CheckListBox.__init__(self, parent, id, pos,size, asiolist)
        
class LOOPCLB(wx.CheckListBox):
    def __init__(self, parent, id, pos, size):
        #list3 = ["temp","orar","Y"]
        objekthere = NAudio.CoreAudioApi.MMDeviceEnumerator()
        niceouthere = objekthere.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.Render, NAudio.CoreAudioApi.DeviceState.Active)
        count2here = niceouthere.get_Count()
        global alist
        alist = []
        blist = []
        for yyyyy in range(count2here):
            alist.append(niceouthere.get_Item(yyyyy))
            #print(niceout.get_Item(xxxx).get_DeviceFriendlyName())
            ##print(str(yyyyy) + ": " + niceouthere.get_Item(yyyyy).get_DeviceFriendlyName())
            blist.append(niceouthere.get_Item(yyyyy).get_DeviceFriendlyName())
            
        #maybe alist is not the type of list we think it is
        
        #end trace
        
        #wx.CheckListBox.__init__(self,parent,id,pos,size,list3)
        wx.CheckListBox.__init__(self,parent,id,pos,size,blist)
        

class MonitorChoice(wx.Choice):
    #def __init__(self,parent,id):
    def __init__(self,parent,id,pos,size):
        devicecount = NAudio.Wave.WaveOut.DeviceCount
        devicelist = []
        for n in range(devicecount):
            devicelist.append(NAudio.Wave.WaveOut.GetCapabilities(n).ProductName)
        #wx.Choice.__init__(self, parent, id, (0,0), (50,50), devicelist)
        wx.Choice.__init__(self, parent, id, pos, size, devicelist)
        #MonitorChoice is contained in MonitorPanel which is self.rightside and is split with self.AudioChecker on the left.
        
class MonitorPanel(wx.Panel):
    def __init__(self,parent,id, countt):
        wx.Panel.__init__(self,parent,id, (0,0), (50,50), 0, "Monitor-Panel")
        for xx in range(countt):
            globals()["mon" + str(xx)] = MonitorChoice(self, 1200 + xx, (0+(xx*5),0+(xx*23)), (120,23))
        for xx in range(countt):
            globals()["monbt" + str(xx)] = wx.CheckBox(self,1400 + xx, "mon"+str(xx), (127+(xx*5),0+(xx*23)), (70,23))
        
        global asiochoice
        asiochoice = ASIOChoice(self, 5678,(220,0),(200,200))
        #######2
        global loopclub
        loopclub = LOOPCLB(self,7272,(420,0),(200,200))
        #these lines added the children to this parent monitorpanel which is self.rightside
        
#######dowasapi
#this is for the LR button which records both the loopback and the checked inputs...
##tt
def DOWASAPI(shelf):
    #wasapilist = loopclub.GetChecked()
    checkedtorecloopback = loopclub.GetChecked()
    #returns something like (0,1,2)
    
    #print(alist[0])
    #for zzz in wasapilist:
        #print(str(zzz))
    
    #pdb.set_trace()
    
    #kapture0-7 are the objects connecting to the wavewriter later
    import datetime
    tz2 = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    
    '''
    def wave0write(sender, e):
        if 1 == 1:
            writer0.WriteData(e.Buffer,0,e.BytesRecorded)
            writer0.Flush()
    '''
    def w0wt(sender,e):
        kapture0writer.WriteData(e.Buffer,0,e.BytesRecorded)
        kapture0writer.Flush()
        
    def w1wt(sender,e):
        kapture1writer.WriteData(e.Buffer,0,e.BytesRecorded)
        kapture1writer.Flush()
        
    def w2wt(sender,e):
        kapture2writer.WriteData(e.Buffer,0,e.BytesRecorded)
        kapture2writer.Flush()
    
    if 0 in checkedtorecloopback:
        global kapture0
        kapture0 = NAudio.Wave.WasapiLoopbackCapture(alist[0])
        global kapture0writer
        kapture0writer = NAudio.Wave.WaveFileWriter(tz2+"."+str(0)+".loopback.wav",kapture0.WaveFormat)
        print(kapture0writer)
        
        #kapture0.DataAvailable += kapture0writer
        kapture0.DataAvailable += w0wt
        kapture0.StartRecording()
        
    if 1 in checkedtorecloopback:
        global kapture1
        kapture1 = NAudio.Wave.WasapiLoopbackCapture(alist[1])
        global kapture1writer
        kapture1writer = NAudio.Wave.WaveFileWriter(tz2+"."+str(1)+".loopback.wav",kapture1.WaveFormat)
        kapture1.DataAvailable += w1wt
        kapture1.StartRecording()
        
    if 2 in checkedtorecloopback:
        global kapture2
        kapture2 = NAudio.Wave.WasapiLoopbackCapture(alist[2])
        global kapture2writer
        kapture2writer = NAudio.Wave.WaveFileWriter(tz2+"."+str(2)+".loopback.wav",kapture2.WaveFormat)
        kapture2.DataAvailable += w2wt
        kapture2.StartRecording()
        
    if 3 in checkedtorecloopback:
        global kapture3
        kapture3 = NAudio.Wave.WasapiLoopbackCapture(alist[3])
    if 4 in checkedtorecloopback:
        global kapture4
        kapture4 = NAudio.Wave.WasapiLoopbackCapture(alist[4])
    if 5 in checkedtorecloopback:
        global kapture5
        kapture4 = NAudio.Wave.WasapiLoopbackCapture(alist[5])
    if 6 in checkedtorecloopback:
        global kapture6
        kapture4 = NAudio.Wave.WasapiLoopbackCapture(alist[6])
    if 7 in checkedtorecloopback:
        global kapture7
        kapture4 = NAudio.Wave.WasapiLoopbackCapture(alist[7])
    ####pdb.set_trace()
        gorecordA()
        
        '''
    for zzz in checkedtorecloopback:
        globals()["kapture"+str(zzz)] = NAudio.Wave.WasapiLoopbackCapture(alist[zzz])
        import datetime
        timestampz2 = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        globals()["kapturewriter"+str(zzz)] = NAudio.Wave.WaveFileWriter(timestampz2 + "." + str(zzz) + ".loopback.wav", globals()["kapture"+str(zzz)].WaveFormat)
        '''
        
            
    '''
    selektion = input("which playback device to record with wasapi loopback?\n>->")
    #here you are supposed to input the playback device to record.
    try:
        #global globals()["waveIn" + str(xx)] 
         = NAudio.Wave.WasapiLoopbackCapture(niceout.get_Item(selektion))
        print(kapture)
        import datetime
        timestampz2 = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        kapturewriter = NAudio.Wave.WaveFileWriter(timestampz2 + ".loopback.wav", kapture.WaveFormat)
        #need to specify the right waveformat based on the source
        def kw0(sender,e):
            kapturewriter.WriteData(e.Buffer,0,e.BytesRecorded)
            kapturewriter.Flush()
        #kapture.DataAvailable += kapturewriter
        kapture.DataAvailable += kw0
        kapture.StartRecording()
    except:
        pass
        '''
    
    
########v
def goLPBK(shelf):
    #resultzzz = NAudio.CoreAudioApi.MMDeviceEnumerator.EnumerateAudioEndPoints()
    objekt = NAudio.CoreAudioApi.MMDeviceEnumerator() #doing this with () was an important step
    piece1 = NAudio.CoreAudioApi.DataFlow.All
    piece2 = NAudio.CoreAudioApi.DeviceState.All
    ##subob = objekt.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.All, NAudio.CoreAudioApi.DeviceState.All)
    #NAudio.CoreAudioApi.DeviceState.Communications NAudio.CoreAudioApi.DeviceState.Console NAudio.CoreAudioApi.DeviceState.Multimedia
    
    #enumeratedresults = NAudio.CoreAudioApi.MMDeviceEnumerator.EnumerateAudioEndPoints(piece1,piece2)
    try:
        #eresult = NAudio.CoreAudioApi.MMDeviceEnumerator.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.All, NAudio.CoreAudioApi.DeviceState.All)
        ##nice1 = objekt.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.All, NAudio.CoreAudioApi.DeviceState.All)
        
        ##nice1 = objekt.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.All, NAudio.CoreAudioApi.DeviceState.Active)
        nicerec = objekt.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.Capture, NAudio.CoreAudioApi.DeviceState.Active)
        niceout = objekt.EnumerateAudioEndPoints(NAudio.CoreAudioApi.DataFlow.Render, NAudio.CoreAudioApi.DeviceState.Active)
        #count1 = nice1.get_Count()
        count1 = nicerec.get_Count()
        count2 = niceout.get_Count()
        print("ok")
        print("---> " + str(count1) + " recording devices:")
        for xxx in range(count1):
            #print(nicerec.get_Item(xxx).get_DeviceFriendlyName())
            print(str(xxx) + ": " + nicerec.get_Item(xxx).get_DeviceFriendlyName())
        print("----> " + str(count2) + " playback devices:")
        for xxxx in range(count2):
            #print(niceout.get_Item(xxxx).get_DeviceFriendlyName())
            print(str(xxxx) + ": " + niceout.get_Item(xxxx).get_DeviceFriendlyName())
    except:
        pass
        print("goLPBK failed somehow.")
        #pdb.set_trace()
    selektion = input("which playback device to record with wasapi loopback?\n>->")
    ##77
    pdb.set_trace()
    #here you are supposed to input the playback device to record.
    try:
        kapture = NAudio.Wave.WasapiLoopbackCapture(niceout.get_Item(selektion))
        print(kapture)
        import datetime
        timestampz2 = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        kapturewriter = NAudio.Wave.WaveFileWriter(timestampz2 + ".loopback.wav", kapture.WaveFormat)
        #need to specify the right waveformat based on the source
        def kw0(sender,e):
            kapturewriter.WriteData(e.Buffer,0,e.BytesRecorded)
            kapturewriter.Flush()
        #kapture.DataAvailable += kapturewriter
        kapture.DataAvailable += kw0
        kapture.StartRecording()
    except:
        pass
    #pdb.set_trace()
    #https://csharp.hotexamples.com/examples/NAudio.CoreAudioApi/MMDeviceEnumerator/-/php-mmdeviceenumerator-class-examples.html
    #pdb.set_trace()
########^
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
    #AudioChecker is an AudioCheckList object
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
        waveIn1.DataAvailable += wave1write
        waveIn1.StartRecording()
    if 2 in checkedlist:
        waveIn2.DataAvailable += wave2write
        waveIn2.StartRecording()
    if 3 in checkedlist:
        waveIn3.DataAvailable += wave3write
        waveIn3.StartRecording()
    if 4 in checkedlist:
        waveIn4.DataAvailable += wave4write
        waveIn4.StartRecording()
    if 5 in checkedlist:
        waveIn5.DataAvailable += wave5write
        waveIn5.StartRecording()
    if 6 in checkedlist:
        waveIn6.DataAvailable += wave6write
        waveIn6.StartRecording()
    if 7 in checkedlist:
        waveIn7.DataAvailable += wave7write
        waveIn7.StartRecording()
    if 8 in checkedlist:
        waveIn8.DataAvailable += wave8write
        waveIn8.StartRecording()
    if 9 in checkedlist:
        waveIn9.DataAvailable += wave9write
        waveIn9.StartRecording()
    if 10 in checkedlist:
        waveIn10.DataAvailable += wave10write
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
