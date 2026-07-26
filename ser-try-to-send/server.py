#!/usr/bin/python3

import random
import socket

hex_characters = b"0123456789ABCDEF"
random.seed()
characters=bytearray(65536);
colors=bytearray(65536);
for ii in range(len(characters)):
    characters[ii] = 0x20
    colors[ii] = 0x1f
for (character, color) in [(0x23, 0x99), (0x2a, 0x9a), (0x2a, 0x9e), (0x2a, 0x96)]:
    for _ in range(2000):
        ii = random.randrange(len(characters))
        characters[ii] = character
        colors[ii] = color
for yy in range(16):
    for xx in range(16):
        ii = 256*16*yy+16*xx
        characters[ii] = hex_characters[yy]
        characters[ii+1] = hex_characters[xx]
        colors[ii] = 0x05
        colors[ii+1] = 0x05
ss = socket.create_server(("127.0.0.1", 12345), reuse_port=True)
try:
    while True:
        cs, addr = ss.accept()
        try:
            print("Connected to %s" % str(addr))
            cs.send(b"\x93\x8e\x05")
            last_color = 0x05
            current_x = 0
            current_y = 0
            while True:
                sendbuf = bytearray(b"\x13")
                for sy in range(25):
                    for sx in range(40):
                        if (sx == 39) and (sy == 24):
                            continue
                        character = None
                        color = None
                        if (sx == 19) and (sy == 12):
                            character = 0xda
                            color = 0x9c
                        else:
                            mx = (current_x+sx)%256
                            my = (current_y+sy)%256
                            mi = 256*my+mx
                            character = characters[mi]
                            color = colors[mi]
                        if last_color != color:
                            last_color = color
                            sendbuf.append(color)
                        sendbuf.append(character)
                cs.send(sendbuf)
                received = cs.recv(4096)
                if len(received) == 0:
                    break
                for cc in received:
                    match cc:
                        case 65: # A
                            current_x = current_x + 255
                        case 68: # D
                            current_x = current_x + 1
                        case 83: # S
                            current_y = current_y + 1
                        case 87: # W
                            current_y = current_y + 255
                current_x = current_x%256
                current_y = current_y%256
        except BrokenPipeError:
            pass
        except ConnectionResetError:
            pass
        finally:
            cs.close()    
            print("Closed %s" % str(addr))
finally:
        ss.close()
