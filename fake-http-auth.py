import os
import random
import urllib2,urllib
import httplib,time
import threading,Queue

#our sample data
l = ["/login.php","/","/auth.aspx","/authentication.php","/index.php","/index.jsp","/login.jsp","/login.aspx","/login/","/login_secure","/auth/","/index.asp","/index/"]
doms = open(sys.argv[1],"r")
p = ["http","https","ftp"]

#some basic methods to generate random data
def getcreds_user():
	us = ["admin3@hotmail.com","admin@facebook.com","mark.zuckerberg","userwhohatesyour@gmail.com","hatemylife@gmail.com","pfff","duckme","fuckyou","inception","packet_is_a_lie"]
 	return random.choice(us)
def getcreds_pass():
	pa = ["honeydick","kinkydickless","Password","password123","123xxxxx","yolome","orly?","thisisarat","youseendme","packetmonkey","wallofsheeprulez","1337defcon","dickmeon","yorasta","thisisyourmasta","forreal","boomz","ohnow","uksucksyo!","noway"]
	return random.choice(pa)
def get_action():
	act = ["login","auth","pissmeoff","index"]
	return random.choice(act)

def get_random_agent():
	age = ["Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com"]	
	return random.choice(age)

def get_content_type():
	cont = ["application/json","application/x-www-form-urlencoded","multipart/form-data"]
	return random.choice(cont)

queue = Queue.Queue()

#thread instance for queue jobs
class ThreadUrl(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
	 	while True:
			f_domains = self.queue.get()
			url = random.choice(p)+"://"+f_domains.strip("\n")+random.choice(l)
			data = {}
			data['action'] = get_action()
			data['login'] = getcreds_user()
			data['password'] = getcreds_pass()
			url_values = urllib.urlencode(data)
			req = urllib2.Request(url,url_values)
			req.add_header('Cookie', 'PHPSESSIONID=3hab1j2h31abb1jhb3jh5b1k3h3')
			req.add_header('Content-Type',get_content_type())
			req.add_header('User-Agent',get_random_agent())
			req.add_header('Accept','text/*, text/html, text/html;level=1, */*')
			try:
				resp = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
				if e.code == 404 or e.code == 61  or e.code == 60 or e.code == 8:
					self.queue.task_done()
					pass
			except Exception, exx:
				self.queue.task_done()
				pass
			print "done - ", url
			self.queue.task_done()

def main():
    #we want to thread this jobs 
    for i in range(15):
      t = ThreadUrl(queue)
      t.setDaemon(True)
      t.start()
   #populate queue with data   
    for lines in doms:
    	queue.put(lines)
    queue.join()

main()

