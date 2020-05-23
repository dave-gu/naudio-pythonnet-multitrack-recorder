# naudio-pythonnet-multitrack-recorder
simultaneous multitrack recording of wav files using naudio &amp; pythonnet -- for multiple devices -- &amp; record poly wav from ASIO

First of all what this project does is provide a frontend to enumerate and record from recording inputs on Windows to stereo wav files.
What we have achieved is simultaneous "multitrack" recording from multiple audio usb interfaces.
-Some musician or remixer may find themselves in a situation where they want to record from two or more recording devices.
For instance, you have an audio interface with a guitar and a synth, and another differently named interface which is your usb microphone.
You cannot accomplish this recording scenario using Ableton, Fruity Loops, etc. without using ASIO, which functions in an exclusive mode.
If you have configured your devices in those DAWs without using ASIO then you will have the ability to access 2 channel in, 2 channel out.
However, it is totally possible to access all of your devices non exclusively with multiple programs,
so based on that, I concluded it was definitely possible to do this particular type of simultaneous recording without using ASIO.


Anyways, your musician or remixer might also want to record a playing audio stream to synchronize it.
Recording the playing audio stream will be accomplished through the WasapiLoopbackCapture object in NAudio.
Since we can now record multiple streams of audio input from different devices,
and also record the playback audio with the wasapi loopback capture, this method will provide us with
a multitrack recording of the session as uncompressed wav audio files.

First of all this is a Python based program. But we get to utilize the NAudio C# library by importing its DLL via pythonnet.
I have also customized this DLL by building from the NAudio source to remove an error message that I received during development.
We also utilize the WxPython library.  The program, when opened, begins to display the UI using WxPython.
The recordings of the audio input devices are accomplished by creating the NAudio.Wave.WaveIn
and subscribing an event handler function using the += operator.  e.g. WaveInNAMED.DataAvailable += writerfunc
The event handler function receives the event, which contains a buffer array of bytes.  Check the wave0write function etc in the source py files.
To better understand the objects within the NAudio namespace, use your ildasm.exe to open the NAudio.dll.
