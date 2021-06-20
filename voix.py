import numpy as np
import sounddevice as sd

assert np

usage_line = ' press <enter> to quit, +<enter> or -<enter> to change scaling '
columns = 80


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


appareil = "Casque (FreeBuds 3 Hands-Free A"
print(sd.query_devices(kind='input'))
samplerate = 44100


def coucou(indata, frames, time, status):
    if type(time) is None or type(status) is None or type(frames) is None:
        pass
    somme = 0
    maximum = indata[0]
    minimum = indata[0]
    for i in indata:
        somme += i[0]
        if i[0] > maximum:
            maximum = i
        if i[0] < minimum:
            minimum = i
    if maximum > 0.001:
        print(f"\033[91m{maximum}")
    else:
        print(f"\033[92m{maximum}")


with sd.InputStream(device=appareil, channels=1, callback=coucou,
                    blocksize=int(2500),
                    samplerate=samplerate):
    while True:
        try :
            continue
        except Exception as e:
            print(e)
