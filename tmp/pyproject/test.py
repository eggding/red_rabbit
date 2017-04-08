import socket
so = socket.create_connection(("127.0.0.1", 10242))
so.send("dslf")