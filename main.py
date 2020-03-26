from threading import Thread
from queue import Queue
import time
from lights import Lights
from akai import Akai
import sys

ip = sys.argv[1]

pasek = Lights(ip)

akai = Akai()

"""
Read knob values and send the GET to set the Lights.

Monitor the knobs values. If anyone changes send a GET to set the lights. Wait 100ms before next packet.

TODO:
- Detect incoming MIDI data at the mido level?
- Do something about this ugly time.sleep(0.1)
- Introduce an extrapolating method
:return:
"""

def producer(output_queue):
    [red, green, blue] = [0, 0, 0]
    while True:
        [r, g, b] = [i * 2 for i in akai.get_knobs()][:3] # Get RGB values from the AKAI
        if [red, green, blue] == [r, g, b]:
            continue
        output_queue.put([r, g, b])
        time.sleep(0.1)                               # Do something about it!

def consumer(input_queue):
    while True:
        [r, g, b] = input_queue.get()

        pasek.set_colors(r, g, b)

        input_queue.task_done() 

if __name__ == '__main__':
    q = Queue()
    Thread(target=producer, args=(q,)).start()
    Thread(target=consumer, args=(q,)).start()
    Thread(target=akai.listen).start()
