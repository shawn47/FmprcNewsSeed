#coding=utf-8

from sys import argv

from NewsSeedThread import fetchNews
from checkExpiredNews import checkExpiredNews

if __name__ == '__main__':
	script, method = argv
	print(method)
	try:
		if method == "fetchNews":
			fetchNews()
		else:
			checkExpiredNews()
	except Exception as e:
		raise e
