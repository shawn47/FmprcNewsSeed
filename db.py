# -*- coding: utf-8 -*-

import pymysql

class CrawlerDB:
	def insertNewsBatch(self, newsObjs):
		try:
			conn = pymysql.connect(host = 'localhost',user = 'root',passwd = 'qwer1234',db = 'PressStat',port = 3306,charset = 'utf8')
			cur = conn.cursor()
			 
			cur.execute('create database if not exists fmprc_news_seed')
			conn.select_db('fmprc_news_seed')
			cur.execute("""
				CREATE TABLE news_seeds (
					id INT NOT NULL AUTO_INCREMENT,
					title VARCHAR(256) NOT NULL,
					news_hash VARCHAR(32) NOT NULL,
					url TEXT NOT NULL
					media VARCHAR(32) NOT NULL,
					expired_date TIMESTAMP NOT NULL,
					created TIMESTAMP NULL DEFAULT 0,
					updated TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
					PRIMARY KEY (id),
					UNIQUE KEY (news_hash)
				);
				""")
			 
			news_list = []
			for i in newsObjs:
				values.append((i[0], i[1], i[2], i[3], i[4]))
				 
			cur.executemany('insert into test values(%s, %s, %s, %s, %s)', values)
		 
			cur.execute('update test set info="I am rollen" where id=3')
		 
			conn.commit()
			cur.close()
			conn.close()
		except MySQLError as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))
