from protocol import Connection, TCPAsyncSocketConnection

async def display_ip(args: Connection, conn: TCPAsyncSocketConnection):
    return {
        "version": {"name": "", "protocol": 0},
        "players": {"max": 0, "online": 0},
        "description": {
            "text": "Your IP: "+conn.writer.get_extra_info("peername")[0]
        }
    }