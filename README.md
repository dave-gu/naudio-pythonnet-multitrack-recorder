# naudio-pythonnet-multitrack-recorder
simultaneous multitrack recording of wav files using naudio &amp; pythonnet -- for multiple devices -- &amp; record poly wav from ASIO

First of all what this project does is provide a frontend to enumerate and record from recording inputs on Windows to stereo wav files.<br>
What we have achieved is simultaneous "multitrack" recording from multiple audio usb interfaces.<br>
-Some musician or remixer may find themselves in a situation where they want to record from two or more recording devices.<br>
For instance, you have an audio interface with a guitar and a synth, and another differently named interface which is your usb microphone.<br>
You cannot accomplish this recording scenario using Ableton, Fruity Loops, etc. without using ASIO, which functions in an exclusive mode.<br>
If you have configured your devices in those DAWs without using ASIO then you will have the ability to access 2 channel in, 2 channel out.<br>
However, it is totally possible to access all of your devices non exclusively with multiple programs,<br>
so based on that, I concluded it was definitely possible to do this particular type of simultaneous recording without using ASIO.<br>
<br>
<br>
Anyways, your musician or remixer might also want to record a playing audio stream to synchronize it.<br>
Recording the playing audio stream will be accomplished through the WasapiLoopbackCapture object in NAudio.<br>
Since we can now record multiple streams of audio input from different devices,<br>
and also record the playback audio with the wasapi loopback capture, this method will provide us with<br>
a multitrack recording of the session as uncompressed wav audio files.<br>
<br>
First of all this is a Python based program. But we get to utilize the NAudio C# library by importing its DLL via pythonnet.<br>
I have also customized this DLL by building from the NAudio source to remove an error message that I received during development.<br>
We also utilize the WxPython library.  The program, when opened, begins to display the UI using WxPython.<br>
The recordings of the audio input devices are accomplished by creating the NAudio.Wave.WaveIn<br>
and subscribing an event handler function using the += operator.  e.g. WaveInNAMED.DataAvailable += writerfunc<br>
The event handler function receives the event, which contains a buffer array of bytes.  Check the wave0write function etc in the source py files.<br>
To better understand the objects within the NAudio namespace, use your ildasm.exe to open the NAudio.dll.<br>
