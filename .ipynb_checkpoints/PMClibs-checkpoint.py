#When run from your IPython profile, or using the %run -i PMCLibs.py command within your notebook, this file will load the necessary modules for PMC labs and define a few helper functions for working with audio files.

#import helpful stuff:
from __future__ import division, print_function, absolute_import
import scipy.constants as const
import scipy
from scipy.io import wavfile
from scipy import signal
from IPython.core.display import HTML
import numpy as np
import struct
import warnings
import matplotlib.pyplot as plt
import StringIO
import base64

# WavPlayer adapted from http://nbviewer.ipython.org/github/Carreau/posts/blob/master/07-the-sound-of-hydrogen.ipynb
# this is a wrapper that take a filename and publish an html <audio> tag to listen to it
def WavPlayer(data, rate):
    """ will display HTML 5 audio player for compatible browser
        
        The browser need to know how to play wav through html5.
        There is no autoplay to prevent file playing when the browser opens
        
        Adapted from SciPy.io.
        """
    
    buffer = StringIO.StringIO()
    buffer.write(b'RIFF')
    buffer.write(b'\x00\x00\x00\x00')
    buffer.write(b'WAVE')
    
    buffer.write(b'fmt ')
    if data.ndim == 1:
        noc = 1
    else:
        noc = data.shape[1]
    bits = data.dtype.itemsize * 8
    sbytes = rate*(bits // 8)*noc
    ba = noc * (bits // 8)
    buffer.write(struct.pack('<ihHIIHH', 16, 1, noc, rate, sbytes, ba, bits))
    
    # data chunk
    buffer.write(b'data')
    buffer.write(struct.pack('<i', data.nbytes))
    
    if data.dtype.byteorder == '>' or (data.dtype.byteorder == '=' and sys.byteorder == 'big'):
        data = data.byteswap()
    
    buffer.write(data.tostring())
    #    return buffer.getvalue()
    # Determine file size and place it in correct
    #  position at start of the file.
    size = buffer.tell()
    buffer.seek(4)
    buffer.write(struct.pack('<i', size-8))
    
    val = buffer.getvalue()
    
    src = """
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Simple Test</title>
        </head>
        
        <body>
        <audio controls="controls" style="width:600px" >
        <source controls src="data:audio/wav;base64,{base64}" type="audio/wav" />
        Your browser does not support the audio element.
        </audio>
        </body>
        """.format(base64=base64.encodestring(val))
    display(HTML(src))

def play(data, rate=44100) :
    """ Creates an HTML audio player to play an array of samples stored in data.
        
        Data should be an array of sample values
        Each sample expected to be floats in the range -1 to 1
        Rate is expressed in Hz, default is 44100
        """
    tmp1 = 2**15 * data
    tmp  = tmp1.astype(np.int16)
    WavPlayer(tmp, rate)

def wavReadMono(filename):
    """ Reads a .wav file into a single array of samples.
        
        Sample data will be floats in the range -1 to 1
        """
    [rate, samps] = wavfile.read(filename)
    if (size(shape(samps)) == 1) :
        s = samps.astype(np.double)/2**15
    else:
        modsamps = samps[:,0].astype(np.double)/(2**15)
        for i in range(1, samps.shape[1]) :
            modsamps = modsamps + (samps[:,i].astype(np.double))/(2**15)
        modsamps = modsamps / samps.shape[1]
        s = modsamps
    
    return s;

def wavReadMulti(filename):
    """ Reads a .wav file into a multidimensional array.
        
        If called as data = wavReadMulti then
        data[:,i] will be an array storing samples for channel i
        Sample data will be floats in the range -1 to 1
        
        """
    [rate, samps] = wavfile.read(filename)
    if (size(shape(samps)) == 1) :
        s = samps.astype(np.double)/2**15
    else :
        modsamps = np.ndarray(shape=shape(samps),dtype=np.double)
        for i in range(0, samps.shape[1]) :
            modsamps[:,i] = (samps[:,i].astype(np.double))/(2**15)
        s = modsamps
    return s;

def wavWrite(filename, data, rate=44100):
    """ Writes data to a .WAV file """
    wavfile.write(filename, rate, (2**15*data).astype(np.int16))
