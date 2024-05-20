import asyncio
from json import dumps

from protocol import TCPAsyncSocketConnection, Connection
from widgets import widgets

async def handler(reader, writer):
    try:
        conn = TCPAsyncSocketConnection()
        conn.writer = writer
        conn.reader = reader

        pkg = await conn.read_buffer()

        if pkg.read_varint() != 0:
            raise Exception("invailid protocol")
        
        pkg.read_varint()
        data = Connection()
        data.received = b"".fromhex(pkg.read_utf().split(".")[0])
        widget_id = data.read_varint()
        pkg.read_ushort()

        if pkg.read_varint() != 1:
            raise Exception("Status not asked")

        while True:
            pkg = await conn.read_buffer()
            action = pkg.read_varint()

            if action == 0:
                data = Connection()
                data.write_varint(0)
                data.write_utf(dumps(await widgets[widget_id](data, conn)))
                conn.write_buffer(data)
            elif action == 1:
                data = Connection()
                data.write_varint(1)
                data.write_long(pkg.read_long())
                conn.write_buffer(data)
            else:
                break
    except OSError:
        pass
    finally:
        writer.close()


async def main():
    await asyncio.start_server(handler, '0.0.0.0', 25565)
    await asyncio.Event().wait()
    
asyncio.run(main())