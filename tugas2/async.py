#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio2.py
# Asynchronous I/O inside an "asyncio" coroutine.

import asyncio, zen_utils
import sys
from audioop import add

value = {}

@asyncio.coroutine
def handle_conversation(reader, writer):
    address = writer.get_extra_info('peername')
    value[address] = 0
    print('Accepted connection from {}'.format(address))
    while True:
        data = b''
        while not data.endswith(b'.'):
            more_data = yield from reader.read(4096)
            if not more_data:
                if data:
                    print('Client {} sent {!r} but then closed'
                          .format(address, data))
                else:
                    print('Client {} closed socket normally'.format(address))
                return
            data += more_data
        data = str(data,encoding="ascii")
        cmd = data.split()
        if (cmd[0] == "ADD"):
            value[address] += int(cmd[1][:-1])
        elif (cmd[0] == "DEC"):
            value[address] -= int(cmd[1][:-1])
        else:
            print("error")
            sys.exit(0)
        writer.write(construct_msg(value[address]))

def construct_msg(sum):
    msg = "value = : " + str(sum)
    len_msg = b"%03d" % (len(msg),)
    msg = len_msg + bytes(msg,encoding="ascii")
    return msg

if __name__ == '__main__':
    address = zen_utils.parse_command_line('asyncio server using coroutine')
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conversation, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
