# -*- coding: utf-8 -*-

import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='root', database='medical')
try:
    cursor = conn.cursor()
    failureUrls = open('./FailureUrl.log', 'r')
    for line in failureUrls.readlines():
        insertStr = "\'" + line[line.find('https'):line.find(".html")].strip() + ".html\'"
        insertSQL = "insert into source_url(url) values(%s)"
        insertData = [insertStr]
        cursor.execute(insertSQL,insertData)
        conn.commit()
    cursor.close()
except mysql.connector.Error as e:
    print('connect fails!{}'.format(e))
