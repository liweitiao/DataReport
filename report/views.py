from django.shortcuts import render
import json, types
import datetime, time
import os, math
import xlrd
# Create your views here.

from django.http import HttpResponse, HttpResponseBadRequest
from django.db import connections
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from DataReport import settings
import os.path

# ---------------------------蔬菜供应----------------------------------
def report15(request):
    return  render(request, 'report15.html')

def report16(request):
    return  render(request, 'report16.html')

def report17(request):
    return  render(request, 'report17.html')

def report18(request):
    return  render(request, 'report18.html')

def report19(request):
    return  render(request, 'report19.html')

def report20(request):
    return  render(request, 'report20.html')
# ------------------------------蔬菜供应-------------------------------

# -------------------蔬菜部供应统计0116开发-------------------
def baobiao19_supply(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    day = int(request.GET.get('day'))
    timeStr = '%d-%d-%d'%(year, month, day)
    startTime = timeStr + ' 00:00:00'
    endTime = timeStr + ' 23:59:59'
    # 查询每日来货总量
    sum = querySupplySum(startTime, endTime)
    # print(year, month, day, startTime, endTime)
    # 查询来货数据
    data02 = queryBaobiao19_supply_data(startTime, endTime)
    # print('data02',data02)
    sum20 = 0
    for item in data02:
        # 查询档位号
        shopId = queryBaobiao19_shopId(startTime, endTime, item[0])
        item.insert(0, shopId)
        sum20 += item[2]
        DoD = "%.1f%%"%((item[2] / sum) * 100)
        item.append(DoD)

    # 处理合计数据
    sumDoD = "%.1f%%"%((sum20 / sum) * 100)
    data02.append([sum20, sumDoD])
    # print('--------02', data02)
    # data = [
    #     ['B2435', 'lisi', 41, '4%'],
    #     ['B2435', 'lisi', 42, '4%'],
    #     ['B2435', 'lisi', 43, '4%'],
    #     ['B2435', 'lisi', 44, '4%'],
    #     ['B2435', 'lisi', 45, '4%'],
    #     ['B2435', 'lisi', 46, '4%'],
    #     [2435, '20%']
    # ]

    return JsonResponse(data02, safe=False)

def queryBaobiao19_shopId(startTime, endTime, name):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询海吉星蔬菜来货总量对比数据的sql语句
    sqlStr = ''' SELECT
                    *
                from
                (
                    SELECT
                    v.doorway
                    from V_REPPONDER_PRODUCT_V2 v
                    where v.GROSSTIME BETWEEN "TO_DATE"('%s', 'YYYY-MM-DD HH24:mi:ss') AND "TO_DATE"('%s', 'YYYY-MM-DD HH24:mi:ss')
                    and v.CUSTOMERNAME = '%s'
                    and v.doorway is NOT NULL
                )
                where ROWNUM = 1''' % (startTime, endTime, name)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    print('result----',result)
    res = result[0][0]

    return res


def queryBaobiao19_supply_data(startTime, endTime):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询海吉星蔬菜来货总量对比数据的sql语句
    sqlStr = '''SELECT
                    *
                from 
                (
                    SELECT
                    v.CUSTOMERNAME, "ROUND"("SUM"(v.netweight)/1000, 0)
                    from V_REPPONDER_PRODUCT_V2 v
                    where  v.GROSSTIME BETWEEN "TO_DATE"('%s', 'YYYY-MM-DD HH24:mi:ss') AND "TO_DATE"('%s', 'YYYY-MM-DD HH24:mi:ss')
                    and v.BI_GOODSSORTOID = 14
                    GROUP BY v.CUSTOMERNAME
                    ORDER BY "SUM"(v.netweight) desc
                )
                where ROWNUM <=20'''%(startTime, endTime)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray

def querySupplySum(startTime, endTime):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询海吉星蔬菜来货总量对比数据的sql语句
    sqlStr = ''' SELECT
                    "ROUND"("SUM"(v.netweight)/1000, 0)
                from V_REPPONDER_PRODUCT_V2 v
                where  v.GROSSTIME BETWEEN "TO_DATE"('%s', 'YYYY-MM-DD HH24:mi:ss') AND "TO_DATE"('%s', 'YYYY-MM-DD HH24:mi:ss')
                and v.BI_GOODSSORTOID = 14''' % (startTime, endTime)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    res = result[0][0]

    return res




def baobiao18_source(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    day = int(request.GET.get('day'))
    currentTime, lastTime = handleTime(year, month, day)
    currentTime += ' 23:59:59'
    lastTime += ' 00:00:00'
    print(currentTime, lastTime)
    data = query_baobiao18_data(lastTime, currentTime)
    return JsonResponse(data, safe=False)

def query_baobiao18_data(lastTime, currentTime):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询海吉星蔬菜来货总量对比数据的sql语句
    sqlStr = ''' SELECT
                    "SUBSTR"("TO_CHAR"(v.GROSSTIME, 'YYYY-MM-DD HH24:mi:ss'),0,10) 日期,
                    "ROUND"("SUM"(case when v.productname_xx not in ('大蒜','甘薯','胡萝卜','淮山','姜','莲藕','萝卜','土豆','竹笋','红薯','番薯','F-19红薯','马蹄','芋头','山药','生姜','白萝卜','荸荠','淮山药','冬笋','沙葛','沙姜','老姜','粉葛','黑薯','鲁薯','红萝卜','葱姜蒜','洋葱','济薯25红薯','毛芋头','笋子','紫薯') then v.netweight else 0 end)/1000, 0) 鲜菜类,
                    "ROUND"("SUM"(case when v.productname_xx in ('大蒜','甘薯','胡萝卜','淮山','姜','莲藕','萝卜','土豆','竹笋','红薯','番薯','F-19红薯','马蹄','芋头','山药','生姜','白萝卜','荸荠','淮山药','冬笋','沙葛','沙姜','老姜','粉葛','黑薯','鲁薯','红萝卜','葱姜蒜','洋葱','济薯25红薯','毛芋头','笋子','紫薯') then v.netweight else 0 end)/1000, 0) 硬口菜
                from V_REPPONDER_PRODUCT_V2 v
                where  v.GROSSTIME BETWEEN "TO_DATE"('%s', 'YYYY-MM-DD HH24:mi:ss') AND "TO_DATE"('%s', 'YYYY-MM-DD HH24:mi:ss')
                and v.BI_goodssortna like '%%蔬菜%%'
                GROUP BY "SUBSTR"("TO_CHAR"(v.GROSSTIME, 'YYYY-MM-DD HH24:mi:ss'),0,10)
                ORDER BY "SUBSTR"("TO_CHAR"(v.GROSSTIME, 'YYYY-MM-DD HH24:mi:ss'),0,10);''' % (lastTime, currentTime)
    print(sqlStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray



def average_price(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    day = int(request.GET.get('day'))
    # 拼接本日的时间
    currentDayQueryStr, nextDayQueryStr = queryTimeStr02(year, month, day)
    # 拼接昨天的时间
    lastDayQueryStr, nextOfLastDayQueryStr = queryTimeStr03(year, month, day)

    # 处理需要返回前端的时间字符串
    currentTime, lastTime = handleTime(year, month, day)
    # 拼接本月的表名
    if (month < 10):
        monthStr = '0' + str(month)
    else:
        monthStr = str(month)
    currentTableName = 'T_PRICE_COLLECTION_' + str(year) + monthStr
    # print('currentTabelName', currentTableName)

    # 拼接上月的表名
    if (month == 1):
        lastMonth = 12
        lastYear = year - 1
        monthStr = str(lastMonth)
    elif (month - 1 < 10):
        monthStr = '0' + str(month - 1)
        lastYear = year
    else:
        monthStr = str(month - 1)
        lastYear = year

    lastTableName = 'T_PRICE_COLLECTION_' + str(lastYear) + monthStr
    # 查询蔬菜单品均价的数据
    data = queryAverage_price_data(currentTableName, lastTableName)


    # 查询蔬菜今日的数据
    currentDay_data = queryTwoDay_price_data(currentTableName, lastTableName, currentDayQueryStr, nextDayQueryStr)
    # 查询蔬菜昨日的数据
    lastDay_data = queryTwoDay_price_data(currentTableName, lastTableName, lastDayQueryStr, nextOfLastDayQueryStr)
    # 处理今日和昨日的数据
    data02 = handleData17(currentDay_data, lastDay_data)

    # currentTime = currentDay_data[0][3]
    # lastTime = lastDay_data[0][3]
    return JsonResponse([data, data02, currentTime, lastTime], safe=False)

def handleData17(currentDay_data, lastDay_data):
    res = []
    for i in lastDay_data:
        for j in currentDay_data:
            if i[2] != None and j[2] != None and i[0] == j[0]:
                i.pop()
                i.append(j[2])
                DoD = "%.1f%%" % (((j[2] - i[2]) / i[2]) * 100)
                i.append(DoD)
                res.append(i)
                break
    currntSum = 0
    lastSum = 0
    if len(res) > 0:
        for item in res:
            currntSum += item[3]
            lastSum += item[2]
        currntAverage = "%.1f"%(currntSum / len(res))
        lastAverage = "%.1f"%(lastSum / len(res))
        average_DoD = "%.1f%%"%(((float(currntAverage) - float(lastAverage)) / float(lastAverage)) * 100)
        res.append([lastAverage, currntAverage, average_DoD])
    return res

def handleTime(year, month, day):
    today = '%d-%d-%d'%(year, month, day)
    current = datetime.datetime.strptime(today, '%Y-%m-%d')
    currentTime = datetime.datetime.strftime(current, '%Y-%m-%d')

    last = current - datetime.timedelta(days=1)
    lastTime = datetime.datetime.strftime(last, '%Y-%m-%d')
    return [currentTime, lastTime]



def queryTwoDay_price_data(currentTableName, lastTableName, start, end):
    cursor = connections['price'].cursor()
    sqlStr = '''SELECT
                  t.category_name, 
                  t.origin_name, 
                  t.avg_price,
                  "TO_CHAR"(t.CREATE_date, 'YYYY-MM-DD')
                from 
                (
                    SELECT * from %s
                        UNION
                    SELECT * from %s
                ) t
                where CREATE_DATE BETWEEN "TO_DATE"(%s) AND "TO_DATE"(%s)
                and t.CATEGORY_NAME in ('大白菜','白萝卜','油麦菜','上海青','奶白菜','娃娃菜','尖椒','菠菜','生菜','包菜','莴笋','西红柿','青瓜','红萝卜','圆椒','苦瓜','茄子','豇豆','菜心','芥兰','豆角','黄瓜','芥蓝','胡萝卜')
                ORDER BY t.category_name
                '''%(currentTableName, lastTableName, start, end)
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        item = list(item)
        resArray.append(item)

    return resArray

def queryAverage_price_data(currentTableName, lastTableName):
    cursor = connections['price'].cursor()
    sqlStr = '''SELECT
                 "SUBSTR"("TO_CHAR"(v.CREATE_DATE, 'YYYY-MM-DD HH24:mi:ss'),0,10),
                 "ROUND"("SUM"(v.AVG_PRICE)/"COUNT"(v.CATEGORY_NAME), 1)
                from 
                (
                    SELECT * from %s
                    UNION
                    SELECT * from %s
                ) v
                WHERE v.AVG_PRICE > 0
                and v.CATEGORY_NAME in ('大白菜','白萝卜','油麦菜','上海青','奶白菜','娃娃菜','尖椒','菠菜','生菜','包菜','莴笋','西红柿','圆椒','苦瓜','茄子','菜心','豆角','黄瓜','芥蓝','胡萝卜')
                GROUP BY "SUBSTR"("TO_CHAR"(v.CREATE_DATE, 'YYYY-MM-DD HH24:mi:ss'),0,10)
                ORDER BY "SUBSTR"("TO_CHAR"(v.CREATE_DATE, 'YYYY-MM-DD HH24:mi:ss'),0,10)'''%(currentTableName, lastTableName)
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        item = list(item)
        resArray.append(item)

    return resArray



def average_price02(request):
    data = [
        [3.4,3.5,4.4,3.2,4.1,4.4,4.6,3.8,3.0,3.5,4.2,4.4],
        ['12-01', '12-02','12-03','12-04','12-05','12-06','12-07','12-08','12-09','12-10','12-11','12-12']
    ]
    return JsonResponse(data, safe=False)


def contrast(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    day = int(request.GET.get('day'))
    print('year-month-day', year, month, day)
    # 拼接本年开始和结束的时间
    currentStartTimeStr, currentEndTimeStr = contrastTimeStr(year, month, day)
    # 查询本年的数据
    currentYearData = queryContrastData(currentStartTimeStr, currentEndTimeStr)
    # 拼接去年开始和结束的时间
    lastStartTimeStr, lastEndTimeStr = contrastTimeStr(year-1, month, day)
    # 查询去年的数据
    lastYearData = queryContrastData(lastStartTimeStr, lastEndTimeStr)

    return JsonResponse([lastYearData, currentYearData], safe=False)

def contrastTimeStr(year, month, day):
    endTimeStr = "'%s-%s-%s 23:59:59', 'YYYY-MM-DD HH24:mi:ss'" % (str(year), str(month), str(day))
    nowStr = '%s-%s-%s'%(str(year), str(month), str(day))
    y = datetime.datetime.strptime(nowStr, '%Y-%m-%d')
    startTime = y - datetime.timedelta(days=20)
    startTimeStr = "'%s', 'YYYY-MM-DD HH24:mi:ss' "%str(startTime)
    return [startTimeStr, endTimeStr]

def queryContrastData(startTimeStr, endTimeStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询海吉星蔬菜来货总量对比数据的sql语句
    sqlStr = '''select
                    "SUBSTR"("TO_CHAR"(v.GROSSTIME, 'YYYY-MM-DD HH24:mi:ss'),0,10),
                    "ROUND"("SUM"(v.NETWEIGHT)/1000, 0)
                from V_REPPONDER_PRODUCT_V2 v
                where v.GROSSTIME BETWEEN "TO_DATE"(%s) AND "TO_DATE"(%s)
                and v.BI_goodssortna like '%%蔬菜%%'
                GROUP BY "SUBSTR"("TO_CHAR"(v.GROSSTIME, 'YYYY-MM-DD HH24:mi:ss'),0,10)
                ORDER BY "SUBSTR"("TO_CHAR"(v.GROSSTIME, 'YYYY-MM-DD HH24:mi:ss'),0,10)'''%(startTimeStr, endTimeStr)
    print(sqlStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray

def source(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    day = int(request.GET.get('day'))
    # 拼接今天的时间
    currentDayQueryStr, nextDayQueryStr = queryTimeStr02(year, month, day)
    currentDaySourceData = querySourceData(currentDayQueryStr, nextDayQueryStr)
    # 拼接昨天的时间
    lastDayQueryStr, nextOfLastDayQueryStr = queryTimeStr03(year, month, day)
    lastDaySourceData = querySourceData(lastDayQueryStr, nextOfLastDayQueryStr)
    # 需要返回前端的时间字符串
    dayArr = [lastDayQueryStr[6:11]]
    return JsonResponse([currentDaySourceData, lastDaySourceData, dayArr], safe=False)


def querySourceData(currentQueryStr, nextQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询海吉星蔬菜来源地的sql语句
    sqlStr = '''select 
                    "SUBSTR"(v.PROVINCECITYNAME,0,2),
                    "ROUND"("SUM"(v.NETWEIGHT)/1000, 0)
                from V_REPPONDER_PRODUCT_V2 v
                where v.GROSSTIME BETWEEN "TO_DATE"(%s) AND "TO_DATE"(%s)
                GROUP BY "SUBSTR"(v.PROVINCECITYNAME,0,2)
                ORDER BY "SUM"(v.NETWEIGHT) desc'''%(currentQueryStr, nextQueryStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray











def conn(request):
    data = connect()
    return JsonResponse(data, safe=False)


def connect():
    cursor = connections['price'].cursor()
    sqlStr = '''SELECT
                 t.ORIGIN_NAME, t.CREATE_DATE, t.CATEGORY_ID, t.CATEGORY_NAME, t.AVG_PRICE
                from T_PRICE_COLLECTION_202012 t
                where 1=1
                and CREATE_DATE BETWEEN "TO_DATE"('2020-12-14 00:00:00', 'YYYY-MM-DD HH24:mi:ss') AND "TO_DATE"('2020-12-15 00:00:00', 'YYYY-MM-DD HH24:mi:ss')
                and t.CATEGORY_NAME in ('大白菜','白萝卜','油麦菜','上海青','奶白菜','娃娃菜','尖椒','菠菜','生菜','包菜','莴笋','西红柿','青瓜','红萝卜','圆椒','苦瓜','茄瓜','豇豆','菜心','芥兰')
                ;'''
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        item = list(item)
        resArray.append(item)

    print('DoD++++++++++', resArray)
    return resArray




# -------------------蔬菜部供应统计0116开发-------------------

def file_extension(path):
  return os.path.splitext(path)[1]

# ----------------jsonp----------------------
def jsonp(request):
    data = {'a':111}
    callback = request.GET.get('callback')
    res = "%s(%s)"%(callback, json.dumps(data))
    print(type(res), res)
    # return HttpResponse(res)
    return HttpResponse(res)

# ----------------jsonp----------------------

def exer(request):
    data = {'a':1, 'b':2}
    return  render(request, 'exer.html')

def tenant(request):
    return render(request, 'tenant.html')

def report11(request):
    return render(request, 'report11.html')

def baobiao11(request):
    data = []
    for i in range(111, 130):
        map = {"shop_id": i,
               "name": i,
               "idno": i,
               "id_address": i,
               "now_address": i,
               "phone": i,
               "native": i,
               "nation": i,
               "legal_person_name": i,
               "legal_person_id": i,
               "remarks": i
               }
        data.append(map)
    result = {"code": 0, "msg": "", "count": 30, "data": data}
    return JsonResponse(result, safe=False)


def report12(request):
    return render(request, 'report12.html')

def baobiao12(request):
    data = []
    for i in range(111, 130):
        # for j in range(0, len(currentDayData[i])):
        map = {"shop_id": i,
               "rename_time": i,
               "rename_type": i,
               "rename_before": i,
               "rename_after": i,
               "relationship": i,
               "remarks": i
               }
        data.append(map)
    result = {"code": 0, "msg": "", "count": 30, "data": data}
    return JsonResponse(result, safe=False)

# -----------------------承租人信息---------------------------------------

@csrf_exempt
def upload_tenant(request):
    # 根name取 file 的值
    file = request.FILES.get('file')
    # logger.log().info('uplaod:%s'% file)
    # 创建upload文件夹
    if not os.path.exists(settings.UPLOAD_ROOT):
        os.makedirs(settings.UPLOAD_ROOT)
    try:
        if file_extension(file.name) not in ('.xlsx', '.xls'):
            return HttpResponseBadRequest('error')
        # 循环二进制写入
        with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
            for i in file.readlines():
                f.write(i)
    except Exception as e:
        return HttpResponseBadRequest('error')
    # 插入数据失败时要返回失败
    try:
        wrdb_tenant(file.name)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('error')

    return JsonResponse('ok', safe=False)


# 将excel数据写入mysql
def wrdb_tenant(filename):
    # 打开上传 excel 表格
    readboot = xlrd.open_workbook(settings.UPLOAD_ROOT + "/" + filename)
    sheet = readboot.sheet_by_index(0)
    #获取excel的行和列
    nrows = sheet.nrows
    ncols = sheet.ncols
    for i in range(1, nrows):
        row = sheet.row_values(i)
        print(row)
        shop_id = row[0]
        name = row[1]
        idno = row[2]
        id_address = row[3]
        now_address = row[4]
        try:
            phone = math.floor(row[5])
        except:
            phone = row[5] or ''
        native = row[6]
        sql = '''insert into TENANT_INFORMATION ("tenant_id","shop_id","name","idno","id_address","now_address","phone","native") values '''
        values = "(TENANT_INFORMATION_seq.nextval, '%s','%s','%s','%s','%s','%s','%s')"%(shop_id, name, idno, id_address, now_address, phone, native)
        sql += values
        insertTenant_Information(sql)

def insertTenant_Information(sql):
    # 建立游标对象
    cursor = connection.cursor()
    cursor.execute(sql)


def gettenantList(request):
    pagenum = int(request.GET.get('pagenum'))
    pagesize = int(request.GET.get('pagesize'))
    query = request.GET.get('query').strip()
    # 查询数据
    tenantList = query_tenantList(query)

    total = len(tenantList)
    if total < pagesize * pagenum:
        end = total
    else:
        end = pagesize * pagenum

    start = (pagenum - 1) * pagesize
    result = []
    for i in range(start, end):
        map = {
            "tenant_id": tenantList[i][0],
            "shop_id": tenantList[i][1],
            "name": tenantList[i][2],
            "idno": tenantList[i][3],
            "id_address": tenantList[i][4],
            "now_address": tenantList[i][5],
            "phone": tenantList[i][6],
            "native": tenantList[i][7],
            "nation": tenantList[i][8],
            "legal_person_name": tenantList[i][9],
            "legal_person_id": tenantList[i][10],
            "remarks": tenantList[i][11]
        }
        result.append(map)
    data = {"code": 200, "msg": '', "total": total, "data": result}
    return JsonResponse(data, safe=False)


def query_tenantList(query):
    query = '%' + query + '%'
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询承租人信息的语句
    sqlStr = '''SELECT 
                    "tenant_id","shop_id", "name", "idno", "id_address", "now_address" , "phone", "native", "nation", "legal_person_name", "legal_person_id", "remarks"  
                from tenant_information where "shop_id" like '%s' or "name" like '%s' or "idno" like '%s';'''%(query, query, query)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 处理成符合格式的数据
        resArray.append(list(item))
    return resArray


def addTenant(request):
    if request.method == 'POST':
        data = (request.body).decode()
        # 解析出需要插入的数据
        data = json.loads(data)

        try:
            insertIntoTenant(data)
        except Exception as e:
            res = {"code": 400, "msg": "添加承租人失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "添加承租人成功! "}

        return JsonResponse(res, safe=False)


def insertIntoTenant(data):
    shop_id = data["shop_id"] or ''
    name = data["name"] or ''
    idno = data["idno"] or ''
    id_address = data["id_address"] or ''
    now_address = data["now_address"] or ''
    phone = data["phone"] or ''
    native = data["native"] or ''
    nation = data["nation"] or ''
    legal_person_name = data["legal_person_name"] or ''
    legal_person_id = data["legal_person_id"] or ''
    remarks = data["remarks"] or ''

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接insert的sql语句
    sqlStr = '''insert into tenant_information ("tenant_id","shop_id","name","idno","id_address","now_address",
                    "phone","native","nation","legal_person_name","legal_person_id","remarks" ) 
                values(tenant_information_seq.nextval, '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
                '''%(shop_id,name,idno,id_address,now_address,phone,native,nation,legal_person_name,legal_person_id,remarks)

    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def deleteTenant(request):
    if request.method == 'POST':
        tenant_id = (request.body).decode()

        try:
            deleteTenantById(tenant_id)
        except Exception as e:
            res = {"code": 400, "msg": "删除承租方失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "删除承租方成功! "}
        return JsonResponse(res, safe=False)


def deleteTenantById(tenant_id):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接insert的sql语句
    sqlStr = '''delete from tenant_information where "TO_CHAR"("tenant_id") = '%s' '''%(tenant_id)
    # print(sqlStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def getTenantById(request):
    tenantId = request.GET.get('tenantId')
    res = queryTenantById(tenantId)
    if (len(res) == 0):
        result = {"code": 400, "msg": '没有查询到承租人! ', "data": 0}
    else:
        map = {
            "tenant_id": res[0][0],
            "shop_id": res[0][1],
            "name": res[0][2],
            "idno": res[0][3],
            "id_address": res[0][4],
            "now_address": res[0][5],
            "phone": res[0][6],
            "native": res[0][7],
            "nation": res[0][8],
            "legal_person_name": res[0][9],
            "legal_person_id": res[0][10],
            "remarks": res[0][11]
        }
        result = {"code": 200, "msg": '查询到承租人信息! ', "data": map}
    return JsonResponse(result, safe=False)


def queryTenantById(tenantId):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询承租人信息的语句
    sqlStr = '''SELECT * from tenant_information where "TO_CHAR"("tenant_id") = '%s' '''%(tenantId)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 处理成符合格式的数据
        resArray.append(list(item))
    return resArray


def updateTenantInfo(request):
    if request.method == 'POST':
        data = (request.body).decode()
        # 解析出需要插入的数据
        data = json.loads(data)

        # time.sleep(3)
        try:
            updateTenant(data)
        except Exception as e:
            res = {"code": 400, "msg": "修改承租人失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "修改承租人成功! "}

        return JsonResponse(res, safe=False)


def updateTenant(data):
    tenant_id = data["tenant_id"] or ''
    shop_id = data["shop_id"] or ''
    name = data["name"] or ''
    idno = data["idno"] or ''
    id_address = data["id_address"] or ''
    now_address = data["now_address"] or ''
    phone = data["phone"] or ''
    native = data["native"] or ''
    nation = data["nation"] or ''
    legal_person_name = data["legal_person_name"] or ''
    legal_person_id = data["legal_person_id"] or ''
    remarks = data["remarks"] or ''

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接aupdate的sql语句
    sqlStr = '''UPDATE tenant_information  set "shop_id"='%s',"name"='%s',"idno"='%s',"id_address"='%s',
                "now_address"='%s',"phone"='%s',"native"='%s',"nation"='%s',"legal_person_name"='%s',
                "legal_person_id"='%s', "remarks"='%s'
                where "TO_CHAR"("tenant_id") = '%s'
                ''' % (shop_id, name, idno, id_address, now_address, phone, native, nation, legal_person_name, legal_person_id, remarks, tenant_id)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


# --------------------------------------------------------------


# -----------------------物业合同更名记录---------------------------------------

@csrf_exempt
def upload_contract(request):
    # 根name取 file 的值
    file = request.FILES.get('file')
    # 创建upload文件夹
    if not os.path.exists(settings.UPLOAD_ROOT):
        os.makedirs(settings.UPLOAD_ROOT)
    try:
        if file_extension(file.name) not in ('.xlsx', '.xls'):
            return HttpResponseBadRequest('error')
        # 循环二进制写入
        with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
            for i in file.readlines():
                f.write(i)
    except Exception as e:
        return HttpResponseBadRequest('error')
    # 插入数据失败时要返回失败
    try:
        wrdb_contract(file.name)
    except Exception as e:
        return HttpResponseBadRequest('error')

    return JsonResponse('ok', safe=False)


# 将excel数据写入mysql
def wrdb_contract(filename):
    # 打开上传 excel 表格
    readboot = xlrd.open_workbook(settings.UPLOAD_ROOT + "/" + filename)
    sheet = readboot.sheet_by_index(0)
    #获取excel的行和列
    nrows = sheet.nrows
    ncols = sheet.ncols
    for i in range(1, nrows):
        row = sheet.row_values(i)
        shop_id = row[0]
        rename_time = row[1]
        rename_type = row[2]
        rename_before = row[3]
        rename_after = row[4]
        relationship = row[5]
        remarks = row[6]
        sql = '''insert into CONTRACT_RECORD ("record_id","shop_id","rename_time","rename_type","rename_before","rename_after","relationship","remarks") values '''
        values = "(CONTRACT_RECORD_seq.nextval, '%s','%s','%s','%s','%s','%s','%s')"%(shop_id, rename_time, rename_type, rename_before, rename_after, relationship, remarks)
        sql += values
        insertContract_Record(sql)


def insertContract_Record(sql):
    # 建立游标对象
    cursor = connection.cursor()
    cursor.execute(sql)


def getcontractList(request):
    pagenum = int(request.GET.get('pagenum'))
    pagesize = int(request.GET.get('pagesize'))
    query = request.GET.get('query').strip()
    # 查询数据
    contractList = query_contractList(query)

    total = len(contractList)
    if total < pagesize * pagenum:
        end = total
    else:
        end = pagesize * pagenum

    start = (pagenum - 1) * pagesize
    # while total < start:
    #     pagenum -= 1
    #     start = (pagenum - 1) * pagesize
    # 处理成符合格式的数据
    result = []
    for i in range(start, end):
        map = {
            "record_id": contractList[i][0],
            "shop_id": contractList[i][1],
            "rename_time": contractList[i][2],
            "rename_type": contractList[i][3],
            "rename_before": contractList[i][4],
            "rename_after": contractList[i][5],
            "relationship": contractList[i][6],
            "remarks": contractList[i][7]
        }
        result.append(map)
    data = {"code": 200, "msg": '', "total": total, "data": result}
    return JsonResponse(data, safe=False)


def query_contractList(query):
    query = '%' + query + '%'
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询承租人信息的语句
    sqlStr = '''SELECT 
                    "record_id","shop_id", "rename_time", "rename_type", "rename_before", "rename_after" , "relationship", "remarks"  
                from contract_record where "shop_id" like '%s' or "rename_before" like '%s' or "rename_after" like '%s';'''%(query, query, query)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 处理成符合格式的数据
        resArray.append(list(item))
    return resArray


def deleteContract(request):
    if request.method == 'POST':
        record_id = (request.body).decode()

        try:
            deleteContractById(record_id)
        except Exception as e:
            res = {"code": 400, "msg": "删除经营信息失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "删除经营信息成功! "}
        return JsonResponse(res, safe=False)


def deleteContractById(record_id):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接insert的sql语句
    sqlStr = '''delete from contract_record where "TO_CHAR"("record_id") = '%s' '''%(record_id)
    # print(sqlStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def getContractById(request):
    record_id = request.GET.get('record_id')
    res = queryContractById(record_id)
    if (len(res) == 0):
        result = {"code": 400, "msg": '没有查询到经营信息! ', "data": 0}
    else:
        map = {
            "record_id": res[0][0],
            "shop_id": res[0][1],
            "rename_time": res[0][2],
            "rename_type": res[0][3],
            "rename_before": res[0][4],
            "rename_after": res[0][5],
            "relationship": res[0][6],
            "remarks": res[0][7]
        }
        result = {"code": 200, "msg": '查询到经营信息! ', "data": map}
    return JsonResponse(result, safe=False)


def queryContractById(record_id):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询承租人信息的语句
    sqlStr = '''SELECT * from contract_record where "TO_CHAR"("record_id") = '%s' '''%(record_id)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 处理成符合格式的数据
        resArray.append(list(item))
    return resArray


def updateContractInfo(request):
    if request.method == 'POST':
        data = (request.body).decode()
        # 解析出需要插入的数据
        data = json.loads(data)

        # time.sleep(3)
        try:
            updateContract(data)
        except Exception as e:
            res = {"code": 400, "msg": "修改经营信息失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "修改经营信息成功! "}

        return JsonResponse(res, safe=False)


def updateContract(data):
    record_id = data["record_id"] or ''
    shop_id = data["shop_id"] or ''
    rename_time = data["rename_time"] or ''
    rename_type = data["rename_type"] or ''
    rename_before = data["rename_before"] or ''
    rename_after = data["rename_after"] or ''
    relationship = data["relationship"] or ''
    remarks = data["remarks"] or ''

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接aupdate的sql语句
    sqlStr = '''UPDATE contract_record  set "shop_id"='%s',"rename_time"='%s',"rename_type"='%s',"rename_before"='%s',
                "rename_after"='%s',"relationship"='%s',"remarks"='%s'
                where "TO_CHAR"("record_id") = '%s'
                ''' % (shop_id, rename_time, rename_type, rename_before, rename_after, relationship, remarks, record_id)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def addContract(request):
    if request.method == 'POST':
        data = (request.body).decode()
        # 解析出需要插入的数据
        data = json.loads(data)

        # time.sleep(3)
        try:
            insertIntoContract_Record(data)
        except Exception as e:
            # print('error', e)
            res = {"code": 400, "msg": "添加经营信息失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "添加经营信息成功! "}

        return JsonResponse(res, safe=False)


def insertIntoContract_Record(data):
    shop_id = data["shop_id"] or ''
    rename_time = data["rename_time"] or ''
    rename_type = data["rename_type"] or ''
    rename_before = data["rename_before"] or ''
    rename_after = data["rename_after"] or ''
    relationship = data["relationship"] or ''
    remarks = data["remarks"] or ''

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接insert的sql语句
    sqlStr = '''insert into CONTRACT_RECORD ("record_id","shop_id","rename_time","rename_type","rename_before","rename_after","relationship","remarks") 
                values(contract_record_seq.nextval, '%s','%s','%s','%s','%s','%s','%s')
                '''%(shop_id,rename_time, rename_type, rename_before, rename_after, relationship, remarks)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount



# -------------------------------------------------------------

# -----------------------------经营信息--------------------------------

@csrf_exempt
def upload_management(request):
    # 根name取 file 的值
    file = request.FILES.get('file')
    # 创建upload文件夹
    if not os.path.exists(settings.UPLOAD_ROOT):
        os.makedirs(settings.UPLOAD_ROOT)
    try:
        if file_extension(file.name) not in ('.xlsx', '.xls'):
            return HttpResponseBadRequest('error')
        # 循环二进制写入
        with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
            for i in file.readlines():
                f.write(i)
    except Exception as e:
        return HttpResponseBadRequest('error')
    # 插入数据失败时要返回失败
    try:
        wrdb_management(file.name)
    except Exception as e:
        return HttpResponseBadRequest('error')

    return JsonResponse('ok', safe=False)


# 将excel数据写入mysql
def wrdb_management(filename):
    # 打开上传 excel 表格
    readboot = xlrd.open_workbook(settings.UPLOAD_ROOT + "/" + filename)
    sheet = readboot.sheet_by_index(0)
    #获取excel的行和列
    nrows = sheet.nrows
    ncols = sheet.ncols
    for i in range(1, nrows):
        row = sheet.row_values(i)
        shop_id = row[0]
        business_license_name = row[1]
        business_license_no = row[2]
        name = row[3]
        try:
            phone = math.floor(row[4])
        except:
            phone = row[4] or ''
        category = row[5]
        base = row[6]
        other_market = row[7]
        remarks = row[8]
        sql = '''insert into management ("management_id","shop_id","business_license_name","business_license_no","name","phone","category","base","other_market","remarks") values '''
        values = "(management_seq.nextval, '%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(shop_id, business_license_name, business_license_no, name, phone, category, base, other_market, remarks)
        sql += values
        insertMangement(sql)


def insertMangement(sql):
    # 建立游标对象
    cursor = connection.cursor()
    cursor.execute(sql)


def getmanagementList(request):
    pagenum = int(request.GET.get('pagenum'))
    pagesize = int(request.GET.get('pagesize'))
    query = request.GET.get('query').strip()
    # 查询数据
    managementList = query_managementList(query)

    total = len(managementList)
    if total < pagesize * pagenum:
        end = total
    else:
        end = pagesize * pagenum

    start = (pagenum - 1) * pagesize
    result = []
    for i in range(start, end):
        map = {
            "management_id": managementList[i][0],
            "shop_id": managementList[i][1],
            "business_license_name": managementList[i][2],
            "business_license_no": managementList[i][3],
            "name": managementList[i][4],
            "phone": managementList[i][5],
            "category": managementList[i][6],
            "base": managementList[i][7],
            "other_market": managementList[i][8],
            "remarks": managementList[i][9]
        }
        result.append(map)
    data = {"code": 200, "msg": '', "total": total, "data": result}
    return JsonResponse(data, safe=False)


def query_managementList(query):
    query = '%' + query + '%'
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询承租人信息的语句
    sqlStr = '''SELECT 
                    "management_id","shop_id", "business_license_name", "business_license_no", "name", "phone" , "category","base","other_market", "remarks"  
                from management where "shop_id" like '%s' or "name" like '%s';'''%(query, query)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 处理成符合格式的数据
        resArray.append(list(item))
    return resArray


def deleteManagement(request):
    if request.method == 'POST':
        management_id = (request.body).decode()
        try:
            deleteManagementById(management_id)
        except Exception as e:
            res = {"code": 400, "msg": "删除合同更名记录失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "删除合同更名记录成功! "}
        return JsonResponse(res, safe=False)


def deleteManagementById(management_id):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接insert的sql语句
    sqlStr = '''delete from management where "TO_CHAR"("management_id") = '%s' '''%(management_id)
    # print(sqlStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def getManagementById(request):
    management_id = request.GET.get('management_id')
    res = queryManagementById(management_id)
    if (len(res) == 0):
        result = {"code": 400, "msg": '没有查询到合同更名记录信息! ', "data": 0}
    else:
        map = {
            "management_id": res[0][0],
            "shop_id": res[0][1],
            "business_license_name": res[0][2],
            "business_license_no": res[0][3],
            "name": res[0][4],
            "phone": res[0][5],
            "category": res[0][6],
            "base": res[0][5],
            "other_market": res[0][6],
            "remarks": res[0][7]
        }
        result = {"code": 200, "msg": '查询到合同更名记录信息! ', "data": map}
    return JsonResponse(result, safe=False)


def queryManagementById(management_id):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询承租人信息的语句
    sqlStr = '''SELECT * from management where "TO_CHAR"("management_id") = '%s' '''%(management_id)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 处理成符合格式的数据
        resArray.append(list(item))
    return resArray


def updateManagementInfo(request):
    if request.method == 'POST':
        data = (request.body).decode()
        # 解析出需要插入的数据
        data = json.loads(data)
        try:
            updateManagement(data)
        except Exception as e:
            print('error', e)
            res = {"code": 400, "msg": "修改合同更名记录失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "修改合同更名记录成功! "}

        return JsonResponse(res, safe=False)


def updateManagement(data):
    management_id = data["management_id"] or ''
    shop_id = data["shop_id"] or ''
    business_license_name = data["business_license_name"] or ''
    business_license_no = data["business_license_no"] or ''
    name = data["name"] or ''
    phone = data["phone"] or ''
    category = data["category"] or ''
    base = data["base"] or ''
    other_market = data["other_market"] or ''
    remarks = data["remarks"] or ''

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接aupdate的sql语句
    sqlStr = '''UPDATE management set "shop_id"='%s',"business_license_name"='%s',"business_license_no"='%s',"name"='%s',
                "phone"='%s',"category"='%s',"base"='%s',"other_market"='%s',"remarks"='%s'
                where "TO_CHAR"("management_id") = '%s'
                ''' % (shop_id, business_license_name, business_license_no, name, phone, category, base,other_market,remarks,management_id)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def addManagement(request):
    if request.method == 'POST':
        data = (request.body).decode()
        # 解析出需要插入的数据
        data = json.loads(data)

        try:
            insertIntoManagement(data)
        except Exception as e:
            # print('error', e)
            res = {"code": 400, "msg": "添加合同更名记录失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "添加合同更名记录成功! "}

        return JsonResponse(res, safe=False)


def insertIntoManagement(data):
    shop_id = data["shop_id"] or ''
    business_license_name = data["business_license_name"] or ''
    business_license_no = data["business_license_no"] or ''
    name = data["name"] or ''
    phone = data["phone"] or ''
    category = data["category"] or ''
    base = data["base"] or ''
    other_market = data["other_market"] or ''
    remarks = data["remarks"] or ''

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接insert的sql语句
    sqlStr = '''insert into management ("management_id","shop_id","business_license_name","business_license_no","name","phone","category","base","other_market","remarks") 
                values(management_seq.nextval, '%s','%s','%s','%s','%s','%s','%s','%s','%s')
                '''%(shop_id, business_license_name, business_license_no, name, phone, category, base, other_market, remarks)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


# ----------------------------------经营信息---------------------------


# ----------------------------------社会关系---------------------------

@csrf_exempt
def upload_social(request):
    # 根name取 file 的值
    file = request.FILES.get('file')
    # 创建upload文件夹
    if not os.path.exists(settings.UPLOAD_ROOT):
        os.makedirs(settings.UPLOAD_ROOT)
    try:
        if file_extension(file.name) not in ('.xlsx', '.xls'):
            return HttpResponseBadRequest('error')
        # 循环二进制写入
        with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
            for i in file.readlines():
                f.write(i)
    except Exception as e:
        return HttpResponseBadRequest('error')
    # 插入数据失败时要返回失败
    try:
        wrdb_social(file.name)
    except Exception as e:
        return HttpResponseBadRequest('error')

    return JsonResponse('ok', safe=False)


# 将excel数据写入mysql
def wrdb_social(filename):
    # 打开上传 excel 表格
    readboot = xlrd.open_workbook(settings.UPLOAD_ROOT + "/" + filename)
    sheet = readboot.sheet_by_index(0)
    #获取excel的行和列
    nrows = sheet.nrows
    ncols = sheet.ncols

    for i in range(1, nrows):
        row = sheet.row_values(i)
        print(row)
        shop_id = row[0] or ''
        name = row[1] or ''
        native = row[2] or ''
        relationship = row[3] or ''
        idno = row[4] or ''
        id_address = row[5] or ''
        now_address= row[6] or ''
        try:
            phone = math.floor(row[7])
        except:
            phone = row[7] or ''
        related_shop = row[8] or ''

        sql = '''insert into social ("social_id", "shop_id","name","native","relationship","idno","id_address","now_address","phone","related_shop") values '''
        values = "(social_seq.nextval, '%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(shop_id,name,native,relationship,idno,id_address,now_address,phone,related_shop)
        sql += values
        insertSocial(sql)


def insertSocial(sql):
    # 建立游标对象
    cursor = connection.cursor()
    cursor.execute(sql)


def getsocialList(request):
    pagenum = int(request.GET.get('pagenum'))
    pagesize = int(request.GET.get('pagesize'))
    query = request.GET.get('query').strip()
    print(query)
    # 查询数据
    socialList = query_socialList(query)

    total = len(socialList)
    if total < pagesize * pagenum:
        end = total
    else:
        end = pagesize * pagenum
    start = (pagenum - 1) * pagesize
    result = []
    for i in range(start, end):
        map = {
            "social_id": socialList[i][0],
            "shop_id": socialList[i][1],
            "name": socialList[i][2],
            "native": socialList[i][3],
            "relationship": socialList[i][4],
            "idno": socialList[i][5],
            "id_address": socialList[i][6],
            "now_address": socialList[i][7],
            "phone": socialList[i][8],
            "related_shop": socialList[i][9]
        }
        result.append(map)
    data = {"code": 200, "msg": '', "total": total, "data": result}
    return JsonResponse(data, safe=False)


def query_socialList(query):
    query = '%' + query + '%'
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询承租人信息的语句
    sqlStr = '''SELECT 
                    "social_id", "shop_id", "name","native","relationship","idno","id_address","now_address","phone","related_shop"  
                from social where "shop_id" like '%s' or "name" like '%s' or "idno" like '%s';'''%(query, query, query)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 处理成符合格式的数据
        resArray.append(list(item))
    return resArray


def deleteSocial(request):
    if request.method == 'POST':
        social_id = (request.body).decode()
        try:
            deleteSocialById(social_id)
        except Exception as e:
            res = {"code": 400, "msg": "删除社会关系失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "删除社会关系成功! "}
        return JsonResponse(res, safe=False)


def deleteSocialById(social_id):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接insert的sql语句
    sqlStr = '''delete from social where "TO_CHAR"("social_id") = '%s' '''%(social_id)
    # print(sqlStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def getSocialById(request):
    social_id = request.GET.get('social_id')
    res = querySocialById(social_id)
    if (len(res) == 0):
        result = {"code": 400, "msg": '没有查询到社会关系信息! ', "data": 0}
    else:
        map = {
            "social_id": res[0][0],
            "shop_id": res[0][1],
            "name": res[0][2],
            "native": res[0][3],
            "relationship": res[0][4],
            "idno": res[0][5],
            "id_address": res[0][6],
            "now_address": res[0][7],
            "phone": res[0][8],
            "related_shop": res[0][9]
        }
        result = {"code": 200, "msg": '查询到社会关系信息! ', "data": map}
    return JsonResponse(result, safe=False)


def querySocialById(social_id):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询承租人信息的语句
    sqlStr = '''SELECT * from social where "TO_CHAR"("social_id") = '%s' '''%(social_id)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 处理成符合格式的数据
        resArray.append(list(item))
    return resArray


def updateSocialInfo(request):
    if request.method == 'POST':
        data = (request.body).decode()
        # 解析出需要插入的数据
        data = json.loads(data)

        # time.sleep(3)
        try:
            updateSocial(data)
        except Exception as e:
            res = {"code": 400, "msg": "修改社会关系失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "修改社会关系成功! "}

        return JsonResponse(res, safe=False)


def updateSocial(data):
    social_id = data["social_id"] or ''
    shop_id = data["shop_id"] or ''
    name = data["name"] or ''
    native = data["native"] or ''
    relationship = data["relationship"] or ''
    idno = data["idno"] or ''
    id_address = data["id_address"] or ''
    now_address = data["now_address"] or ''
    phone = data["phone"] or ''
    related_shop = data["related_shop"] or ''

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接aupdate的sql语句
    sqlStr = '''UPDATE social set 
                    "shop_id" ='%s',
                    "name" ='%s',
                    "native" ='%s',
                    "relationship" ='%s',
                    "idno" ='%s',
                    "id_address" ='%s',
                    "now_address" ='%s',
                    "phone" ='%s',
                    "related_shop" ='%s'
                where "TO_CHAR"("social_id") = '%s'
                ''' % (shop_id,name,native,relationship,idno,id_address,now_address,phone,related_shop,social_id)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def addSocial(request):
    if request.method == 'POST':
        data = (request.body).decode()
        # 解析出需要插入的数据
        data = json.loads(data)
        try:
            insertIntoSocial(data)
        except Exception as e:
            # print('error', e)
            res = {"code": 400, "msg": "添加社会关系失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "添加社会关系成功! "}

        return JsonResponse(res, safe=False)


def insertIntoSocial(data):
    shop_id = data["shop_id"] or ''
    name = data["name"] or ''
    native = data["native"] or ''
    relationship = data["relationship"] or ''
    idno = data["idno"] or ''
    id_address = data["id_address"] or ''
    now_address = data["now_address"] or ''
    phone = data["phone"] or ''
    related_shop = data["related_shop"] or ''

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接insert的sql语句
    sqlStr = '''insert into social ("social_id", "shop_id","name","native","relationship","idno","id_address","now_address","phone","related_shop") 
                values(social_seq.nextval, '%s','%s','%s','%s','%s','%s','%s','%s','%s')
                '''%(shop_id, name,native,relationship,idno,id_address,now_address,phone,related_shop)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount

# ----------------------------------社会关系---------------------------

# ----------------------------------会员荣誉---------------------------
@csrf_exempt
def upload_member_honor(request):
    # 根name取 file 的值
    file = request.FILES.get('file')
    # 创建upload文件夹
    if not os.path.exists(settings.UPLOAD_ROOT):
        os.makedirs(settings.UPLOAD_ROOT)
    try:
        if file_extension(file.name) not in ('.xlsx', '.xls'):
            return HttpResponseBadRequest('error')
        # 循环二进制写入
        with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
            for i in file.readlines():
                f.write(i)
    except Exception as e:
        return HttpResponseBadRequest('error')
    # 插入数据失败时要返回失败
    try:
        wrdb_member_honor(file.name)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('error')

    return JsonResponse('ok', safe=False)


# 将excel数据写入mysql
def wrdb_member_honor(filename):
    # 打开上传 excel 表格
    readboot = xlrd.open_workbook(settings.UPLOAD_ROOT + "/" + filename)
    sheet = readboot.sheet_by_index(0)
    #获取excel的行和列
    nrows = sheet.nrows
    ncols = sheet.ncols

    for i in range(1, nrows):
        row = sheet.row_values(i)
        name = row[0] or ''
        idno = row[1] or ''
        try:
            year = math.floor(row[2])
        except:
            year = row[2] or ''
        honor = row[3] or ''

        sql = '''insert into Member_Honor ("honor_id","name","idno","year","honor") values '''
        values = "(Member_Honor_seq.nextval, '%s','%s','%s','%s')"%(name,idno,year,honor)
        sql += values
        insertMember_Honor(sql)


def insertMember_Honor(sql):
    # 建立游标对象
    cursor = connection.cursor()
    cursor.execute(sql)


def gethonorList(request):
    pagenum = int(request.GET.get('pagenum'))
    pagesize = int(request.GET.get('pagesize'))
    query = request.GET.get('query').strip()
    # 查询数据
    honorList = query_honorList(query)


    total = len(honorList)
    if total < pagesize * pagenum:
        end = total
    else:
        end = pagesize * pagenum

    start = (pagenum - 1) * pagesize
    result = []
    for i in range(start, end):
        map = {
            "honor_id": honorList[i][0],
            "name": honorList[i][1],
            "idno": honorList[i][2],
            "year": honorList[i][3],
            "honor": honorList[i][4]
        }
        result.append(map)
    data = {"code": 200, "msg": '', "total": total, "data": result}
    return JsonResponse(data, safe=False)


def query_honorList(query):
    query = '%' + query + '%'
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询承租人信息的语句
    sqlStr = '''SELECT 
                     "honor_id","name","idno","year","honor"
                from member_honor where "name" like '%s' or "idno" like '%s' ;'''%(query, query)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 处理成符合格式的数据
        resArray.append(list(item))
    return resArray


def deleteHonor(request):
    if request.method == 'POST':
        honor_id = (request.body).decode()

        try:
            deleteHonorById(honor_id)
        except Exception as e:
            # print(e)
            res = {"code": 400, "msg": "删除会员荣誉失败! "}
            return JsonResponse(res, safe=False)

        res = {"code": 200, "msg": "删除会员荣誉成功! "}
        return JsonResponse(res, safe=False)


def deleteHonorById(honor_id):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接insert的sql语句
    sqlStr = '''delete from member_honor where "TO_CHAR"("honor_id") = '%s' '''%(honor_id)
    # print(sqlStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def getHonorById(request):
    honor_id = request.GET.get('honor_id')
    res = queryHonorById(honor_id)
    if (len(res) == 0):
        result = {"code": 400, "msg": '没有查询到会员荣誉信息! ', "data": 0}
    else:
        map = {
            "honor_id": res[0][0],
            "name": res[0][1],
            "idno": res[0][2],
            "year": res[0][3],
            "honor": res[0][4]
        }
        result = {"code": 200, "msg": '查询到会员荣誉信息! ', "data": map}
    return JsonResponse(result, safe=False)


def queryHonorById(honor_id):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询承租人信息的语句
    sqlStr = '''SELECT * from member_honor where "TO_CHAR"("honor_id") = '%s' '''%(honor_id)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 处理成符合格式的数据
        resArray.append(list(item))
    return resArray


def updateHonorInfo(request):
    if request.method == 'POST':
        data = (request.body).decode()
        # 解析出需要插入的数据
        data = json.loads(data)
        try:
            updateHonor(data)
        except Exception as e:
            res = {"code": 400, "msg": "修改会员荣誉失败! "}
            return JsonResponse(res, safe=False)
        res = {"code": 200, "msg": "修改会员荣誉成功! "}

        return JsonResponse(res, safe=False)


def updateHonor(data):
    honor_id = data["honor_id"] or ''
    name = data["name"] or ''
    idno = data["idno"] or ''
    year = data["year"] or ''
    honor = data["honor"] or ''

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接aupdate的sql语句
    sqlStr = '''UPDATE member_honor set 
                    "name" ='%s',
                    "idno" ='%s',
                    "year" ='%s',
                    "honor" ='%s'
                where "TO_CHAR"("honor_id") = '%s'
                ''' % (name, idno, year, honor, honor_id)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def addHonor(request):
    if request.method == 'POST':
        data = (request.body).decode()
        # 解析出需要插入的数据
        data = json.loads(data)
        try:
            insertIntoMember_Honor(data)
        except Exception as e:
            res = {"code": 400, "msg": "添加会员荣誉失败! "}
            return JsonResponse(res, safe=False)
        res = {"code": 200, "msg": "添加会员荣誉成功! "}

        return JsonResponse(res, safe=False)


def insertIntoMember_Honor(data):
    name = data["name"] or ''
    idno = data["idno"] or ''
    year = data["year"] or ''
    honor = data["honor"] or ''


    # 建立游标对象
    cursor = connection.cursor()
    # 拼接insert的sql语句
    sqlStr = '''insert into Member_Honor("honor_id", "name", "idno", "year", "honor") 
                values(member_honor_seq.nextval, '%s','%s','%s','%s')
                '''%(name, idno, year, honor)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


# ----------------------------------会员荣誉---------------------------


# ---------------------------商户信息报表数据------------------------

def report_tenant_info(request):
    return render(request, 'report_tenant_info.html')


def tenant_contract(request):
    name = request.GET.get('name')
    idNo = request.GET.get('idNo')
    data = query_tenant_contract(name, idNo)
    return JsonResponse(data, safe=False)


def query_tenant_contract(name, idNo):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询物业合同信息的语句
    sqlStr = '''SELECT 
                SEATNO, SUMAREA, SUMAREA1, "SUBSTR"(BEGINDATE,0,10), "SUBSTR"(ENDDATE,0,10) , ALLYEARS
                from V_STORECONTRACT
                where (CUSTOMERNAME = '%s' or idno='%s') and STATENUM = 1;'''%(name, idNo)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def employee_information(request):
    name = request.GET.get('name')
    idNo = request.GET.get('idNo')
    data = query_employee_information(name, idNo)
    return JsonResponse(data, safe=False)


def query_employee_information(name, idNo):
    # 建立游标对象
    cursor = connection.cursor()
    sqlStr = '''select 
                    a.EMPLOYEE, a.IDNO, a.SHOPID, a.POSITION, a.IDADDRESS, a.HOMEADDR, a.LINK_1,
                    a.NATIONALITYS,
                    case when a.sex = 'M' then '男' else '女' end as sex,
                    a.native
                from employeereco@hgeb a
                left join employeereco_chidren@hgeb f on a.employeerecooid=f.employeerecooid
                WHERE f.ISLEAVE = 0
                and a.SHOPID in
                (
                    SELECT SEATNO
                    from V_STORECONTRACT
                    where (CUSTOMERNAME = '%s' or idno='%s') and STATENUM = 1
                );'''%(name, idNo)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def penal(request):
    name = request.GET.get('name')
    idNo = request.GET.get('idNo')
    data = query_penal(name, idNo)
    # data = {'a':1}
    return JsonResponse(data, safe=False)


def query_penal(name, idNo):
    # 建立游标对象
    cursor = connection.cursor()
    sqlStr = '''SELECT 
                 a.SHOPID, a.shopername
                ,"CONCAT"(b.name, "CONCAT"('--', b.KEYTIPS)) as c
                    ,case when (a.FEE > 0 and a.score > 0) then "CONCAT"("CONCAT"('罚钱: ' , a.FEE), "CONCAT"('  扣分: ' , a.SCORE))
                    when (a.FEE > 0 and a.score = 0) then "CONCAT"('罚钱: ' , a.FEE)
                    ELSE '警告 ' end as d
                ,"SUBSTR"(a.PAYDATE,0,10)
                from 
                PENALIZE a 
                LEFT JOIN PENALIZECLAUSE b on a.CLAUSEID = b.PENALIZECLAUSEOID
                where
                a.status != 2 and a.FEETYPE=0
                and SHOPID in 
                (
                    SELECT SEATNO
                    from V_STORECONTRACT
                    where (CUSTOMERNAME = '%s' or idno='%s') and STATENUM = 1
                )'''%(name, idNo)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def goods(request):
    name = request.GET.get('name')
    idNo = request.GET.get('idNo')
    # 查询档位
    shops = query_shop(name, idNo)
    data = []
    # 用档位分别查询数据
    for item in shops:
        # 用档位查询的数据
        result = query_shop_goods(item[0])
        if (result[1] != 0):
            data.append(result)
    return JsonResponse(data, safe=False)


def query_shop(name, idNo):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询物业合同信息的语句
    sqlStr = '''SELECT DISTINCT(SEATNO)
                from V_STORECONTRACT
                where (CUSTOMERNAME = '%s' or idno='%s') and STATENUM = 1
                ;'''%(name, idNo)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def query_shop_goods(shop):
    # 查询主要来货产地
    data_origin = query_shop_goods_byOrigin(shop)
    data_category = query_shop_goods_byCategory(shop)
    # 来货总量
    sum = 0
    origin = ''
    category = ''
    for i in range(0, len(data_origin)):
        sum += data_origin[i][1]
        origin += data_origin[i][0] + ':' + str(data_origin[i][1]) + ', '
    for i in range(0, len(data_category)):
        category += data_category[i][0] + ':' + str(data_category[i][1]) + ', '
    return [shop,sum, origin[0:-2], category[0:-2]]


def query_shop_goods_byOrigin(shop):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询物业合同信息的语句
    sqlStr = '''SELECT 
                 b.PROVINCECITYNAME
                ,ROUND("SUM"(a.SUMNETWEIGHT/1000),0)
                from
                PONDERATION  a
                INNER JOIN PONDERATIONITEM  b on a.PONDERATIONOID = b.PONDERATIONOID
                where a.grosstime BETWEEN "TO_DATE"('2019-01-01 00:00:00', 'YYYY-MM-DD HH24:mi:ss') and "TO_DATE"('2020-01-01 
                00:00:00', 'YYYY-MM-DD HH24:mi:ss')
                and a.DOORWAY = '%s'
                group by b.PROVINCECITYNAME
                order by "SUM"(a.SUMNETWEIGHT/1000) desc;''' % (shop)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def query_shop_goods_byCategory(shop):
    # 建立游标对象
    cursor = connection.cursor()
    sqlStr = ''' SELECT 
                 b.PRODUCTNAME
                 ,ROUND("SUM"(a.SUMNETWEIGHT/1000),0)
                 from
                 PONDERATION  a
                 INNER JOIN PONDERATIONITEM  b on a.PONDERATIONOID = b.PONDERATIONOID
                 where a.grosstime BETWEEN "TO_DATE"('2019-01-01 00:00:00', 'YYYY-MM-DD HH24:mi:ss') and "TO_DATE"('2020-01-01 
                00:00:00', 'YYYY-MM-DD HH24:mi:ss')
                 and a.DOORWAY = '%s'
                 group by b.PRODUCTNAME
                 order by "SUM"(a.SUMNETWEIGHT/1000) desc
                 ;''' % (shop)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def parking_card(request):
    name = request.GET.get('name')
    idNo = request.GET.get('idNo')
    data = query_parkingCard(name, idNo)
    return JsonResponse(data, safe=False)


def query_parkingCard(name, idNo):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询物业合同信息的语句
    sqlStr = '''select shopid, iccardtypename, employee
                    from v_tcmonthiccard_pno
                    where status = 1 and vehicletypeid != '012'
                    and shopid in 
                    (
                        SELECT SEATNO
                        from V_STORECONTRACT
                        where (CUSTOMERNAME = '%s' or idno='%s') and STATENUM = 1
                    )
                    ORDER BY shopid desc;''' % (name, idNo)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def tenant_information(request):
    name = request.GET.get('name')
    idno = request.GET.get('idNo')
    data = query_tenant_information(name, idno)
    return JsonResponse(data, safe=False)


def query_tenant_information(name, idno):
    query_name = '%' + name + '%'
    query_idno = '%' + idno + '%'
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询物业合同信息的语句
    sqlStr = '''SELECT 
                "name", "idno", "legal_person_name","legal_person_id", "id_address", "now_address", "phone" , "native", "nation"
                from TENANT_INFORMATION
                where "name" like '%s' or "idno" like '%s'
              '''%(query_name, query_idno)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = list(result[0])
    # 将结果转换为数组

    return resArray


def contract_record(request):
    name = request.GET.get('name')
    idNo = request.GET.get('idNo')
    # 查询档位
    shops = query_shop(name, idNo)
    data = []
    # 用档位分别查询合同更名记录数据
    for item in shops:
        # 用档位查询的数据
        result = query_contract_record(item[0])
        # print('result---->', result)
        # print(item[0])
        for reco in result:
            if len(reco) != 0 and reco[0] == item[0]:
                data.append(reco)
    return JsonResponse(data, safe=False)


def query_contract_record(shop):
    shop = '%' + shop + '%'
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询合同更名记录的语句
    sqlStr = '''SELECT 
                    "shop_id", "rename_time", "rename_type", "rename_before", "rename_after", "relationship", "remarks" 
                from CONTRACT_RECORD where  "shop_id" like '%s'
             ''' % (shop)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def management_info(request):
    name = request.GET.get('name')
    idNo = request.GET.get('idNo')
    # 查询档位
    shops = query_shop(name, idNo)
    print('shops---->', shops)
    data = []
    # 用档位分别查询经营信息
    for item in shops:
        # 用档位查询的数据
        result = query_management_info(item[0])
        # print('result---->', result)
        # print(item[0])
        for reco in result:
            if len(reco) != 0 and reco[2] == item[0]:
                data.append(reco)
    return JsonResponse(data, safe=False)


def query_management_info(shop):
    shop = '%' + shop + '%'
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询经营信息的语句
    sqlStr = '''SELECT 
                    "name","business_license_no","shop_id", "category", "business_license_name",   
                    "base","phone","other_market", "remarks" 
                from management where  "shop_id" like '%s'
                 ''' % (shop)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def honor_info(request):
    name = request.GET.get('name')
    idno = request.GET.get('idNo')
    data = query_honor_info(name, idno)
    return JsonResponse(data, safe=False)


def query_honor_info(name, idno):
    query_name = '%' + name + '%'
    query_idno = '%' + idno + '%'
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询会员荣誉的语句
    sqlStr = '''SELECT 
                    "name", "idno", "year","honor"
                    from MEMBER_HONOR
                    where "name" like '%s' or "idno" like '%s'
              ''' % (query_name, query_idno)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def social_info(request):
    name = request.GET.get('name')
    idNo = request.GET.get('idNo')
    # 查询档位
    shops = query_shop(name, idNo)
    data = []
    # 用档位分别查询社会关系数据
    for item in shops:
        # 用档位查询的数据
        result = query_social_info(item[0])
        for social in result:
            if len(social) != 0 and social[8] == item[0]:
                data.append(social)
    return JsonResponse(data, safe=False)


def query_social_info(shop):
    shop = '%' + shop + '%'
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询社会关系的语句
    sqlStr = '''SELECT 
                        "name","idno",  "relationship","native", 
                        "id_address", "now_address", "phone", "related_shop", "shop_id"
                   from social where  "shop_id" like '%s'
                ''' % (shop)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


# -----------------------商户信息报表数据----------------------------


def report01(request):
    print(request)
    return render(request, 'report01.html')


def report02(request):
    return render(request, 'report02.html')


def report03(request):
    return render(request, 'report03.html')


def report04(request):
    return render(request, 'report04.html')


def report05(request):
    return render(request, 'report05.html')


def report06(request):
    return render(request, 'report06.html')


def report07(request):
    return render(request, 'report07.html')


def report08(request):
    return render(request, 'report08.html')


def index(request):
    return render(request, 'index.html')


def baobiao01(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    # 拼接本月的时间
    currentMonthQueryStr, nextMonthQueryStr = queryTimeStr(year, month)
    # 查询本月数据---B1、B2、B3、B4、B5、B6、(D1、D2)冻品
    currentMonthData01 = queryData01(currentMonthQueryStr, nextMonthQueryStr)
    print("--------------------------------------------")
    print("B1-B6", currentMonthData01)
    # 查询本月数据---B0固定档数据
    currentMonthData02 = queryData02(currentMonthQueryStr, nextMonthQueryStr)
    print("--------------------------------------------")
    print("B0固定档数据", currentMonthData02)
    # 查询本月数据---玉米固定档数据
    currentMonthData03 = queryData03(currentMonthQueryStr, nextMonthQueryStr)
    print("--------------------------------------------")
    print("玉米固定档数据", currentMonthData03)
    # 查询本月数据---玉米、基地菜、瓜豆、菇类、固定基地菜、水菜数据
    currentMonthData04 = queryData04(currentMonthQueryStr, nextMonthQueryStr)
    print("--------------------------------------------")
    print("玉米、基地菜、瓜豆、菇类、固定基地菜、水菜数据", currentMonthData04)
    # 查询本月数据---地摊固定档数据
    currentMonthData05 = queryData05(currentMonthQueryStr, nextMonthQueryStr)
    print("--------------------------------------------")
    print("地摊固定档数据", currentMonthData05)

    # 按照报表格式处理本月的各个数据
    currentMonthResult = handleAllData(currentMonthData01, currentMonthData02, currentMonthData03, currentMonthData04, currentMonthData05)

    # 如果本月为1月，则上个月为上一年的12月， 否则为本月减1
    if (month == 1):
        lastMonth = 12
        lastYear = year -1
    else:
        lastMonth = month -1
        lastYear = year

    # 拼接上月的时间
    lastMonthQueryStr, nextOfLastMonthQueryStr = queryTimeStr(lastYear, lastMonth)
    # 查询上月数据---B1、B2、B3、B4、B5、B6、(D1、D2)冻品
    lastMonthData01 = queryData01(lastMonthQueryStr, nextOfLastMonthQueryStr)
    # 查询上月数据---B0固定档数据
    lastMonthData02 = queryData02(lastMonthQueryStr, nextOfLastMonthQueryStr)
    # 查询上月数据---玉米固定档数据
    lastMonthData03 = queryData03(lastMonthQueryStr, nextOfLastMonthQueryStr)
    # 查询上月数据---玉米、基地菜、瓜豆、菇类、固定基地菜、水菜数据
    lastMonthData04 = queryData04(lastMonthQueryStr, nextOfLastMonthQueryStr)
    # 查询上月数据---地摊固定档数据
    lastMonthData05 = queryData05(lastMonthQueryStr, nextOfLastMonthQueryStr)

    # 按照报表格式处理上月的各个数据
    lastMonthResult = handleAllData(lastMonthData01, lastMonthData02, lastMonthData03, lastMonthData04, lastMonthData05)

    # 处理来货量和车辆数合计的环比数据,得出环比率
    for i in range(0, len(currentMonthResult)):
        # 格式化来货量环比率如40.17%
        MoM01 = "%.2f%%"%((currentMonthResult[i][0]/lastMonthResult[i][0] - 1)*100)
        # 格式化车辆数合计环比率如40.17%
        MoM02 = "%.2f%%"%((currentMonthResult[i][-1]/lastMonthResult[i][-1] - 1)*100)
        # 插入到数组的第二列
        currentMonthResult[i].insert(1, MoM01)
        # 插入到数组的最后一列
        currentMonthResult[i].append(MoM02)
    return JsonResponse(currentMonthResult, safe=False)


def queryTimeStr(year, month):
    if (month == 12):
        nextMonth = 1
        nextYear = year + 1
    else:
        nextMonth = month + 1
        nextYear = year
    # currentMonthStr = "'" + str(year) + "-" + str(month) + "-01 " + "00:00:00', 'YYYY-MM-DD HH24:mi:ss'"
    currentMonthQueryStr = "'%s-%s-01 00:00:00', 'YYYY-MM-DD HH24:mi:ss'"%(str(year), str(month))
    nextMonthQueryStr = "'%s-%s-01 00:00:00', 'YYYY-MM-DD HH24:mi:ss'"%(str(nextYear), str(nextMonth))

    return [currentMonthQueryStr, nextMonthQueryStr]


def handleAllData(data1, data2, data3, data4, data5):
    """
    :param data1: B1、B2、B3、B4、B5、B6、(D1、D2)冻品的数据
    :param data2: B0固定档数据
    :param data3: 玉米固定档数据
    :param data4: 第一种情况：固定基地菜、水菜、菇类、瓜豆、玉米、基地菜 或者是第二种情况： 固定基地菜、水菜、菇类、瓜豆、玉米、或者是第三种情况： 固定基地菜、水菜数据（菜农菜）、瓜豆、玉米
    :param data5: 地摊固定档数据
    :return: data1为最终结果集
    """
    # 取出data1中的D1/D2的数据
    D2Data = data1.pop()
    D1Data = data1.pop()
    D1D2Data = []
    for i in range(0, len(D2Data)):
        D1D2Data.append(D2Data[i] + D1Data[i])
    # 将B0固定档的数据插入到data1中
    data1.append(data2[0])

    # data4中的数据如果是第一种情况：固定基地菜、水菜、菇类、瓜豆、玉米、基地菜
    if (len(data4) == 6):
        # 将data4中的数据分别解构出来、分别是  [固定基地菜、水菜、菇类、瓜豆、玉米、基地菜]
        # data406 = data4.pop()  # 水菜
        # data405 = data4.pop()  # 固定基地菜
        # data404 = data4.pop()  # 菇类
        # data403 = data4.pop()  # 瓜豆
        # data402 = data4.pop()  # 基地菜
        # data401 = data4.pop()  # 玉米

        data406 = data4.pop()  # 基地菜
        data405 = data4.pop()  # 玉米
        data404 = data4.pop()  # 瓜豆
        data403 = data4.pop()  # 菇类
        data402 = data4.pop()  # 水菜
        data401 = data4.pop()  # 固定基地菜

        # 将玉米固定档数据加入到data401玉米数据中
        # for i in range(0, len(data3)):
        #     data401[i] += data3[0][i]

        print('data3', data3)
        for i in range(0, len(data3[0])):
            data405[i] += data3[0][i]

        # 将基地菜和固定基地菜合并到固定基地菜data405中
        # for i in range(0, len(data405)):
        #     data405[i] += data402[i]

        for i in range(0, len(data401)):
            data401[i] += data406[i]

        # 将固定基地菜、玉米、瓜豆、水菜、菇类插入到data1中
        # data1.append(data405)
        # data1.append(data401)
        # data1.append(data403)
        # data1.append(data406)
        # data1.append(data404)

        data1.append(data401)
        data1.append(data405)
        data1.append(data404)
        data1.append(data402)
        data1.append(data403)

    # data4中的数据如果是第二种情况：固定基地菜、水菜、菇类、瓜豆、玉米
    if (len(data4) == 5):
        # 将data4中的数据分别解构出来、分别是  [固定基地菜、水菜、菇类、瓜豆、玉米]
        # data405 = data4.pop()  # 水菜
        # data404 = data4.pop()  # 固定基地菜
        # data403 = data4.pop()  # 菇类
        # data402 = data4.pop()  # 瓜豆
        # data401 = data4.pop()  # 玉米

        data405 = data4.pop()  # 玉米
        data404 = data4.pop()  # 瓜豆
        data403 = data4.pop()  # 菇类
        data402 = data4.pop()  # 水菜--基地菜
        data401 = data4.pop()  # 固定基地菜

        # 将玉米固定档数据加入到data401玉米数据中
        # for i in range(0, len(data3)):
        #     data401[i] += data3[0][i]

        for i in range(0, len(data3[0])):
            data405[i] += data3[0][i]

        # 将固定基地菜、玉米、瓜豆、水菜、菇类插入到data1中
        # data1.append(data404)
        # data1.append(data401)
        # data1.append(data402)
        # data1.append(data405)
        # data1.append(data403)

        data1.append(data401)
        data1.append(data405)
        data1.append(data404)
        data1.append(data402)
        data1.append(data403)

    # data4中的数据于2020.9.11号发现有第三种情况：固定基地菜、水菜数据（菜农菜）、瓜豆、玉米
    if (len(data4) == 4):
        # print("++++++++++++data4",data4)
        # 将data4中的数据分别解构出来、分别是  [固定基地菜、水菜、瓜豆、玉米]
        data404 = data4.pop()  # 玉米
        data403 = data4.pop()  # 瓜豆
        data402 = data4.pop()  # 水菜
        data401 = data4.pop()  # 固定基地菜

        # 将玉米固定档数据加入到data401玉米数据中
        for i in range(0, len(data3[0])):
            data404[i] += data3[0][i]

        # 将固定基地菜、玉米、瓜豆、水菜插入到data1中
        data1.append(data401)
        data1.append(data404)
        data1.append(data403)
        data1.append(data402)
        # 插入菇类的假数据
        data1.append([1,1,1,1,1,1])

    # 将地摊固定档的数据插入到data1中
    data1.append(data5[0])

    # 将冻品D1/D2的数据插入到data1中
    data1.append(D1D2Data)

    # 计算合计的数据并添加到data1中
    sum = []
    for i in range(0, len(data1[0])):
        item = 0
        for j in range(0, len(data1)):
            item += data1[j][i]
        sum.append(item)
    data1.append(sum)

    return data1


def queryData01(currentMonthQueryStr, nextMonthQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询B1、B2、B3、B4、B5、B6、(D1、D2)冻品、数据的sql语句
    sqlStr = '''select * from 
                (
                select 
                        "ROUND"("SUM"(a.SUMNETWEIGHT/1000),2) "来货量(T)",
                        "COUNT"(case when a.TCPARKTYPEOID in (4,148)  then 1 else null end) "拖头车",
                        "COUNT"(case when a.TCPARKTYPEOID in (3) then 1 else null end) "超大型车",
                        "COUNT"(case when a.TCPARKTYPEOID in (2,205)  then 1 else null end) "大型车",
                        "COUNT"(case when a.TCPARKTYPEOID in (168,1,201,202,203,204) then 1 else null end) "小型车",	
                        "COUNT"(case when a.TCPARKTYPEOID in (168,1,201,202,203,204,2,205,3,4,148) then 1 else null end) "合计"
                from 
                (
                select * from ponderation where grosstime between to_date('''\
                + currentMonthQueryStr + ''') and to_date('''+ nextMonthQueryStr + ''')
                ) a
                inner join 
                (
                select * from sf_storefront where seatpos in ('B1交易区', 'B2交易区', 'B3交易区','B4交易区','B5交易区','B6交易区','D1交易区','D2交易区')
                ) c 
                on a.doorway=c.seatno
                GROUP BY c.seatpos
                ORDER BY c.seatpos
                )
                where rownum <=8
                ;'''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def queryData02(currentMonthQueryStr, nextMonthQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询B0固定档数据的sql语句
    sqlStr = '''select "ROUND"("SUM"(a.SUMNETWEIGHT)/1000 , 2) "来货量(吨)",
				"COUNT"(case when a.TCPARKTYPEOID in (4,148)  then 1 else null end) "拖头车",
				"COUNT"(case when a.TCPARKTYPEOID in (3) then 1 else null end) "超大型车",
				"COUNT"(case when a.TCPARKTYPEOID in (2,205)  then 1 else null end) "大型车",
				"COUNT"(case when a.TCPARKTYPEOID in (168,1,201,202,203,204) then 1 else null end) "小型车",	
				"COUNT"(case when a.TCPARKTYPEOID in (168,1,201,202,203,204,2,205,3,4,148) then 1 else null end) "合计"
                from ponderation a
                left join sf_storefront b on a.doorway=b.seatno
                where a.grosstime between to_date(''' \
                + currentMonthQueryStr + ''') and to_date(''' + nextMonthQueryStr + ''')
                and (b.seatno like 'B__' or b.seatno in ('A36', 'A53','A40', 'A37','A38'))
                ;'''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def queryData03(currentMonthQueryStr, nextMonthQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询玉米固定档数据的sql语句
    sqlStr = '''select "ROUND"("SUM"(a.SUMNETWEIGHT)/1000 , 2) "来货量(吨)",
				"COUNT"(case when a.TCPARKTYPEOID in (4,148)  then 1 else null end) "拖头车",
				"COUNT"(case when a.TCPARKTYPEOID in (3) then 1 else null end) "超大型车",
				"COUNT"(case when a.TCPARKTYPEOID in (2,205)  then 1 else null end) "大型车",
				"COUNT"(case when a.TCPARKTYPEOID in (168,1,201,202,203,204) then 1 else null end) "小型车",	
				"COUNT"(case when a.TCPARKTYPEOID in (168,1,201,202,203,204,2,205,3,4,148) then 1 else null end) "合计"
                from ponderation a
                where a.grosstime between to_date(''' \
                + currentMonthQueryStr + ''') and to_date(''' + nextMonthQueryStr + ''')
                and a.BARGAINORDESC in ('周华龙', '陈海生')
                ;'''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def queryData04(currentMonthQueryStr, nextMonthQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询基地菜、玉米、瓜豆、水菜、菇类数据的sql语句
    sqlStr = '''select
				"ROUND"("SUM"(a.SUMNETWEIGHT/1000),2) "来货量(T)",
				"COUNT"(case when a.TCPARKTYPEOID in (4,148)  then 1 else null end) "拖头车",
				"COUNT"(case when a.TCPARKTYPEOID in (3) then 1 else null end) "超大型车",
				"COUNT"(case when a.TCPARKTYPEOID in (2,205)  then 1 else null end) "大型车",
				"COUNT"(case when a.TCPARKTYPEOID in (168,1,201,202,203,204) then 1 else null end) "小型车",	
				"COUNT"(case when a.TCPARKTYPEOID in (168,1,201,202,203,204,2,205,3,4,148) then 1 else null end) "合计"
                from 
                (
                select feetypecode,SUMNETWEIGHT,TCPARKTYPEOID from ponderation where grosstime between to_date(''' \
                + currentMonthQueryStr + ''') and to_date(''' + nextMonthQueryStr + ''')
                ) a
                inner join 
                (
                select charge_typeid, type_name from charge_type where type_name in ('车板区固定基地菜(进门项)', '基地菜(车板项)', '玉米(车板)','瓜豆(进门项)','菇类(进门项)','菜农菜(进门项)')
                ) b 
                on a.feetypecode=b.charge_typeid
                GROUP BY b.type_name
                ORDER BY b.type_name desc;'''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def queryData05(currentMonthQueryStr, nextMonthQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询地摊固定档的sql语句
    sqlStr = '''select "ROUND"("SUM"(a.SUMNETWEIGHT)/1000 , 2) "来货量(吨)",
				"COUNT"(case when a.TCPARKTYPEOID in (4,148)  then 1 else null end) "拖头车",
				"COUNT"(case when a.TCPARKTYPEOID in (3) then 1 else null end) "超大型车",
				"COUNT"(case when a.TCPARKTYPEOID in (2,205)  then 1 else null end) "大型车",
				"COUNT"(case when a.TCPARKTYPEOID in (168,1,201,202,203,204) then 1 else null end) "小型车",	
				"COUNT"(case when a.TCPARKTYPEOID in (168,1,201,202,203,204,2,205,3,4,148) then 1 else null end) "合计"
                from
                (
                select grosstime,doorway,SUMNETWEIGHT,TCPARKTYPEOID from ponderation
                where grosstime between to_date(''' \
                + currentMonthQueryStr + ''') and to_date(''' + nextMonthQueryStr + ''')
                )a
                left join sf_storefront b on a.doorway=b.seatno
                where (b.seatpos='冻品区临时车位' or b.seatpos='D3临时停车位' or b.seatpos='天光区' or b.seatpos='车板地摊区' or b.seatpos='天光区（改造）')
                ;'''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def cheliang(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    year = int(year)
    if (year < 2020):
        data = [
            {"name": "拖头车", "value": 0},
            {"name": "超大型车", "value": 0},
            {"name": "大车", "value": 0},
            {"name": "大车", "value": 0}
        ]
    else:
        data = [
            {"name": "拖头车", "value": 0},
            {"name": "超大型车", "value": 0},
            {"name": "大车", "value": 0},
            {"name": "大车", "value": 0}
        ]

    return JsonResponse(data, safe=False)


def chandi(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    currentMonthQueryStr, nextMonthQueryStr = queryTimeStr(year, month)
    result = queryChandiData(currentMonthQueryStr, nextMonthQueryStr)
    result02 = list(result[:8])
    # print(result, result[8])
    sum = 0
    for i in range(8, len(result)):
        sum = sum + result[i][0]
    result02.append((sum, '其他'))
    data = []
    # 将结果集转换为json数据集
    for item in result02:
        data.append({"name": item[1],"value": item[0]})
    return JsonResponse(data, safe=False)


def queryChandiData(currentMonthQueryStr, nextMonthQueryStr):
    cursor = connection.cursor()
    sqlStr = '''select "ROUND"("SUM"(b.sumnetweight)/1000,0), "SUBSTR"(c.provincecityname, 1, 2)
                from 
                (
                select * from PONDERATIONITEM where indate between to_date(''' \
                + currentMonthQueryStr + \
                ''') and to_date(''' \
                + nextMonthQueryStr + \
                ''')) a 
                INNER JOIN 
                (
                select * from PONDERATION where  GROSSTIME between to_date(''' \
                + currentMonthQueryStr + \
                ''') and to_date(''' \
                + nextMonthQueryStr + \
                ''')
                ) b
                on a.PONDERATIONOID = b.PONDERATIONOID
                INNER JOIN
                PROVINCECITY c on a.PROVINCECITYOID = c.provincecityoid
                GROUP BY a.provincecityoid, c.provincecityname
                ORDER BY "SUM"(b.sumnetweight) desc'''

    cursor.execute(sqlStr)
    result = cursor.fetchall()
    return result


def cheshu(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    currentMonthQueryStr, nextMonthQueryStr = queryTimeStr(year, month)
    result = queryCheshuData(currentMonthQueryStr, nextMonthQueryStr)
    data = []
    for item in result:
        data.append(item[0])
    return JsonResponse(data, safe=False)


def queryCheshuData(currentMonthQueryStr, nextMonthQueryStr):
    cursor = connection.cursor()
    sqlStr = '''SELECT
                count(c.parentid) AS "车数"
                FROM (select PONDERATIONOID, GROSSTIME from PONDERATION where GROSSTIME between to_date('''\
                + currentMonthQueryStr + \
                ''') and to_date('''\
                + nextMonthQueryStr + \
                ''') ) A    
                INNER JOIN PONDERATIONITEM  B 
                ON A.PONDERATIONOID = B.PONDERATIONOID 
                left join T_PRODUCTTYPE_MATCH C on B.productoid = c.producttypematchid   
                WHERE  substr(c.parentid,1,2)=14
                GROUP BY TO_CHAR(A.GROSSTIME, 'DD')   
                ORDER BY TO_CHAR(A.GROSSTIME, 'DD')'''
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    return result


def laihuo(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    currentMonthQueryStr, nextMonthQueryStr = queryTimeStr(year, month)
    result = queryLaihuoData(currentMonthQueryStr, nextMonthQueryStr)
    data = []
    for item in result:
        data.append(item[0])
    return JsonResponse(data, safe=False)


def queryLaihuoData(currentMonthQueryStr, nextMonthQueryStr):
    cursor = connection.cursor()
    sqlStr = '''SELECT
                "ROUND"("SUM"(B.NETWEIGHT)/1000,0) AS "来货量(T)"
                FROM (select PONDERATIONOID, GROSSTIME from PONDERATION where GROSSTIME between to_date('''\
                + currentMonthQueryStr + \
                ''') and to_date('''\
                + nextMonthQueryStr + \
                ''') ) A    
                INNER JOIN PONDERATIONITEM  B 
                ON A.PONDERATIONOID = B.PONDERATIONOID 
                left join T_PRODUCTTYPE_MATCH C on B.productoid = c.producttypematchid   
                WHERE  substr(c.parentid,1,2)=14
                GROUP BY TO_CHAR(A.GROSSTIME, 'DD')   
                ORDER BY TO_CHAR(A.GROSSTIME, 'DD')'''
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    return result


def baobiao02exer(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    # 拼接本月的时间
    currentMonthQueryStr, nextMonthQueryStr = queryTimeStr(year, month)
    # 查询本月数据---车板固定档B0、B1、B2、B3、B4、B5、B6
    currentMonthData01 = queryData11(currentMonthQueryStr, nextMonthQueryStr)

    # 将车板固定档B0移动到后面，变为B1、B2、B3、B4、B5、B6、车板固定档B0
    currentMonthResult = handleData11(currentMonthData01)

    # 查询本月B1、B2、B3、B4、B5、B6来货量的数据
    currentMonthDataB16 = queryDataB16(currentMonthQueryStr, nextMonthQueryStr)

    # 查询本月B0车板固定档来货量的数据
    currentMonthDataB0 = queryDataB0(currentMonthQueryStr, nextMonthQueryStr)

    # 将B0车板固定档来货量的数据和总计的数据添加到B1、B2、B3、B4、B5、B6来货量后面
    currentMonthDataB16 = handleData160(currentMonthDataB16, currentMonthDataB0)

    # 将来货量的数据添加到交易数据currentMonthResult后面
    for i in range(0, len(currentMonthResult)):
        currentMonthResult[i].append(currentMonthDataB16[i][0])

    # 如果本月为1月，则上个月为上一年的12月， 否则为本月减1
    if (month == 1):
        lastMonth = 12
        lastYear = year - 1
    else:
        lastMonth = month - 1
        lastYear = year

    # 拼接上月的时间
    lastMonthQueryStr, nextOfLastMonthQueryStr = queryTimeStr(lastYear, lastMonth)
    # 查询上月数据---车板固定档B0、B1、B2、B3、B4、B5、B6
    lastMonthData01 = queryData11(lastMonthQueryStr, nextOfLastMonthQueryStr)

    # 将车板固定档B0移动到后面，变为B1、B2、B3、B4、B5、B6、车板固定档B0
    lastMonthResult = handleData11(lastMonthData01)

    # 查询本月B1、B2、B3、B4、B5、B6来货量的数据
    lastMonthDataB16 = queryDataB16(lastMonthQueryStr, nextOfLastMonthQueryStr)

    # 查询本月B0车板固定档来货量的数据
    lastMonthDataB0 = queryDataB0(lastMonthQueryStr, nextOfLastMonthQueryStr)


    # 将B0车板固定档来货量的数据和总计的数据添加到B1、B2、B3、B4、B5、B6来货量后面
    lastMonthDataB16 = handleData160(lastMonthDataB16, lastMonthDataB0)

    # 将来货量的数据添加到交易数据lastMonthResult后面
    for i in range(0, len(lastMonthResult)):
        lastMonthResult[i].append(lastMonthDataB16[i][0])

    # 按照报表格式处理各个数据
    Result = handleAllData11(currentMonthResult, lastMonthResult, year, month)

    return JsonResponse(Result, safe=False)


def queryData11(currentMonthQueryStr, nextMonthQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询B1、B2、B3、B4、B5、B6、车板固定档的sql语句
    sqlStr = '''SELECT
			"COUNT"(area) as "总交易笔数",
			"ROUND"("SUM"(sumnetweight)/1000,2) as "交易量(吨)",
			"ROUND"("SUM"(TRADESUM)/10000,2) as "交易额(万元)",
			"ROUND"("SUM"(bargainortradefee)/10000,2) as "交易服务费(万元)"
            from
            (
            SELECT  
			substr(D3.SHOPID, 1, 2) as area,
			t.sumnetweight,
			tradesum,
			(-1 * bargainortradefee) BARGAINORTRADEFEE
            FROM vendeesett t 
            left join customer b2    on t.bargainoroid = b2.customeroid
            left join CUSTOMERSHOP D3    ON b2.CUSTOMEROID = D3.CUSTOMEROID
            where t.tradedate >=TO_DATE('''\
                + currentMonthQueryStr + ''') and t.tradedate <=to_date('''+ nextMonthQueryStr + ''')
            ) res
            where area in ('B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6')
            GROUP BY area
            order BY area;'''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def handleData11(currentMonthData01):
    # 取出currentMonthData01第二位及之后的数据
    data01 = currentMonthData01[1:]
    # 将currentMonthData01第一位的数据添加到data01的最后面
    data01.append(currentMonthData01[0])
    # 计算合计数据
    sumData = [0,0,0,0]
    for i in range(0, len(currentMonthData01[0])):
        for j in range(0, len(currentMonthData01)):
            sumData[i] += currentMonthData01[j][i]

    data01.append(sumData)
    return data01


def handleData160(currentMonthDataB16, currentMonthDataB0):
    currentMonthDataB16.append(currentMonthDataB0[0])
    sum = 0
    for i in range(0, len(currentMonthDataB16)):
        sum += currentMonthDataB16[i][0]
    currentMonthDataB16.append([sum])
    return currentMonthDataB16


def queryDataB16(currentMonthQueryStr, nextMonthQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询B1、B2、B3、B4、B5、B6的sql语句
    sqlStr = '''select * from 
                (
                select "ROUND"("SUM"(a.SUMNETWEIGHT/1000),2) "来货量(T)"
                from 
                (
                select * from ponderation where grosstime between to_date(''' \
                + currentMonthQueryStr + ''') and to_date(''' + nextMonthQueryStr + ''')
                ) a
                inner join 
                (
                select * from sf_storefront where seatpos in ('B1交易区', 'B2交易区', 'B3交易区','B4交易区','B5交易区','B6交易区')
                ) c 
                on a.doorway=c.seatno
                GROUP BY c.seatpos
                ORDER BY c.seatpos
                )
                where rownum <=6
                ;'''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def queryDataB0(currentMonthQueryStr, nextMonthQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询B0车板固定档的sql语句
    sqlStr = '''select "ROUND"("SUM"(a.SUMNETWEIGHT)/1000 , 2) "来货量(吨)"
                from ponderation a
                left join sf_storefront b on a.doorway=b.seatno
                where a.grosstime between to_date(''' \
                + currentMonthQueryStr + ''') and to_date(''' + nextMonthQueryStr + ''')
                and (b.seatno like 'B__' or b.seatno in ('A36', 'A53','A40', 'A37','A38'))
              '''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def handleAllData11(currentMonthResult, lastMonthResult, year, month):
    if (month == 2 and year % 4 == 0 and year % 100 != 0):
        days = 29
    elif (month == 2):
        days=28
    elif (month in (1,3,5,7,8,10,12)):
        days=31
    else:
        days=30

    # 处理总交易笔数、总交易量、交易额的环比数据和日均数
    for i in range(0, len(currentMonthResult)):
        # 格式化总交易笔数环比率如40.17%
        MoM01 = "%.2f%%" % ((currentMonthResult[i][0] / lastMonthResult[i][0] - 1) * 100)
        # 格式化总交易量环比率如40.17%
        MoM02 = "%.2f%%" % ((currentMonthResult[i][1] / lastMonthResult[i][1] - 1) * 100)
        # 格式化交易额环比率如40.17%
        MoM03 = "%.2f%%" % ((currentMonthResult[i][2] / lastMonthResult[i][2] - 1) * 100)
        # 格式化电子结算交易率如427.82%
        rate = "%.2f%%" % ((currentMonthResult[i][1] / currentMonthResult[i][4]) * 100)

        # 格式化日均笔数如3.14
        DoD01 = format(currentMonthResult[i][0] / days, '.2f')
        # 格式化日均交易量如986.53
        DoD02 = format(currentMonthResult[i][1] / days, '.2f')
        # 格式化日均交易额如387.97
        DoD03 = format(currentMonthResult[i][2] / days, '.2f')
        # 格式化日均服务费如387.97
        DoD04 = format(currentMonthResult[i][3] / days, '.2f')

        # 将各个数据插入到currentMonthResult中
        currentMonthResult[i].insert(1, MoM01)
        currentMonthResult[i].insert(2, DoD01)
        currentMonthResult[i].insert(4, MoM02)
        currentMonthResult[i].insert(5, DoD02)
        currentMonthResult[i].insert(7, MoM03)
        currentMonthResult[i].insert(8, DoD03)

        # 插入结算方式的数据
        currentMonthResult[i].insert(9, 0.00)
        currentMonthResult[i].insert(10, 0)
        currentMonthResult[i].insert(11, 0.00)
        currentMonthResult[i].insert(12, '0.00%')
        currentMonthResult[i].insert(13, currentMonthResult[i][6])
        currentMonthResult[i].insert(14, '100.00%')

        # 插入交易服务费的数据
        currentMonthResult[i].insert(15, 0.00)
        currentMonthResult[i].insert(17, currentMonthResult[i][16])
        currentMonthResult[i].insert(18, DoD04)

        # 插入电子结算交易率的数据
        currentMonthResult[i].insert(20, rate)
    return currentMonthResult


def wuye(request):
    # 查询B1-B6及冻品区D1/D2的数据，返回档位号前三位为B10、B20、B30、B40、B50、B60、D10、D20、PB3、PB4、PB5、PB6，需要将D10+D20,PB3-6分别加到B30-B60
    dataB1_6 = queryWuyeDataB1_6()
    # 将PB3、PB4、PB5、PB6、D20依次添加到新的数组中，最后将此数组加回到原数组中
    arr = []
    arr.insert(0, dataB1_6.pop())
    arr.insert(0, dataB1_6.pop())
    arr.insert(0, dataB1_6.pop())
    arr.insert(0, dataB1_6.pop())
    # 将D20添加到数组的最后
    arr.append(dataB1_6.pop())

    # 将arr中的[PB3、PB4、PB5、PB6、D20]加到原数组的B30、B40、B50、B60、D10
    for i in range(0, len(arr)):
        for j in range(0, len(arr[i])):
            dataB1_6[i+2][j] += arr[i][j]

    # 查询车板区、综合市场、天光区数据，返回档位号前一位为A、B、D、E、G、T、Z，其中A+B+D为车板区数据、Z为综合市场、E+G+T为天光区
    dataA_Z = queryWuyeDataA_Z()
    dataA, dataB, dataD, dataE, dataG, dataT, dataZ  = dataA_Z

    # A+B+D为车板区数据
    for i in range(0, len(dataA)):
        dataA[i] = dataA[i] +  dataB[i] +  dataD[i]

    # E+G+T为车板区数据
    for i in range(0, len(dataE)):
        dataE[i] = dataE[i] + dataG[i] + dataT[i]

    # 将车板区、综合市场、天光区的数据依次加到dataB1_6中
    dataB1_6.append(dataA)
    dataB1_6.append(dataZ)
    dataB1_6.append(dataE)

    # 处理合计数据
    sum = [0,0,0,0,0,0]
    for i in range(0, len(dataB1_6)):
        for j in range(0, len(dataB1_6[i])):
            sum[j] += dataB1_6[i][j]
    dataB1_6.append(sum)

    # 处理出租率
    for i in range(0, len(dataB1_6)):
        # 格式化出租率如98.91%
        rate01 = "%.2f%%" % ((dataB1_6[i][1] / dataB1_6[i][0]) * 100)
        rate02 = "%.2f%%" % ((dataB1_6[i][4] / dataB1_6[i][3]) * 100)
        dataB1_6[i].insert(3, rate01)
        dataB1_6[i].insert(7, rate02)

    # 添加已签合同数
    for i in range(0, len(dataB1_6)):
        dataB1_6[i].insert(4, dataB1_6[i][1])

    return JsonResponse(dataB1_6, safe=False)


def queryWuyeDataB1_6():
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询B1-B6数据的sql语句
    sqlStr = '''select 
                    "COUNT"(case when state in ('已租', '待租')  then 1 else null end) "可出租",
                    "COUNT"(case when state='已租' then 1 else null end) "已出租",
                    "COUNT"(case when state='待租' then 1 else null end) "未出租",
                    "SUM"(case when state in ('已租', '待租')  then area else null end) "可出租面积",
                    "SUM"(case when state = '已租'  then area else null end) "已出租面积",
                    "SUM"(case when state='待租' then area else 0 end) "待出租"
                from 
                (
                    select 
                            DISTINCT a.SEATNO, 
                            a.AREA,   
                            CASE WHEN A.SEATNAME='非出租物业' THEN '不可租'         
                            WHEN A.SEATNAME='已停用物业' THEN '已停用'         
                            WHEN NVL(V.SF_STORECONTRACTOID, 0)=0 THEN '待租'         
                            ELSE '已租' END AS STATE
                    from SF_STOREFRONT A  
                    left join sf_storetype t on a.storetype = t.sf_storetypeoid  
                    left join department d on a.departmentoid = d.departmentoid  
                    left join sf_area  sf on a.sf_areaoid = sf.sf_areaoid  
                    left join 
                    (   
                        SELECT G2.SF_STORECONTRACTOID, G1.SF_STOREFRONTOID      
                        FROM SF_STORECONTRACTITEM G1       
                        INNER JOIN SF_STORECONTRACT G2 ON G1.SF_STORECONTRACTOID=G2.SF_STORECONTRACTOID                 
                    ) V 
                    ON V.SF_STOREFRONTOID=A.SF_STOREFRONTOID  
                    where d.name = '蔬菜管理部' and A.SEATNAME in ('可出租物业')
                    and (a.SEATNO like 'B%' or a.SEATNO like 'PB%' or a.SEATNO like 'D1%' or a.SEATNO like 'D2%')
                    and t.sf_storetypename in ('固定档位')
                    order by SEATNO
                ) res
                GROUP BY "SUBSTR"(seatno,0,3)
                ORDER BY "SUBSTR"(seatno,0,3)'''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def queryWuyeDataA_Z():
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询车板区、综合市场、天光区数据的sql语句
    sqlStr = '''select 
                    "COUNT"(case when state in ('已租', '待租')  then 1 else null end) "可出租",
                    "COUNT"(case when state='已租' then 1 else null end) "已出租",
                    "COUNT"(case when state='待租' then 1 else null end) "未出租",
                    "SUM"(case when state in ('已租', '待租')  then area else null end) "可出租面积",
                    "SUM"(case when state = '已租'  then area else null end) "已出租面积",
                    "SUM"(case when state='待租' then area else 0 end) "待出租"
                from
                (
                    select 
                        DISTINCT a.SEATNO, 
                        a.AREA,
                        CASE WHEN A.SEATNAME='非出租物业' THEN '不可租'         
                        WHEN A.SEATNAME='已停用物业' THEN '已停用'         
                        WHEN NVL(V.SF_STORECONTRACTOID, 0)=0 THEN '待租'         
                        ELSE '已租' END AS STATE      
                    from SF_STOREFRONT A  
                    left join sf_storetype t on a.storetype = t.sf_storetypeoid  
                    left join department d on a.departmentoid = d.departmentoid  
                    left join sf_area  sf on a.sf_areaoid = sf.sf_areaoid  
                    left join 
                    (   
                        SELECT G2.SF_STORECONTRACTOID, G1.SF_STOREFRONTOID      
                        FROM SF_STORECONTRACTITEM G1       
                        INNER JOIN SF_STORECONTRACT G2 ON G1.SF_STORECONTRACTOID=G2.SF_STORECONTRACTOID             
                        AND SYSDATE>=G2.BEGINDATE AND SYSDATE<=G2.ENDDATE      
                    ) V 
                    ON V.SF_STOREFRONTOID=A.SF_STOREFRONTOID  
                    where d.name = '蔬菜管理部' and A.SEATNAME in ('可出租物业') and t.sf_storetypename in ('地摊', '综合批发', '车板区档位')
                    order by SEATNO
                ) res
                where "SUBSTR"(seatno,0,1) != 'Q'
                GROUP BY "SUBSTR"(seatno,0,1)
                ORDER BY "SUBSTR"(seatno,0,1)'''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def queryItem(request):
    item_no = int(request.GET.get('item_no'))
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    # 拼接查询时间字符串
    currentMonthQueryStr, nextMonthQueryStr = queryTimeStr(year, month)

    data = queryItemData(item_no, currentMonthQueryStr, nextMonthQueryStr)
    return JsonResponse(data, safe=False)


def queryItemData(item_no, currentMonthQueryStr, nextMonthQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询语句
    sqlStr = '''SELECT * from "economic_task_rp"
                where "item_no" = %d and "create_time">="TO_DATE"(%s)
                and "create_time"<="TO_DATE"(%s)
                '''%(item_no, currentMonthQueryStr, nextMonthQueryStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def updateItem(request):
    if request.method == 'POST':
        res = 'OK'
        data = (request.body).decode()
        updateDataArr = data.split(',')

        # 执行数据update操作, 返回更新影响的行数
        rowcount = update(updateDataArr)

        return JsonResponse(rowcount, safe=False)


def update(data):
    # 解析data成各个更新数据
    itemId = int(data[0])
    item_no = int(data[1])
    item_name = data[2]
    budget_allyear = float(data[3])
    budget_month_accumulative = float(data[4])
    receipts_month_accumulative = float(data[5])
    completion_rate_accumulative = data[6]
    budget_completion_rate = data[7]
    last_year = float(data[8])
    growth_rate = data[9]
    Arrears_accumulative = float(data[10])
    receivable_currentmonth = float(data[11])
    receipts_currentmonth = float(data[12])
    completion_rate_currentmonth = data[13]
    create_time = data[14]
    create_time += '  11-11-11'

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接update的sql语句
    sqlStr = '''update "economic_task_rp" set "item_no"=%d, "item_name"='%s', "budget_allyear" = %.2f, "budget_month_accumulative"=%.2f,
                      "receipts_month_accumulative"=%.2f, "completion_rate_accumulative"='%s',
                      "budget_completion_rate"= '%s', "last_year"=%.2f, "growth_rate"='%s', "Arrears_accumulative"=%.2f,
                      "receivable_currentmonth"=%.2f, "receipts_currentmonth"=%.2f, "completion_rate_currentmonth"='%s',"create_time"="TO_DATE"('%s', 'YYYY-MM-DD HH24:mi:ss')
                where "itemId" = %d;'''%(item_no, item_name, budget_allyear, budget_month_accumulative,
                                          receipts_month_accumulative, completion_rate_accumulative,
                                          budget_completion_rate, last_year, growth_rate, Arrears_accumulative,
                                          receivable_currentmonth, receipts_currentmonth, completion_rate_currentmonth, create_time, itemId)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def addItem(request):
    if request.method == 'POST':
        data = (request.body).decode()
        addDataArr = data.split(',')

        # 先按照item_no和时间查询数据，如果有则不能执行插入操作，否则插入
        item_no = int(addDataArr[0])
        create_time = addDataArr[13]
        year = int(create_time.split('-')[0])
        month = int(create_time.split('-')[1])

        # 拼接查询时间字符串
        currentMonthQueryStr, nextMonthQueryStr = queryTimeStr(year, month)

        result = queryItemData(item_no, currentMonthQueryStr, nextMonthQueryStr)
        # print(result)
        if(result):
            return JsonResponse(400, safe=False)
        else:
            # 执行数据update操作, 返回更新影响的行数
            rowcount = add(addDataArr)

            return JsonResponse(200, safe=False)


def add(data):
    # 解析data成各个更新数据
    item_no = int(data[0])
    item_name = data[1]
    budget_allyear = float(data[2])
    budget_month_accumulative = float(data[3])
    receipts_month_accumulative = float(data[4])
    completion_rate_accumulative = data[5]
    budget_completion_rate = data[6]
    last_year = float(data[7])
    growth_rate = data[8]
    Arrears_accumulative = float(data[9])
    receivable_currentmonth = float(data[10])
    receipts_currentmonth = float(data[11])
    completion_rate_currentmonth = data[12]
    create_time = data[13]
    create_time += '  11-11-11'

    # 建立游标对象
    cursor = connection.cursor()
    # 拼接update的sql语句
    sqlStr = '''insert into "economic_task_rp"("itemId","item_no","item_name" , "budget_allyear", "budget_month_accumulative",
                  "receipts_month_accumulative", "completion_rate_accumulative","budget_completion_rate", "last_year", "growth_rate",
                   "Arrears_accumulative","receivable_currentmonth", "receipts_currentmonth","completion_rate_currentmonth","create_time") 
                values(economic_task_itemid.nextval, %d,'%s', %.2f,%.2f,%.2f,'%s','%s',%.2f,'%s',%.2f,%.2f,%.2f,'%s',"TO_DATE"('%s', 'YYYY-MM-DD HH24:mi:ss'))
                '''%(item_no, item_name, budget_allyear, budget_month_accumulative,
                      receipts_month_accumulative, completion_rate_accumulative,
                      budget_completion_rate, last_year, growth_rate, Arrears_accumulative,
                      receivable_currentmonth, receipts_currentmonth, completion_rate_currentmonth, create_time)

    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # # 取到游标对象里面的执行结果
    rowcount = cursor.rowcount
    cursor.execute('commit')

    return rowcount


def economicTask(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    # 拼接本月的时间
    currentMonthQueryStr, nextMonthQueryStr = queryTimeStr(year, month)
    # 查询本月数据
    currentMonthData = queryEconomicData(currentMonthQueryStr, nextMonthQueryStr)

    return JsonResponse(currentMonthData, safe=False)


def queryEconomicData(currentMonthQueryStr, nextMonthQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询数据的sql语句
    sqlStr = '''SELECT * from "economic_task_rp"
                where "create_time" >= "TO_DATE"(%s)
                and "create_time" < "TO_DATE"(%s)
                ORDER BY "item_no" asc'''%(currentMonthQueryStr, nextMonthQueryStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    return resArray


def baobiao06(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    day = int(request.GET.get('day'))

    # 拼接今天的时间
    currentDayQueryStr, nextDayQueryStr = queryTimeStr02(year, month, day)
    # 查询今天数据---B1、B2、B3、B4、B5、B6
    currentDayDataB16 = queryData06_B16(currentDayQueryStr, nextDayQueryStr)
    # 查询今天数据---固定基地菜、水菜数据、菇类、瓜豆、玉米、基地菜、
    currentDayDataCB = queryData06_CB(currentDayQueryStr, nextDayQueryStr)
    # 查询今天数据---玉米固定档的数据
    currentDayDataYM = queryData06_YM(currentDayQueryStr, nextDayQueryStr)
    # 查询今天数据---车板固定档的数据
    currentDayDataCBGDD = queryData06_CBGDD(currentDayQueryStr, nextDayQueryStr)
    # 查询今天数据---天光区的数据
    currentDayDataTG = queryData06_TG(currentDayQueryStr, nextDayQueryStr)

    # 按照日报报表格式处理今天的各个数据
    currentDayResult = handleDayData(currentDayDataB16, currentDayDataCBGDD, currentDayDataYM, currentDayDataCB, currentDayDataTG)

    # 拼接昨天的时间
    lastDayQueryStr, nextOfLastDayQueryStr = queryTimeStr03(year, month, day)
    # 查询昨天数据---B1、B2、B3、B4、B5、B6
    lastDayDataB16 = queryData06_B16(lastDayQueryStr, nextOfLastDayQueryStr)
    # 查询昨天数据---固定基地菜、水菜数据、菇类、瓜豆、玉米、基地菜、
    lastDayDataCB = queryData06_CB(lastDayQueryStr, nextOfLastDayQueryStr)
    # 查询昨天数据---玉米固定档的数据
    lastDayDataYM = queryData06_YM(lastDayQueryStr, nextOfLastDayQueryStr)
    # 查询昨天数据---车板固定档的数据
    lastDayDataCBGDD = queryData06_CBGDD(lastDayQueryStr, nextOfLastDayQueryStr)
    # 查询昨天数据---天光区的数据
    lastDayDataTG = queryData06_TG(lastDayQueryStr, nextOfLastDayQueryStr)

    # 按照日报报表格式处理昨天的各个数据
    lastDayResult = handleDayData(lastDayDataB16, lastDayDataCBGDD, lastDayDataYM, lastDayDataCB, lastDayDataTG)

    # 处理今日和昨日的数据
    result = handleData_DoD(currentDayResult, lastDayResult)

    print('res', result)

    return JsonResponse(result, safe=False)


def queryTimeStr02(year, month, day):
    currentDayQueryStr = "'%s-%s-%s 00:00:00', 'YYYY-MM-DD HH24:mi:ss'" % (str(year), str(month), str(day))
    todayStr = str(year) + '-' + str(month) + '-' + str(day)
    todayToDate = datetime.datetime.strptime(todayStr, '%Y-%m-%d')
    tomorrowStr = todayToDate + datetime.timedelta(days=1)
    nextDayQueryStr = "'%s', 'YYYY-MM-DD HH24:mi:ss'" % (tomorrowStr)
    return [currentDayQueryStr, nextDayQueryStr]


def queryTimeStr03(year, month, day):
    currentDayQueryStr = "'%s-%s-%s 00:00:00', 'YYYY-MM-DD HH24:mi:ss'" % (str(year), str(month), str(day))
    todayStr = str(year) + '-' + str(month) + '-' + str(day)
    todayToDate = datetime.datetime.strptime(todayStr, '%Y-%m-%d')
    yesterdayStr = todayToDate + datetime.timedelta(days=-1)
    lastDayQueryStr = "'%s', 'YYYY-MM-DD HH24:mi:ss'" % (yesterdayStr)
    return [lastDayQueryStr, currentDayQueryStr]


def queryData06_B16(currentDayQueryStr, nextDayQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询B1、B2、B3、B4、B5、B6数据的sql语句
    sqlStr = '''select  "ROUND"("SUM"(a.SUMNETWEIGHT/1000),2) "来货量(T)"
                from 
                (
                select * from ponderation where grosstime between to_date(%s) and to_date(%s)
                ) a
                inner join 
                (
                select * from sf_storefront where seatpos in ('B1交易区', 'B2交易区', 'B3交易区','B4交易区','B5交易区','B6交易区')
                ) c 
                on a.doorway=c.seatno
                GROUP BY c.seatpos
                ORDER BY c.seatpos'''%(currentDayQueryStr, nextDayQueryStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    # print('DoD++++++++++', resArray)
    return resArray


def queryData06_CB(currentDayQueryStr, nextDayQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询固定基地菜、水菜数据、菇类、瓜豆、玉米、基地菜数据的sql语句
    sqlStr = '''select  
                       "ROUND"("SUM"(a.SUMNETWEIGHT/1000),2) "来货量(T)",
                       "ROUND"("SUM"(a.tradefee),2) "过磅金额"
                from 
                (
                select feetypecode,SUMNETWEIGHT,TCPARKTYPEOID,TRADEFEE from ponderation where grosstime between to_date(%s) and to_date(%s)
                ) a
                inner join 
                (
                select charge_typeid, type_name from charge_type where type_name in ('车板区固定基地菜(进门项)', '基地菜(车板项)', '玉米(车板)','瓜豆(进门项)','菇类(进门项)','菜农菜(进门项)')
                ) b 
                on a.feetypecode=b.charge_typeid
                GROUP BY b.type_name
                ORDER BY b.type_name desc'''%(currentDayQueryStr, nextDayQueryStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    # print('DoD++++++++++', resArray)
    return resArray


def queryData06_YM(currentDayQueryStr, nextDayQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询玉米固定档数据的sql语句
    sqlStr = '''select "ROUND"("SUM"(a.SUMNETWEIGHT)/1000 , 2) "来货量(吨)"
                from ponderation a
                    where a.grosstime between to_date(%s) and to_date(%s)
                    and ( a.BARGAINORDESC in ('周华龙', '陈海生') )'''%(currentDayQueryStr, nextDayQueryStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    # print('DoD++++++++++', resArray)
    return resArray


def queryData06_CBGDD(currentDayQueryStr, nextDayQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询车板固定档数据的sql语句
    sqlStr = '''select 
                    "ROUND"("SUM"(a.SUMNETWEIGHT)/1000 , 2) "来货量(吨)"
                from ponderation a
                left join sf_storefront b on a.doorway=b.seatno
                where a.grosstime between to_date(%s) and to_date(%s)
                and (b.seatno like 'B__' or b.seatno in ('A36', 'A53','A40', 'A37','A38'))'''%(currentDayQueryStr, nextDayQueryStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    # print('DoD++++++++++', resArray)
    return resArray


def queryData06_TG(currentDayQueryStr, nextDayQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询天光区数据的sql语句
    sqlStr = '''select 
                    "ROUND"("SUM"(a.SUMNETWEIGHT)/1000 , 2) "来货量(吨)"
                from
                (
                select grosstime,doorway,SUMNETWEIGHT,TCPARKTYPEOID,TRADEFEE from ponderation
                where grosstime between to_date(%s) and to_date(%s) 
                )a
                left join sf_storefront b on a.doorway=b.seatno
                where (b.seatpos='冻品区临时车位' or b.seatpos='D3临时停车位' or b.seatpos='天光区' or b.seatpos='车板地摊区' or b.seatpos='天光区（改造）')
                '''%(currentDayQueryStr, nextDayQueryStr)
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    # print('DoD++++++++++', resArray)
    return resArray


def handleDayData(data1, data2, data3, data4, data5):
    """
    :param data1: B1、B2、B3、B4、B5、B6、(D1、D2)冻品的数据
    :param data2: 车板固定档数据
    :param data3: 玉米固定档数据
    :param data4: 第一种情况：固定基地菜、水菜、菇类、瓜豆、玉米、基地菜 或者是第二种情况： 固定基地菜、水菜、菇类、瓜豆、玉米、或者是第三种情况： 固定基地菜、水菜数据（菜农菜）、瓜豆、玉米
    :param data5: 天光区数据
    :return: data1为最终结果集
    """
    # print('data1, data2, data3, data4, data5', data1, data2, data3, data4, data5)
    #
    # print("++++++++++++++++++++++++++++++++")
    # print("data3+++", type(data3[0][0]) == type(None))
    # print("++++++++++++++++++++++++++++++++")
    # data4中的数据如果是第一种情况：固定基地菜、水菜、菇类、瓜豆、玉米、基地菜
    if (len(data4) == 6):
        # 将data4中的数据分别解构出来、分别是  [固定基地菜、水菜、菇类、瓜豆、玉米、基地菜]
        data406 = data4.pop()  # 基地菜
        data405 = data4.pop()  # 玉米
        data404 = data4.pop()  # 瓜豆
        data403 = data4.pop()  # 菇类
        data402 = data4.pop()  # 水菜
        data401 = data4.pop()  # 固定基地菜

        # 将data405玉米数据加入到玉米固定档数据中
        # for i in range(0, len(data3[0])):
        #     data3[0][i] += data405[i]
        if (type(data3[0][0]) == type(None)):
            data3[0] = data405
        else:
            data3[0][0] += data405[0]



        # 将固定基地菜、基地菜、玉米临时、临时瓜豆、临时水菜、临时菇类中的来货量和过磅金额分别结构出来
        data401_L, data401_G = data401  # 固定基地菜
        data406_L, data406_G = data406  # 基地菜
        data405_L, data405_G = data405  # 玉米临时
        data404_L, data404_G = data404  # 临时瓜豆
        data402_L, data402_G = data402  # 临时水菜
        data403_L, data403_G = data403  # 临时菇类

        # 计算车板区总来货量及过磅金额
        dataAll_CB_L = data401_L + data406_L + data404_L + data402_L + data403_L + data3[0][0] + data2[0][0]
        dataAll_CB_G = data401_G + data406_G + data405_G + data404_G + data402_G + data403_G

        # 计算大档区来货量
        dataAll_B16 = 0
        for i in range(0, len(data1)):
            dataAll_B16 += data1[i][0]

        # 计算区域蔬菜总来货量
        dataAll = dataAll_B16 + dataAll_CB_L + data5[0][0]

        # 按照报表格式组装回数据
        result = [dataAll, dataAll_B16, data1[0][0], data1[1][0], data1[2][0], data1[3][0], data1[4][0], data1[5][0],
                  dataAll_CB_L, dataAll_CB_G, data401_L, data401_G, data406_L, data406_G, data3[0][0], data405_L,
                  data405_G,data2[0][0], data404_L, data404_G, data402_L, data402_G, data403_L, data403_G, data5[0][0]]
        print('result1++', result)

        return result

    # data4中的数据如果是第二种情况：固定基地菜、水菜、菇类、瓜豆、玉米
    if (len(data4) == 5):
        # 将data4中的数据分别解构出来、分别是  [固定基地菜、水菜、菇类、瓜豆、玉米]
        data405 = data4.pop()  # 玉米
        data404 = data4.pop()  # 瓜豆
        data403 = data4.pop()  # 菇类
        data402 = data4.pop()  # 水菜--菜农菜
        data401 = data4.pop()  # 固定基地菜

        # 将data405玉米档数据加入到玉米固定数据中
        # for i in range(0, len(data3[0])):
        #     data3[0][i] += data405[i]
        if (type(data3[0][0]) == type(None)):
            data3[0] = data405
        else:
            data3[0][0] += data405[0]


        # 将固定基地菜、玉米临时、临时瓜豆、临时水菜、临时菇类中的来货量和过磅金额分别结构出来
        data401_L, data401_G = data401  # 固定基地菜
        data406_L, data406_G = 0, 0  # 基地菜
        data405_L, data405_G = data405  # 玉米临时
        data404_L, data404_G = data404  # 临时瓜豆
        data402_L, data402_G = data402  # 临时水菜
        data403_L, data403_G = data403  # 临时菇类

        # 计算车板区总来货量及过磅金额
        dataAll_CB_L = data401_L + data404_L + data402_L + data403_L + data3[0][0] + data2[0][0]
        dataAll_CB_G = data401_G + data405_G + data404_G + data402_G + data403_G

        # 计算大档区来货量
        dataAll_B16 = 0
        for i in range(0, len(data1)):
            dataAll_B16 += data1[i][0]

        # 计算区域蔬菜总来货量
        dataAll = dataAll_B16 + dataAll_CB_L + data5[0][0]

        # 按照报表格式组装回数据
        result = [dataAll, dataAll_B16, data1[0][0], data1[1][0], data1[2][0], data1[3][0], data1[4][0], data1[5][0],
                  dataAll_CB_L, dataAll_CB_G, data401_L, data401_G, data406_L, data406_G, data3[0][0], data405_L,
                  data405_G,data2[0][0], data404_L, data404_G, data402_L, data402_G, data403_L, data403_G, data5[0][0]]
        print('result2++', result)

        return result

    # data4中的数据于2020.9.11号发现有第三种情况：固定基地菜、水菜数据（菜农菜）、瓜豆、玉米
    if (len(data4) == 4):
        # 将data4中的数据分别解构出来、分别是  [固定基地菜、水菜、瓜豆、玉米]
        data401 = data4.pop()  # 固定基地菜
        data405 = data4.pop()  # 玉米
        data404 = data4.pop()  # 瓜豆
        data402 = data4.pop()  # 水菜


        # 将data405玉米数据加入到玉米固定档数据中
        # for i in range(0, len(data3[0])):
        #     data3[0][i] += data405[i]
        if (type(data3[0][0]) == type(None)):
            data3[0] = data405
        else:
            data3[0][0] += data405[0]

        # 将固定基地菜、玉米临时、临时瓜豆、临时水菜中的来货量和过磅金额分别结构出来
        data401_L, data401_G = data401  # 固定基地菜
        data406_L, data406_G = 0, 0  # 基地菜
        data405_L, data405_G = data405  # 玉米临时
        data404_L, data404_G = data404  # 临时瓜豆
        data402_L, data402_G = data402  # 临时水菜
        data403_L, data403_G = 0, 0  # 临时菇类
        print(data401_L , data402_L , data404_L ,data3[0][0] ,data2[0][0])

        # 计算车板区总来货量及过磅金额
        dataAll_CB_L = data401_L + data402_L + data404_L + data3[0][0] + data2[0][0]
        dataAll_CB_G = data401_G + data405_G + data402_G + data404_G

        # 计算大档区来货量
        dataAll_B16 = 0
        for i in range(0, len(data1)):
            dataAll_B16 += data1[i][0]

        # 计算区域蔬菜总来货量
        dataAll = dataAll_B16 + dataAll_CB_L + data5[0][0]

        # 按照报表格式组装回数据
        result = [dataAll, dataAll_B16, data1[0][0], data1[1][0], data1[2][0], data1[3][0], data1[4][0], data1[5][0],
                  dataAll_CB_L, dataAll_CB_G, data401_L, data401_G, data406_L, data406_G, data3[0][0], data405_L,
                  data405_G,data2[0][0], data404_L, data404_G, data402_L, data402_G, data403_L, data403_G, data5[0][0]]
        print('result3++', result)

        return result


def handleData_DoD(currentDayResult, lastDayResult):
    result = []
    # print('-----------------------------')
    # print(currentDayResult)
    # print('-----------------------------')
    # print(lastDayResult)
    # print('-----------------------------')
    for i in range(0, len(currentDayResult)):
        # 增减量
        amount = currentDayResult[i] - lastDayResult[i]
        # 增减幅度
        try:
            DoD  = "%.2f%%"%((amount/lastDayResult[i])*100)
        except:
            DoD = 0.0
        # 添加一行数据
        result.append([lastDayResult[i], currentDayResult[i], amount, DoD])
    return result


def queryDoD(request):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询车板区、综合市场、天光区数据的sql语句
    sqlStr = '''SELECT 
                v.SERIALNO,
                v.CUSTOMERID,
                v.CUSTOMERNAME,
                v.DOORWAY,
                v.PRODUCTID,
                v.BI_GOODSSORTNA,
                v.PRODUCTTYPE2,
                v.PRODUCTTYPE3,
                v.PRODUCTNAME_XX,
                v.GROSSSUM,
                v.SUMNETWEIGHT,
                v.TARESUM,
                v.ISTARE,
                v.GOODSFLAGNAME,
                v.VEHICLETYPENAME,
                v.VEHICLEDESC,
                v.GROSSTIME,
                v.BILLSTATENAME,
                v.PROVINCECITYNAME,
                v.GROSSOPERATORNAME
                from V_REPPONDER_PRODUCT_V2 v 
                where v.GROSSTIME between to_date('2020-08-01 00:00:00', 'YYYY-MM-DD HH24:mi:ss') and to_date('2020-08-02 00-00-00', 'YYYY-MM-DD HH24:mi:ss')
                and v.BI_GOODSSORTNA LIKE '%蔬菜%' '''
    # 游标对象执行sql语句
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        resArray.append(list(item))
    print('DoD++++++++++', resArray)
    return resArray


def baobiao07(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    day = int(request.GET.get('day'))

    # 拼接查询的时间字符串
    currentDayQueryStr, nextDayQueryStr = queryTimeStr02(year, month, day)
    print(currentDayQueryStr, nextDayQueryStr)
    # 查询数据
    currentDayData = queryCurrentDayData(currentDayQueryStr, nextDayQueryStr)

    # 处理成符合格式的数据
    result = []
    for i in range(0, len(currentDayData)):
        # for j in range(0, len(currentDayData[i])):
        map = {"customername": currentDayData[i][0],
               "doorway": currentDayData[i][1],
               "BI_goodssortna": currentDayData[i][2],
               "producttype2": currentDayData[i][3],
               "producttype3": currentDayData[i][4],
               "productname_xx": currentDayData[i][5],
               "grossweight": currentDayData[i][6],
               "tareweight": currentDayData[i][7],
               "netweight": currentDayData[i][8],
               "goodsflagname": currentDayData[i][9],
               "vehicletypename": currentDayData[i][10],
               "vehicledesc": currentDayData[i][11],
               "grosstime": currentDayData[i][12],
               "provincecityname": currentDayData[i][13],
               "grossoperatorname": currentDayData[i][14]
               }
        result.append(map)

    return JsonResponse(result, safe=False)


def baobiao08(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))

    year = request.COOKIES['year']
    month = request.COOKIES['month']
    day = request.COOKIES['day']

    # 拼接查询的时间字符串
    currentDayQueryStr, nextDayQueryStr = queryTimeStr02(year, month, day)

    # 查询混装数据
    data_mix = queryData_mix(currentDayQueryStr, nextDayQueryStr)

    # 查询数据
    currentDayData = queryCurrentDayData(currentDayQueryStr, nextDayQueryStr, data_mix)

    start = (page - 1) * limit
    count = len(currentDayData)
    if count < limit * page:
        end = count
    else:
        end = limit * page

    # 处理成符合格式的数据
    data = []
    for i in range(start, end):
        # for j in range(0, len(currentDayData[i])):
        map = {"customername": currentDayData[i][0],
               "doorway": currentDayData[i][1],
               "BI_goodssortna": currentDayData[i][2],
               "producttype2": currentDayData[i][3],
               "producttype3": currentDayData[i][4],
               "productname_xx": currentDayData[i][5],
               "grossweight": currentDayData[i][6],
               "tareweight": currentDayData[i][7],
               "netweight": currentDayData[i][8],
               "goodsflagname": currentDayData[i][9],
               "vehicletypename": currentDayData[i][10],
               "vehicledesc": currentDayData[i][11],
               "grosstime": currentDayData[i][12],
               "provincecityname": currentDayData[i][13],
               "grossoperatorname": currentDayData[i][14]
               }
        data.append(map)
    result = {"code": 0, "msg": "", "count": count, "data": data}
    return JsonResponse(result, safe=False)


def queryData_mix(currentDayQueryStr, nextDayQueryStr):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询数据的sql语句
    sqlStr = '''select a.PONDERATIONoid,
                       a.NETWEIGHT,
                       a.PRODUCTNAME
                from ponderationitem a
                INNER JOIN  T_PRODUCTTYPE_MATCH c on a.PRODUCTOID = c.PRODUCTTYPEMATCHID
                where  a.PONDERATIONOID in 
                (
                    select b.ponderationoid 
                    from V_REPPONDER_PRODUCT_V2 b
                    where b.grosstime BETWEEN "TO_DATE"(''' + currentDayQueryStr + ''') and "TO_DATE"(''' + nextDayQueryStr + ''')
                    and b.goodsflag = 2
                    and b.BI_goodssortna like '%蔬菜%' 
                ) and "SUBSTR"(c.PARENTID,0,2) = '14' '''
    # 游标对象执行sql语句
    # print(sqlStr)
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        item = list(item)
        resArray.append(item)

    print('DoD++++++++++', resArray)
    return resArray


def baobiao08_searchDoorway(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    key = request.GET.get('key')

    year = request.COOKIES['year']
    month = request.COOKIES['month']
    day = request.COOKIES['day']

    # 拼接查询的时间字符串
    currentDayQueryStr, nextDayQueryStr = queryTimeStr02(year, month, day)

    # 查询混装数据
    data_mix = queryData_mix(currentDayQueryStr, nextDayQueryStr)

    # 查询数据
    currentDayData = queryCurrentDayData_searchDoorway(currentDayQueryStr, nextDayQueryStr, key, data_mix)

    start = (page - 1) * limit
    count = len(currentDayData)
    if count < limit * page:
        end = count
    else:
        end = limit * page

    # 处理成符合格式的数据
    data = []
    for i in range(start, end):
        # for j in range(0, len(currentDayData[i])):
        map = {"customername": currentDayData[i][0],
               "doorway": currentDayData[i][1],
               "BI_goodssortna": currentDayData[i][2],
               "producttype2": currentDayData[i][3],
               "producttype3": currentDayData[i][4],
               "productname_xx": currentDayData[i][5],
               "grossweight": currentDayData[i][6],
               "tareweight": currentDayData[i][7],
               "netweight": currentDayData[i][8],
               "goodsflagname": currentDayData[i][9],
               "vehicletypename": currentDayData[i][10],
               "vehicledesc": currentDayData[i][11],
               "grosstime": currentDayData[i][12],
               "provincecityname": currentDayData[i][13],
               "grossoperatorname": currentDayData[i][14]
               }
        data.append(map)
    result = {"code": 0, "msg": "", "count": count, "data": data}
    return JsonResponse(result, safe=False)


def baobiao08_searchVehicledesc(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    key = request.GET.get('key')

    year = request.COOKIES['year']
    month = request.COOKIES['month']
    day = request.COOKIES['day']

    # 拼接查询的时间字符串
    currentDayQueryStr, nextDayQueryStr = queryTimeStr02(year, month, day)

    # 查询混装数据
    data_mix = queryData_mix(currentDayQueryStr, nextDayQueryStr)

    # 查询数据
    currentDayData = queryCurrentDayData_searchVehicledesc(currentDayQueryStr, nextDayQueryStr, key, data_mix)

    start = (page - 1) * limit
    count = len(currentDayData)
    if count < limit * page:
        end = count
    else:
        end = limit * page

    # 处理成符合格式的数据
    data = []
    for i in range(start, end):
        # for j in range(0, len(currentDayData[i])):
        map = {"customername": currentDayData[i][0],
               "doorway": currentDayData[i][1],
               "BI_goodssortna": currentDayData[i][2],
               "producttype2": currentDayData[i][3],
               "producttype3": currentDayData[i][4],
               "productname_xx": currentDayData[i][5],
               "grossweight": currentDayData[i][6],
               "tareweight": currentDayData[i][7],
               "netweight": currentDayData[i][8],
               "goodsflagname": currentDayData[i][9],
               "vehicletypename": currentDayData[i][10],
               "vehicledesc": currentDayData[i][11],
               "grosstime": currentDayData[i][12],
               "provincecityname": currentDayData[i][13],
               "grossoperatorname": currentDayData[i][14]
               }
        data.append(map)
    result = {"code": 0, "msg": "", "count": count, "data": data}
    return JsonResponse(result, safe=False)


def baobiao08_searchProvincecityname(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    key = request.GET.get('key')

    year = request.COOKIES['year']
    month = request.COOKIES['month']
    day = request.COOKIES['day']

    # 拼接查询的时间字符串
    currentDayQueryStr, nextDayQueryStr = queryTimeStr02(year, month, day)

    # 查询混装数据
    data_mix = queryData_mix(currentDayQueryStr, nextDayQueryStr)

    # 查询数据
    currentDayData = queryCurrentDayData_searchProvincecityname(currentDayQueryStr, nextDayQueryStr, key, data_mix)

    start = (page - 1) * limit
    count = len(currentDayData)
    if count < limit * page:
        end = count
    else:
        end = limit * page

    # 处理成符合格式的数据
    data = []
    for i in range(start, end):
        # for j in range(0, len(currentDayData[i])):
        map = {"customername": currentDayData[i][0],
               "doorway": currentDayData[i][1],
               "BI_goodssortna": currentDayData[i][2],
               "producttype2": currentDayData[i][3],
               "producttype3": currentDayData[i][4],
               "productname_xx": currentDayData[i][5],
               "grossweight": currentDayData[i][6],
               "tareweight": currentDayData[i][7],
               "netweight": currentDayData[i][8],
               "goodsflagname": currentDayData[i][9],
               "vehicletypename": currentDayData[i][10],
               "vehicledesc": currentDayData[i][11],
               "grosstime": currentDayData[i][12],
               "provincecityname": currentDayData[i][13],
               "grossoperatorname": currentDayData[i][14]
               }
        data.append(map)
    result = {"code": 0, "msg": "", "count": count, "data": data}
    return JsonResponse(result, safe=False)


def queryCurrentDayData(currentDayQueryStr, nextDayQueryStr, data_mix):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询数据的sql语句
    sqlStr = '''select 
                    v.customername,
                    v.doorway,
                    v.BI_goodssortna,
                    v.producttype2,
                    v.producttype3,
                    v.productname_xx,
                    v.grossweight,
                    v.tareweight,
                    v.netweight,
                    v.goodsflagname,
                    v.vehicletypename,
                    v.vehicledesc,
                    v.grosstime,
                    v.provincecityname,
                    v.grossoperatorname,
                    v.ponderationoid
                from V_REPPONDER_PRODUCT_V2 v 
                where v.grosstime BETWEEN "TO_DATE"(''' + currentDayQueryStr + ''') and "TO_DATE"(''' + nextDayQueryStr + ''')
                and v.BI_goodssortna like '%蔬菜%' '''
    # 游标对象执行sql语句
    # print(sqlStr)
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        item = list(item)
        if item[9] == '混装':

            # 取出该混装对应的数据
            result_mix = []
            for mix in data_mix:
                if mix[0] == item[15]:
                    result_mix.append(mix)
            # print(result_mix)

            arr_item_BI_goodssortna = item[2].split(',')
            arr_item_BI_producttype2 = item[3].split(',')
            arr_item_BI_producttype3 = item[4].split(',')
            arr_item_BI_productname_xx = item[5].split(',')
            arr_item_BI_provincecityname = item[13].split(',')
            for i in range(0, len(result_mix)):
                if i == 0:
                    item_i = [item[0],item[1],arr_item_BI_goodssortna[i],arr_item_BI_producttype2[i],
                              arr_item_BI_producttype3[i],result_mix[i][2], item[6],item[7],
                              result_mix[i][1],item[9],item[10],item[11],item[12],
                              arr_item_BI_provincecityname[i], item[14]]
                else:
                    item_i = [item[0], item[1], arr_item_BI_goodssortna[i], arr_item_BI_producttype2[i],
                              arr_item_BI_producttype3[i], result_mix[i][2], 0, 0,
                              result_mix[i][1], item[9], item[10], item[11], item[12],
                              arr_item_BI_provincecityname[i], item[14]]
                resArray.append(item_i)
        else:
            resArray.append(item)

    return resArray


def queryCurrentDayData_searchDoorway(currentDayQueryStr, nextDayQueryStr, key, data_mix):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询数据的sql语句
    sqlStr = '''select 
                    v.customername,
                    v.doorway,
                    v.BI_goodssortna,
                    v.producttype2,
                    v.producttype3,
                    v.productname_xx,
                    v.grossweight,
                    v.tareweight,
                    v.netweight,
                    v.goodsflagname,
                    v.vehicletypename,
                    v.vehicledesc,
                    v.grosstime,
                    v.provincecityname,
                    v.grossoperatorname,
                    v.ponderationoid
                from V_REPPONDER_PRODUCT_V2 v 
                where v.grosstime BETWEEN "TO_DATE"(''' + currentDayQueryStr + ''') and "TO_DATE"(''' + nextDayQueryStr + ''')
                and v.BI_goodssortna like '%蔬菜%' and v.doorway like '%''' + key + '''%' '''
    # 游标对象执行sql语句
    # print(sqlStr)
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        item = list(item)
        if item[9] == '混装':

            # 取出该混装对应的数据
            result_mix = []
            for mix in data_mix:
                if mix[0] == item[15]:
                    result_mix.append(mix)
            # print(result_mix)

            arr_item_BI_goodssortna = item[2].split(',')
            arr_item_BI_producttype2 = item[3].split(',')
            arr_item_BI_producttype3 = item[4].split(',')
            arr_item_BI_productname_xx = item[5].split(',')
            arr_item_BI_provincecityname = item[13].split(',')
            for i in range(0, len(result_mix)):
                if i == 0:
                    item_i = [item[0], item[1], arr_item_BI_goodssortna[i], arr_item_BI_producttype2[i],
                              arr_item_BI_producttype3[i], result_mix[i][2], item[6], item[7],
                              result_mix[i][1], item[9], item[10], item[11], item[12],
                              arr_item_BI_provincecityname[i], item[14]]
                else:
                    item_i = [item[0], item[1], arr_item_BI_goodssortna[i], arr_item_BI_producttype2[i],
                              arr_item_BI_producttype3[i], result_mix[i][2], 0, 0,
                              result_mix[i][1], item[9], item[10], item[11], item[12],
                              arr_item_BI_provincecityname[i], item[14]]
                resArray.append(item_i)
        else:
            resArray.append(item)

    return resArray


def queryCurrentDayData_searchVehicledesc(currentDayQueryStr, nextDayQueryStr, key, data_mix):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询数据的sql语句
    sqlStr = '''select 
                    v.customername,
                    v.doorway,
                    v.BI_goodssortna,
                    v.producttype2,
                    v.producttype3,
                    v.productname_xx,
                    v.grossweight,
                    v.tareweight,
                    v.netweight,
                    v.goodsflagname,
                    v.vehicletypename,
                    v.vehicledesc,
                    v.grosstime,
                    v.provincecityname,
                    v.grossoperatorname,
                    v.ponderationoid
                from V_REPPONDER_PRODUCT_V2 v 
                where v.grosstime BETWEEN "TO_DATE"(''' + currentDayQueryStr + ''') and "TO_DATE"(''' + nextDayQueryStr + ''')
                and v.BI_goodssortna like '%蔬菜%' and v.vehicledesc like '%''' + key + '''%' '''
    # 游标对象执行sql语句
    # print(sqlStr)
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        item = list(item)
        if item[9] == '混装':

            # 取出该混装对应的数据
            result_mix = []
            for mix in data_mix:
                if mix[0] == item[15]:
                    result_mix.append(mix)
            # print(result_mix)

            arr_item_BI_goodssortna = item[2].split(',')
            arr_item_BI_producttype2 = item[3].split(',')
            arr_item_BI_producttype3 = item[4].split(',')
            arr_item_BI_productname_xx = item[5].split(',')
            arr_item_BI_provincecityname = item[13].split(',')
            for i in range(0, len(result_mix)):
                if i == 0:
                    item_i = [item[0], item[1], arr_item_BI_goodssortna[i], arr_item_BI_producttype2[i],
                              arr_item_BI_producttype3[i], result_mix[i][2], item[6], item[7],
                              result_mix[i][1], item[9], item[10], item[11], item[12],
                              arr_item_BI_provincecityname[i], item[14]]
                else:
                    item_i = [item[0], item[1], arr_item_BI_goodssortna[i], arr_item_BI_producttype2[i],
                              arr_item_BI_producttype3[i], result_mix[i][2], 0, 0,
                              result_mix[i][1], item[9], item[10], item[11], item[12],
                              arr_item_BI_provincecityname[i], item[14]]
                resArray.append(item_i)
        else:
            resArray.append(item)

    return resArray


def queryCurrentDayData_searchProvincecityname(currentDayQueryStr, nextDayQueryStr, key, data_mix):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询数据的sql语句
    sqlStr = '''select 
                    v.customername,
                    v.doorway,
                    v.BI_goodssortna,
                    v.producttype2,
                    v.producttype3,
                    v.productname_xx,
                    v.grossweight,
                    v.tareweight,
                    v.netweight,
                    v.goodsflagname,
                    v.vehicletypename,
                    v.vehicledesc,
                    v.grosstime,
                    v.provincecityname,
                    v.grossoperatorname,
                    v.ponderationoid
                from V_REPPONDER_PRODUCT_V2 v 
                where v.grosstime BETWEEN "TO_DATE"(''' + currentDayQueryStr + ''') and "TO_DATE"(''' + nextDayQueryStr + ''')
                and v.BI_goodssortna like '%蔬菜%' and v.provincecityname like '%''' + key + '''%' '''
    # 游标对象执行sql语句
    # print(sqlStr)
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        item = list(item)
        if item[9] == '混装':

            # 取出该混装对应的数据
            result_mix = []
            for mix in data_mix:
                if mix[0] == item[15]:
                    result_mix.append(mix)
            # print(result_mix)

            arr_item_BI_goodssortna = item[2].split(',')
            arr_item_BI_producttype2 = item[3].split(',')
            arr_item_BI_producttype3 = item[4].split(',')
            arr_item_BI_productname_xx = item[5].split(',')
            arr_item_BI_provincecityname = item[13].split(',')
            for i in range(0, len(result_mix)):
                if i == 0:
                    item_i = [item[0], item[1], arr_item_BI_goodssortna[i], arr_item_BI_producttype2[i],
                              arr_item_BI_producttype3[i], result_mix[i][2], item[6], item[7],
                              result_mix[i][1], item[9], item[10], item[11], item[12],
                              arr_item_BI_provincecityname[i], item[14]]
                else:
                    item_i = [item[0], item[1], arr_item_BI_goodssortna[i], arr_item_BI_producttype2[i],
                              arr_item_BI_producttype3[i], result_mix[i][2], 0, 0,
                              result_mix[i][1], item[9], item[10], item[11], item[12],
                              arr_item_BI_provincecityname[i], item[14]]
                resArray.append(item_i)
        else:
            resArray.append(item)

    return resArray


def baobiao08_searchCustomername(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    key = request.GET.get('key')

    year = request.COOKIES['year']
    month = request.COOKIES['month']
    day = request.COOKIES['day']

    # 拼接查询的时间字符串
    currentDayQueryStr, nextDayQueryStr = queryTimeStr02(year, month, day)

    # 查询混装数据
    data_mix = queryData_mix(currentDayQueryStr, nextDayQueryStr)

    # 查询数据
    currentDayData = queryCurrentDayData_searchCustomername(currentDayQueryStr, nextDayQueryStr, key, data_mix)

    start = (page - 1) * limit
    count = len(currentDayData)
    if count < limit * page:
        end = count
    else:
        end = limit * page

    # 处理成符合格式的数据
    data = []
    for i in range(start, end):
        # for j in range(0, len(currentDayData[i])):
        map = {"customername": currentDayData[i][0],
               "doorway": currentDayData[i][1],
               "BI_goodssortna": currentDayData[i][2],
               "producttype2": currentDayData[i][3],
               "producttype3": currentDayData[i][4],
               "productname_xx": currentDayData[i][5],
               "grossweight": currentDayData[i][6],
               "tareweight": currentDayData[i][7],
               "netweight": currentDayData[i][8],
               "goodsflagname": currentDayData[i][9],
               "vehicletypename": currentDayData[i][10],
               "vehicledesc": currentDayData[i][11],
               "grosstime": currentDayData[i][12],
               "provincecityname": currentDayData[i][13],
               "grossoperatorname": currentDayData[i][14]
               }
        data.append(map)
    result = {"code": 0, "msg": "", "count": count, "data": data}
    return JsonResponse(result, safe=False)


def queryCurrentDayData_searchCustomername(currentDayQueryStr, nextDayQueryStr, key, data_mix):
    # 建立游标对象
    cursor = connection.cursor()
    # 拼接查询数据的sql语句
    sqlStr = '''select 
                    v.customername,
                    v.doorway,
                    v.BI_goodssortna,
                    v.producttype2,
                    v.producttype3,
                    v.productname_xx,
                    v.grossweight,
                    v.tareweight,
                    v.netweight,
                    v.goodsflagname,
                    v.vehicletypename,
                    v.vehicledesc,
                    v.grosstime,
                    v.provincecityname,
                    v.grossoperatorname,
                    v.ponderationoid
                from V_REPPONDER_PRODUCT_V2 v 
                where v.grosstime BETWEEN "TO_DATE"(''' + currentDayQueryStr + ''') and "TO_DATE"(''' + nextDayQueryStr + ''')
                and v.BI_goodssortna like '%蔬菜%' and v.customername like '%''' + key + '''%' '''
    # 游标对象执行sql语句
    # print(sqlStr)
    cursor.execute(sqlStr)
    # 取到游标对象里面的执行结果
    result = cursor.fetchall()
    resArray = []
    # 将结果转换为数组
    for item in result:
        # 将各项数据转换为数组再插入到结果集中
        item = list(item)
        if item[9] == '混装':

            # 取出该混装对应的数据
            result_mix = []
            for mix in data_mix:
                if mix[0] == item[15]:
                    result_mix.append(mix)
            # print(result_mix)

            arr_item_BI_goodssortna = item[2].split(',')
            arr_item_BI_producttype2 = item[3].split(',')
            arr_item_BI_producttype3 = item[4].split(',')
            arr_item_BI_productname_xx = item[5].split(',')
            arr_item_BI_provincecityname = item[13].split(',')
            for i in range(0, len(result_mix)):
                if i == 0:
                    item_i = [item[0], item[1], arr_item_BI_goodssortna[i], arr_item_BI_producttype2[i],
                              arr_item_BI_producttype3[i], result_mix[i][2], item[6], item[7],
                              result_mix[i][1], item[9], item[10], item[11], item[12],
                              arr_item_BI_provincecityname[i], item[14]]
                else:
                    item_i = [item[0], item[1], arr_item_BI_goodssortna[i], arr_item_BI_producttype2[i],
                              arr_item_BI_producttype3[i], result_mix[i][2], 0, 0,
                              result_mix[i][1], item[9], item[10], item[11], item[12],
                              arr_item_BI_provincecityname[i], item[14]]
                resArray.append(item_i)
        else:
            resArray.append(item)

    return resArray

