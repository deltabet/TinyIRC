#Spawns single bot for basic calls. 
#Assume you have compiled as "main".

import socket
import sys
import subprocess
import select
import threading

errornum = 0

def readAllSoFar(proc):
  retVal=p.stdout.read(1) 
  while (select.select([proc.stdout],[],[],0)[0]!=[]):  
    retVal+=proc.stdout.read(1)
  return retVal


def TestMes(sock, message, testtype):
	sock.send(message)
	mes = sock.recv(2048)
	if (mes == ""):
		print testtype + ' error'
		return -1
	else:
		return 1

class Client(threading.Thread):
	def run(self):
		global errornum
		s = socket.socket()
		host = socket.gethostname() 
		port = 6667 
		s.connect((host, port))
		if (TestMes(s, "JOIN xxx", "JOIN without NICK") == -1):
			s.close
			errornum = -1
			return
		print "Pass JOIN without NICK\n"
		s.send('NICK')
		mes = s.recv(2048)
		if (mes[:12] != "PING :FAGGOT"):
			print "Empty NICK error"
			if (mes == ""):
				errornum = -1
			s.close
			return
		print "pass Empty NICK\n"
		s.send('NICK :ONE TWO')
		mes = s.recv(2048)
		mes = mes[:-2]
		if (mes[-7:] != "ONE TWO"):
			print "Long param NICK error"
			if (mes == ""):
				errornum = -1
			s.close
			return	
		print "pass Long param NICK\n"
		if (TestMes(s, "PING", "PING no message") == -1):
			s.close
			errornum = -1
			return
		if (TestMes(s, "JOIN", "JOIN no channel") == -1):
			s.close
			errornum = -1
			return
		if (TestMes(s, "TOPIC", "TOPIC no channel") == -1):
			s.close
			errornum = -1
			return
		if (TestMes(s, "PRIVMSG", "PRIVMSG blank") == -1):
			s.close
			errornum = -1
			return
		if (TestMes(s, "MODE", "MODE blank") == -1):
			s.close
			errornum = -1
			return
		if (TestMes(s, "WHO", "WHO blank") == -1):
			s.close
			errornum = -1
			return
		if (TestMes(s, "PART", "PART blank") == -1):
			s.close
			errornum = -1
			return
		print "pass blank parameters\n"
		errornum = 1
		s.close
		return
		

p = subprocess.Popen(['./main'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.stdin.write("kick\n")
sys.stdout.flush()
mes_stdout = readAllSoFar(p)
print 'start tests\n'
c = Client()
c.start()
c.join()

if (errornum == -1):
	mes_stdout = p.stderr.readline()
	if (mes_stdout == ''):
		print "Likley Segmentation Fault"
	else:
		print(mes_stdout)
elif (errornum == 0):
	print "syntax error"
else:
	print "tests passed"
sys.exit("test over")



