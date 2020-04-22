import math
import numpy as np
import scipy.io.wavfile as wave
from numpy.fft import fft
import time

import threading
import queue



class ThreadedWork:
    def __init__(self,work,nbthreads=5):
        self.nbthreads = nbthreads
        self.q = queue.Queue()
        self.work = work
        self.threads = []
        for i in range(self.nbthreads):
            t = threading.Thread(target=self.worker,args=(i,))
            t.start()
            self.threads.append(t)

    def worker(self,n):
        while True:
            item = self.q.get()
            if item is None:
                break
            print(item['path'])
            self.work(**item)
            self.q.task_done()

    def submit_work(self,**item):
        self.q.put(item)

    def wait_end(self):
        self.q.join()
        for i in range(self.nbthreads):
            self.q.put(None)
        for t in self.threads:
            t.join()


window = 0.4

rate,data = wave.read('audio.wav')
data = np.mean(data, axis=1)
n = data.size
duree = 1.0*n/rate




from statistics import mean
from PIL import Image, ImageDraw

params = dict(
    width = 610,
    height = 86,
    bar_width_pct = 0.7,
    freq_step = 10,
    min_freq = 100,
    max_freq = 1000
)



def _get_histo(data, rate, pos, duree):
    if pos>duree/2:
        pos = pos-duree/2
    start = int(pos*rate)
    stop = int((pos+duree)*rate)

def get_histo(path,data,rate,width,height,bar_width_pct,freq_step,min_freq, max_freq):
    bar_width = int(bar_width_pct * freq_step * (width/(max_freq-min_freq)))
    spectre = np.absolute(fft(data))
    spectre = spectre/spectre.max()
    n = spectre.size
    freq = np.arange(n)*1.0/n*rate
    values = {}
    i = 0
    for i,f in enumerate(freq):
        fv = int(f/freq_step)*freq_step
        sv = spectre[i]
        if sv:
            values[fv] = values.get(fv,[]) + [sv]

    values = list((k,mean(v)) for k,v in sorted(values.items(),key=lambda x:x[0]))
    o_img = Image.open('fond.png')
    o_draw = ImageDraw.Draw(o_img)
    img = Image.new('RGBA', (width,height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    for i,v in enumerate(values):
        f,s = v
        if f<min_freq or f>=max_freq:
            continue
        x = int((f-min_freq)*width/(max_freq-min_freq))
        y = int((1-s)*height)
        draw.rectangle(((x, y), (x+bar_width, height)), fill="white")
    o_img.paste(img,(355,484),img)
    #img.save(path,'PNG')
    o_img.save(path,'PNG')
    return True



tw = ThreadedWork(get_histo,20)

i = 0
pos = 0
step = 1/30.0
duree = 60
#duree = 10
while pos<=duree:
    _pos = pos-window/2 if pos>window/2 else pos
    start = int(_pos*rate)
    stop = int((_pos+window)*rate)
    tw.submit_work(path="imgs/test%d.png" % i, data=data[start:stop],rate=rate,**params)
    i += 1
    pos += step
tw.wait_end()
