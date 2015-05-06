import socket, string

#HOST = '192.168.1.10'
HOST = 'localhost'
PORT = 25000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

while 1:
	data = s.recv(4096)
	if data:
		print data.split(',')
	else:
		break


print s.recv(4096)

