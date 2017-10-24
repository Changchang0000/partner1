# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 14:30:19 2017

@author: 刘常
"""

#==============================================================================

#L=['PTerror_AM80,PTerror_AP80,PTerror_AM100,PTerror_AP100,PTerror_AM115,PTerror_AP115',
#               'PTerror_BM80,PTerror_BP80,PTerror_BM100,PTerror_BP100,PTerror_BM115,PTerror_BP115',
#               'PTerror_CM80,PTerror_CP80,PTerror_CM100,PTerror_CP100,PTerror_CM115,PTerror_CP115']
#def TerrorDiag(L):
#    print L[0]
#TerrorDiag(L)

import MySQLdb as mdb
import numpy as np
import EEMD_2rdfault as eft
# 打开数据库连接
db=mdb.connect(host='localhost',port=3306,user='root',passwd='QQqq531508084',db='t2rdfaultdiag',charset='utf8' )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
AreaName="靖海电厂（#1主变高）"

#对表meterdata执行标准信息查询操作
cursor.execute('SELECT * FROM meterdata where State="正常" and Area="%s"' %AreaName)
#获取表中的column信息
desc = cursor.description
for x in desc:
    print x[0],
print "\n"
#获取meterdata表查询操作中的正常状态数据，作为基本数据存储到mdt列表中
mdt=[0 for i in range(30)]
results=cursor.fetchall()
for r in results:
    for i in range(len(r)):
        mdt[i]=r[i]
        print mdt[i],
    print "\n"
    
#对表measurepoint执行标准信息查询操作
cursor.execute('SELECT * FROM measurepoint where State="正常" and Area="%s"' %AreaName)
#获取表中的column信息
desc = cursor.description
for x in desc:
    print x[0],
print "\n"
#获取measurepoint表查询操作中的正常状态数据，作为基本数据存储到mpt列表中
mpt=[0 for i in range(45)]
results=cursor.fetchall()
for r in results:
    for i in range(len(r)):
        mpt[i]=r[i]
        print mpt[i],
    print "\n"
    
#对表errordata执行标准信息查询操作
cursor.execute('SELECT * FROM errordata where State="正常" and Area="%s"' %AreaName)
#获取表中的column信息
desc = cursor.description
for x in desc:
    print x[0],
print "\n"
#获取errordata表查询操作中的正常状态数据，作为基本数据存储到edt列表中
edt=[0 for i in range(50)]
results=cursor.fetchall()
for r in results:
    for i in range(len(r)):
        edt[i]=r[i]
        print edt[i],
    print "\n"
    
    
#对表meterdata执行测试信息查询操作
cursor.execute('SELECT * FROM meterdata where State="" and Area="%s"' %AreaName)
#获取meterdata表查询操作中的未定状态数据，存储到mdt1列表中
mdt1=[0 for i in range(30)]
results=cursor.fetchall()
for r in results:
    for i in range(len(r)):
        mdt1[i]=r[i]
        print mdt1[i],
    print "\n"
    
#对表measurepoint执行测试信息查询操作
cursor.execute('SELECT * FROM measurepoint where State="" and Area="%s"' %AreaName)
#获取measurepoint表查询操作中的未定状态数据，存储到mpt1列表中
mpt1=[0 for i in range(50)]
results=cursor.fetchall()
for r in results:
    for i in range(len(r)):
        mpt1[i]=r[i]
        print mpt1[i],
    print "\n"
    
#对表errordata执行测试信息查询操作
cursor.execute('SELECT * FROM errordata where State="" and Area="%s"' %AreaName)
#获取errordata表查询操作中的未定状态数据，存储到edt1列表中
edt1=[0 for i in range(50)]
results=cursor.fetchall()
for r in results:
    for i in range(len(r)):
        edt1[i]=r[i]
        print edt1[i],
    print "\n"

cursor.close()    
db.close()


#以下为二次回路各故障诊断模块
eft.PT_2rdfault(np.mean([float(mdt[5]),float(mdt[6]),float(mdt[7])]),
                0.5,float(mdt1[5]),float(mdt1[6]),float(mdt1[7]),
                float(mpt1[5]),float(mpt1[6]),float(mpt1[7]),
                float(mpt1[8]),float(mpt1[9]),float(mpt1[10]),
                float(mpt1[11]),float(mpt1[12]),float(mpt1[13]),
                float(mpt1[14]),float(mpt1[15]),float(mpt1[16]),
                float(edt1[5]),float(edt1[6]),  float(edt1[7]),
                float(mdt1[26]),float(mdt1[27]),float(mdt1[28]),
                float(mdt1[20]),float(mdt1[21]),float(mdt1[22]))

eft.CT_2rdfault(np.mean([float(mdt[8]),float(mdt[9]),float(mdt[10])]),
                float(mdt1[8]),float(mdt1[9]),float(mdt1[10]),
                float(mpt1[17]),float(mpt1[18]),float(mpt1[19]),
                float(mpt1[20]),float(mpt1[21]),float(mpt1[22]),
                float(mpt1[23]),float(mpt1[24]),float(mpt1[25]),
                float(mpt1[26]),float(mpt1[27]),float(mpt1[28]),
                float(mpt1[29]),float(mpt1[30]),float(mpt1[31]),
                float(mpt1[32]),float(mpt1[33]),float(mpt1[34]),
                float(mpt1[35]),float(mpt1[36]),float(mpt1[37]),
                float(mpt1[38]),float(mpt1[39]),float(mpt1[40]),
                float(mdt1[23]),float(mdt1[24]),float(mdt1[25]))

eft.eleSteal_fault(np.mean([float(mdt[5]),float(mdt[6]),float(mdt[7])]),
                   np.mean([float(mdt[8]),float(mdt[9]),float(mdt[10])]),
                   float(mdt1[5]),float(mdt1[6]),float(mdt1[7]),float(mdt1[8]),
                   float(mdt1[9]),float(mdt1[10]),float(mdt1[14]),float(mdt1[17]),
                   float(mdt1[18]),float(mdt1[19]))

eft.line_fault(float(mdt[14]),float(mdt1[14]),float(mdt1[5]),float(mdt1[6]),
               float(mdt1[7]),float(mdt1[8]),float(mdt1[9]),float(mdt1[10]),
               float(mdt1[17]),float(mdt1[18]),float(mdt1[19]))

eft.whErrorDiag(float(mdt1[29]),float(mdt1[15]),float(mdt1[16]))

eft.PTerrorDiag(edt[44],edt1[8:26])#仅针对0.02级电压互感器，其他精度等级的base值可通过交互界面选择

eft.CTerrorDiag(edt[45],edt1[26:44])
































