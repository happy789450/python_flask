import pymysql


def getConnect():
    try:
        connect = pymysql.connect(host='10.4.45.30', user='rice', password='123456', database='devops', port=3306)
        return connect
    except Exception as e:
        print(e)


def selectByParameters(sql, params=None):
    try:
        connect = getConnect()
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, params)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
    finally:
        try:
            cursor.close()
        except Exception as e:
            print(e)
        try:
            connect.close()
        except Exception as e:
            print(e)


def updateByParameters(sql, params=None):
    try:
        connect = getConnect()
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        count = cursor.execute(sql, params)
        connect.commit()
        return count
    except Exception as e:
        connect.rollback()
        print(e)
    finally:
        try:
            cursor.close()
        except Exception as e:
            print(e)
        try:
            connect.close()
        except Exception as e:
            print(e)


# 测试查询封装，带查询查询封装
if __name__ == "__main__":
    sql = 'select * from servers'
    result = selectByParameters(sql)
    print(result)

# if __name__ == "__main__":
#     sql = 'select * from servers where name = %s'
#     params = ("nginx", )
#     result = selectByParameters(sql, params=params)
#     print( result )

# 测试更新封装，带参数的更新封装
# if __name__ == "__main__":
#     sql = "insert into servers (name, ip, port, user) values( 'nginx', '127.0.0.1', 22, 'root' );"
#     result = updateByParameters(sql)
#     print( result )
#
# if __name__ == "__main__":
#     sql = "delete from servers where id = %s"
#     result = updateByParameters(sql, params=( 3, ))
#     print( result )
