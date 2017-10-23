# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 14:30:19 2017

@author: 刘常
"""

#==============================================================================
# def zero():
#     return "zero"
#  
# def one():
#     return "one"
#  
# def numbers_to_functions_to_strings(argument):
#     switcher = {
#         0: zero,
#         1: one,
#         2: lambda: "two",
#     }
#     # Get the function from switcher dictionary
#     func = switcher.get(argument, lambda: "nothing")
#     # Execute the function
#     return func()
# print numbers_to_functions_to_strings(2)
# #字典映射
#==============================================================================

#L=['PTerror_AM80,PTerror_AP80,PTerror_AM100,PTerror_AP100,PTerror_AM115,PTerror_AP115',
#               'PTerror_BM80,PTerror_BP80,PTerror_BM100,PTerror_BP100,PTerror_BM115,PTerror_BP115',
#               'PTerror_CM80,PTerror_CP80,PTerror_CM100,PTerror_CP100,PTerror_CM115,PTerror_CP115']
#def TerrorDiag(L):
#    print L[0]
#TerrorDiag(L)

import MySQLdb as mdb
# 打开数据库连接
db=mdb.connect(host='localhost',port=3306,user='root',passwd='QQqq531508084',db='t2rdfaultdiag',charset='utf8' )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

TABLE_NAME='meterdata'
cursor.execute('SELECT * FROM %s WHERE Area="靖海电厂（#1主变高）"' %TABLE_NAME)
#print 'total records: %d' %count
#print 'total records:', cursor.rowcount

desc = cursor.description
for x in desc:
    print x[0],
print "\n"

results=cursor.fetchall()
for r in results:
    for s in r:
        print s,
    print "\n"

cursor.close()    
db.close()




























