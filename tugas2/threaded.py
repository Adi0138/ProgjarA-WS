#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_threaded.py
# Using multiple threads to serve several clients in parallel.

from audioop import add
from email import message
from klien_paralel import recvall
import zen_utils
from threading import Thread
import sys

value = {}

def handle_connection(listener):
    while True:
        sock,address = listener.accept()
        value[address] = 0
        print('Accepted connection from {}'.format(address))
        try:
            while True:
                handle_requests(sock,address)
        except EOFError:
            # msg = construct_msg(value[address])
            # sock.sendall(msg)
            print('Client socket to {} has closed'.format(address))
        except Exception as e:
            print('Client {} error: {}'.format(address,e))
        finally:
            sock.close()

def construct_msg(sum):
    msg = "value = : " + str(sum)
    len_msg = b"%03d" % (len(msg),)
    msg = len_msg + bytes(msg,encoding="ascii")
    return msg

def handle_requests(sock,address):
    sum = 0
    message = zen_utils.recv_until(sock,b'.')
    message = str(message,encoding="ascii")
    cmd = message.split()
    # print(cmd)
    if (cmd[0] == "ADD"):
        sum += int(cmd[1][:-1])
    elif (cmd[0] == "DEC"):
        sum -= int(cmd[1][:-1])
    else:
        print("error")
        sys.exit(0)
    value[address] += sum
    msg = construct_msg(value[address])
    sock.sendall(msg)

def start_threads(listener, workers=4):
    t = (listener,)
    for i in range(workers):
        Thread(target=handle_connection, args=t).start()

if __name__ == '__main__':
    address = zen_utils.parse_command_line('multi-threaded server')
    listener = zen_utils.create_srv_socket(address)
    start_threads(listener)
