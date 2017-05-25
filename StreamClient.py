import io
import socket
import struct
from PIL import Image
import os
import sys
import params
import time


class StreamClient():

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self, target, port):
        self.server_socket.connect((target, port))
        self.connection = server_socket.makefile('rwb')

    def send_command(self, cmd, arg=None):
        self.connection.write(struct.pack('<c', bytes(cmd, encoding='ascii')))
        if arg != None:
            if type(arg) == str:
                self.connection.write(struct.pack('<L', len(arg)))
                self.connection.write(
                            struct.pack('<%ds'%len(arg),
                                bytes(arg, encoding='ascii')))
            elif type(arg) == float:
                self.connection.write(struct.pack('<L', struct.calcsize('<f')))
                self.connection.write(struct.pack('<f', arg))
            elif type(arg[0]) == float and type(arg[1]) == float:
                self.connection.write(struct.pack('<L', struct.calcsize('<ff')))
                self.connection.write(struct.pack('<ff', arg[0], arg[1]))
            else:
                print('Invalid argument: %s'%arg)
                return 0
        self.connection.flush()
        return 1

    image_stream = io.BytesIO()
    def get_image(self):
        self.send_command('p')
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        self.image_stream.seek(0)
        self.image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        self.image_stream.seek(0)
        return Image.open(self.image_stream)

    pickle_stream = io.BytesIO()
    def get_data(self):
        pass
