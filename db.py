# -*- coding: utf-8 -*-

import pymysql

# cur.execute('create database if not exists fmprc_news_seed')
# conn.select_db('fmprc_news_seed')
# cur.execute("""
# 	CREATE TABLE news_seeds (
# 		id INT NOT NULL AUTO_INCREMENT,
# 		title VARCHAR(256) NOT NULL,
# 		news_hash VARCHAR(32) NOT NULL,
# 		url TEXT NOT NULL,
# 		media VARCHAR(32) NOT NULL,
# 		expired_date TIMESTAMP NOT NULL,
# 		is_expired INT NOT NULL DEFAULT 0,
# 		created TIMESTAMP NULL,
# 		updated TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
# 		PRIMARY KEY (id),
# 		UNIQUE KEY (news_hash)
# 	);
# 	""")

class CrawlerDB:
	def insertNewsBatch(self, news_objs):
		try:
			conn = pymysql.connect(host = 'localhost',user = 'root',passwd = 'qwer1234',db = 'fmprc_news_seed',port = 3306,charset = 'utf8')
			cur = conn.cursor()
			 
			news_list = []
			for i in news_objs:
				news_list.append((i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
				 
			cur.executemany('insert ignore into news_seeds (`title`, `news_hash`, `url`,' + 
				'`media`, `expired_date`, `created`, `country_a`, `country_b`) ' + 
				'values (%s, %s, %s, %s, %s, %s, %s, %s)', news_list)
		 
			conn.commit()
			cur.close()
			conn.close()
		except pymysql.InternalError as error:
			code, message = error.args
			print(">>>>>>>>>>>>> %s %s", code, message)

	def findExpiredNews(self, target_date):
		result = []
		try:
			conn = pymysql.connect(host = 'localhost',user = 'root',passwd = 'qwer1234',db = 'fmprc_news_seed',port = 3306,charset = 'utf8')
			cur = conn.cursor()
				 
			cur.execute('select id from news_seeds where expired_date < %s', target_date)
			rows = cur.fetchall()

			conn.commit()
			cur.close()
			conn.close()
			
			result += rows
		except pymysql.InternalError as error:
			code, message = error.args
			print(">>>>>>>>>>>>> %s %s", code, message)
		finally:
			return result

	def setNewsExpired(self, news_id_list):
		try:
			conn = pymysql.connect(host = 'localhost',user = 'root',passwd = 'qwer1234',db = 'fmprc_news_seed',port = 3306,charset = 'utf8')
			cur = conn.cursor()
				 
			cur.executemany('update news_seeds set `is_expired` = 1 where id = %s', news_id_list)
		 
			conn.commit()
			cur.close()
			conn.close()
		except pymysql.InternalError as error:
			code, message = error.args
			print(">>>>>>>>>>>>> %s %s", code, message)
