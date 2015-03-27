#!/usr/bin/env python

import numpy as np
import pyaudio
import matplotlib.pyplot as plt

from music_base import *

if __name__ == '__main__':
    root = Note('G', 3)
    scale = Scale(root, [2, 2, 1, 2, 2, 2, 1])

    sa_note = scale.get(0)
    ri_note = scale.get(1)
    ga_note = scale.get(2)
    ma_note = scale.get(3)
    pa_note = scale.get(4)
    da_note = scale.get(5)
    ni_note = scale.get(6)
    usa_note = scale.get(7)
    uri_note = scale.get(8)
    uga_note = scale.get(9)

    sa = rise_flat(sa_note)
    ri = rise_flat(ri_note)
    ga = rise_flat(ga_note)
    ma = rise_flat(ma_note)
    pa = rise_flat(pa_note)
    da = rise_flat(da_note)
    ni = rise_flat(ni_note)
    usa = rise_flat(usa_note)
    uri = rise_flat(uri_note)
    uga = rise_flat(uga_note)

    sa_flat_fall = flat_fall(sa_note)
    ri_flat_fall = flat_fall(ri_note)
    ga_flat_fall = flat_fall(ga_note)
    ma_flat_fall = flat_fall(ma_note)
    pa_flat_fall = flat_fall(pa_note)
    da_flat_fall = flat_fall(da_note)
    ni_flat_fall = flat_fall(ni_note)
    usa_flat_fall = flat_fall(usa_note)
    uri_flat_fall = flat_fall(uri_note)
    uga_flat_fall = flat_fall(uga_note)

    rig = from_next(ri_note, ga_note, 1)
    dag = from_next(da_note, usa_note, 1)
    urig = from_next(uri_note, uga_note, 1)

    chunks = []

    vara_veena = ('ga ga pa , pa , '
                  'dag pa usa , usa , '
                  'urig usa dag dag pa , '
                  'dag pa ga ga rig , '
                  'ga pa da usa dag , '
                  'dag pa ga ga rig , '
                  'ga ga dag pa ga , '
                  'pa ga ga rig sa , '
                  'ga ga ga ga rig ga '
                  'pa ga pa , pa , '
                  'ga ga da pa dag , '
                  'dag pa usa , usa , '
                  'dag uga urig , usa usa '
                  'dag usa dag , dag pa '
                  'ga pa dag usa dag pa '
                  'dag pa ga ga rig sa '
                  'rig ga ga , ga , '
                  'ga rig pa ga rig , '
                  'sa ri sa ga rig sa '
                  'ga ga pa , pa , '
                  'dag pa usa , usa ,').split(' ')

    for swaram in vara_veena:
        if swaram != ',':
            chunks.append(locals()[swaram])
            # Hack ahead!
            if swaram[-1] == 'g':
                prev_note = swaram[:-1]
            else:
                prev_note = swaram
        else:
            chunks.append(locals()[prev_note + '_flat_fall'])

    chunk = np.concatenate(chunks) * 0.25

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    stream.write(chunk.astype(np.float32).tostring())
    stream.close()
    p.terminate()
