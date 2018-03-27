#coding=utf-8# -*- coding: UTF-8 -*-
 
import Queue
import threading
import time

class NewsSeedThread (threading.Thread):
	def __init__(self, threadID, keyWord, q):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = keyWord
		self.q = q
	def run(self):
		print "Starting " + self.name
		process_data(self.name, self.q)
		print "Exiting " + self.name

def process_data(keyWord, q):
	while not exitFlag:
		queueLock.acquire()
		if not workQueue.empty():
			data = q.get()
			queueLock.release()
			print "%s processing %s" % (keyWord, data)
		else:
			queueLock.release()
		time.sleep(1)

exitFlag = 0
threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1

if __name__ == '__main__':
	for tName in threadList:
		thread = NewsSeedThread(threadID, tName, workQueue)
		thread.start()
		threads.append(thread)
		threadID += 1

	queueLock.acquire()
	for word in nameList:
		workQueue.put(word)
	queueLock.release()

	while not workQueue.empty():
		pass
 
	exitFlag = 1
	 
	for t in threads:
		t.join()
	print "Exiting Main Thread"