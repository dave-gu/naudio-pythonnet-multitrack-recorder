# naudio-pythonnet-multitrack-recorder
simultaneous multitrack recording of wav files using naudio &amp; pythonnet -- for multiple devices -- &amp; record poly wav from ASIO

First of all what this project does is provide a frontend to enumerate and record from recording inputs on Windows to stereo wav files.<br>
Second of all, the zip file is the release.  It's portable... runs on Windows. Unzip the contents and run the program.<br>
What we have achieved is simultaneous "multitrack" recording from multiple audio usb interfaces.<br>
<br>
INSTRUCTIONS:<br>
The left button initiates simultaneous wav recordings of the checked boxes on the left portion.<br>
The waves are recorded timestamped into the folder.  You can end the program to stop recording.<br>
Everything is recorded to the hard disk directly. You do not have to do anything additional to save it from the program's memory.<br>
If you have ASIO devices, they will be shown on the right and you can check one and hit the right button to record a multitrack "poly wav" of all its channels.<br>
<br>
Additional Info - More About The Making Of the Program:<br>
-Some musician or remixer may find themselves in a situation where they want to record from two or more recording devices.<br>
For instance, you have an audio interface with a guitar and a synth, and another differently named interface which is your usb microphone.<br>
You cannot accomplish this recording scenario using Ableton, Fruity Loops, etc. without using ASIO, which functions in an exclusive mode.<br>
If you have configured your devices in those DAWs without using ASIO then you will have the ability to access 2 channel in, 2 channel out.<br>
However, it is totally possible to access all of your devices non exclusively with multiple programs,<br>
so based on that, I concluded it was definitely possible to do this particular type of simultaneous recording without using ASIO.<br>
Well, I have done it, and it was possible all this time.  It might look easy and obvious but apparently it wasn't because you can't find any programs other than n-track studio and obs studio that might have this functionality.  Also check out Purr Data and compare its multiple device audio control panel to the lamer normal one in PD-Extended.  As you can see from this sequence of facts about music technology, you can tell that there is still a lot of room for improvement all around.  DAW programs have succeeded at being VST hosts and offering mixing, sequencing, playback, audio rendering, and plugin hosting capabilites. But, I guess the way they are, they don't seem to support recording multiple audio input devices at the same time. if it is possible to simultaneously multitrack in Windows DAWs, most people are probably going to be using a singular interface with its dedicated ASIO driver, rather than multiple separate devices. But, as a low budget musician you end up having a lot of lower cost usb audio components.  Also, another way that you could duplicate this same effect is by running two programs and using a macro to try to simultaneously click the record buttons.  The setup for that is also somewhat complicated.  Also you can run VSTfx that record, too, that's another thing that could be done.  In that case some plugins have multiple outputs and with some DAWs you should be able to record into the DAW on those tracks, or otherwise use a recorder vst effect.  As far as the actual "multitrack" terminology goes, you can see by the usage of it that like 75% of the time people are just looking for a normal horizontal timeline DAW and have no concern about recording two or more audio tracks simultaneously from differently named devices.  But I think that there are plenty of people out there as well that were also like hmm, i dunno, multitrack should mean actually recording multiple tracks at the same time haha what's up with that? Oh yeah another thing to check out is the FlexASIO driver, that's like ASIO4ALL but it uses nonexclusive modes. That was the problem with ASIO4ALL, it would crash your system. I haven't tried it yet but it sounds like it should work pretty ok eventually or already.<br>
<br>
Also, some other features that I already have happening in C# or that are otherwise deduced possible that I might put in here:<br>
play a file into a vst effect and record the effected output<br>
native code effects that operate on the 32-bit floating stream values<br>
create more & different audio objects within csharp and put them into dlls to import here<br>
<br>
what's confusing right now?<br>
the wasapiloopbackcapture values are floats and i'm trying to convert them to 16-bit and get the data from that, but there's kind of a different push versus pull type event system in play governing the way the audio is transmitted and i can't figure out how to equilibrate its operation to be able to treat the complete thing the same as a WaveIn<br>
i can record the default playback through wasapi capture loopback but i haven't yet figured out how to pass the immdevice enumerator object entries to create the playback capture object so that it refers to and gives the signal from different loopbacks<br>
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
