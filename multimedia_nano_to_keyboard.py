
import time
import serial
import pynput
from pynput.keyboard import Controller

keyboard = Controller()

ir = ['FF22DD', 'FF02FD', 'FFC23D', 'FFE01F', 'FFA857', 'FF906F']
# names = ['MEDIA_PREVIOUS', 'MEDIA_NEXT', 'MEDIA_PLAY_PAUSE', 'MEDIA_VOLUME_DOWN', 'MEDIA_VOLUME_UP', 'MEDIA_VOLUME_MUTE']
kb = [269025046, 269025047, 269025044, 269025041, 269025043, 269025042]
# 269025045, stop

commands = {ir[i]: kb[i] for i in range(len(ir))}

def read():
    with serial.Serial('/dev/ttyUSB0', 9600) as ser:
        last = None
        while True:
            in_c = ser.readline().strip().decode('utf-8')
            print(in_c)
            current_milli_time = int(round(time.time() * 1000))
            if in_c in commands:
                print("ok")
                kb_c = pynput.keyboard._xorg.KeyCode(commands[in_c])
                keyboard.press(kb_c)
                time.sleep(0.3)
                keyboard.release(kb_c)
                last = kb_c
                last_time = int(round(time.time() * 1000))
            elif in_c == 'FFFFFFFF' and last is not None:
                if current_milli_time - last_time < 100:
                    print('block')
                    continue
                print(last_time, current_milli_time)
                print('repeat')
                keyboard.press(kb_c)
                time.sleep(0.1)
                keyboard.release(kb_c)
                last_time = current_milli_time
            else:
                last = None
    
if __name__ == '__main__':
    while True:
        try:
            read()
        except Exception as e:
            print(e)
            time.sleep(5)

