import threading

class IPs(object):
	"""
	data structure
	{totalOfIP: int, totalRequest: int, ips: {ip1: count, ip2: count, etc}}
	"""
	def __init__(self):
		self.lock = threading.Lock()
		self.totalOfIP = 0
		self.totalRequest = 0
		self.ips = {}

	def addIps(self, ip):
		""" synchronization """
		self.lock.acquire()
		self.totalRequest += 1

		if ip in self.ips:
			self.ips[ip] += 1
		else:
			self.ips.update({ip: 1})
			self.totalOfIP += 1
		self.lock.release()

	def clearIps(self):
		self.ips.clear()


class IPTrack(object):
	def __init__(self, ips):
		""" ipsObj is an object of IPs """
		self.ipsObj = ips

	def ipAdd(self, ip):
		self.ipsObj.addIps(ip)

	def request_handled(self, ip_address):
		""" Create each thread for each request """
		thread = threading.Thread(target=self.ipAdd, args=(ip_address,))
		thread.start()
		thread.join()

	def top100(self):
		ipsOfTop100 = []
		listOfTop100 = sorted(self.ipsObj.ips.items(), key=lambda x: x[1], reverse=True)[:100]

		""" Extract ip address only """
		for ip, count in listOfTop100:
			ipsOfTop100.append(ip)

		return ipsOfTop100

	def clear(self):
		self.ipsObj.clearIps()
		

""" Initialization """
ips = IPs()
ipTrack = IPTrack(ips)

""" test cases, call request_handled func """
ipTrack.request_handled('1.2.3.4')
ipTrack.request_handled('2.3.4.5')
ipTrack.request_handled('2.3.4.5')
ipTrack.request_handled('3.4.5.6')

""" print out all of ips address requested """
print(ips.ips)

""" print out top 100 IP addresses """
print(ipTrack.top100())

""" clear the all IP stored """
ipTrack.clear()

""" confirm the in-memory storage is empty """
print(ips.ips)