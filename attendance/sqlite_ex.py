import sqlite3
import pandas as pd
import commonutil

# db 열기
def dbOpen():
    # DB 연결
    global conn;
    conn = sqlite3.connect(commonutil.getRootPath() +"/db/attendance.db")
     # 커서 가져오기
    global cur;
    cur = conn.cursor()

# db 닫기
def dbClose():
    conn.close()

# 테이블 생성
def createTable():
    print('[Start] create table')
    query = 'create table if not exists attendance ('
    query = query + 'id integer primary key autoincrement,'
    query = query + 'name text,'
    query = query + 'create_dt text,'
    query = query + 'update_dt text'
    query = query + ')'
    print('\tQuery : '+query)
    conn.execute(query)
    print('[End] create table')

# 테이블 드랍(삭제)
def dropTable():
    # 테이블이 있을 경우, 드랍
    print('[Start] drop table')
    
    try:
        query = 'drop table attendance'
        print('\tQuery : '+ query)
        conn.execute(query)
    except sqlite3.OperationalError as e:
        print("Already exist table. Cause :")
        print(e)

    print('[End] drop table')

# 출석 데이터 추가
def insertAttendance(name):
    print('[Start] insert table')
    query = "INSERT INTO attendance (name, create_dt)VALUES ('"+ name +"', '"+ commonutil.getNowDate() +"')"
    print('\tQuery : '+ query)
    cur.execute("INSERT INTO attendance (name, create_dt)VALUES ('"+ name +"', '"+ commonutil.getNowDate() +"')")
    
    '''
    # 한번에 여러개의 행을 입력하고 싶을때...
    cur.executemany(
        'INSERT INTO attendance VALUES (?, ?, ?)',
        [
            (1, 'kjh', '2022-10-12 00:00:00.000'), 
            (2, 'jhj', '2022-10-12 00:00:00.000')
        ]
    )
    '''
    # db 저장
    conn.commit()
    print('[End] insert table')

# 출석 데이터 수정(쓸일이 있을려나)
def updateAttendance(id, name):
    print('[Start] update table')
    query = "update attendance set name='"+ name +"', update_dt='"+ commonutil.getNowDate() +"' where id="+ str(id)
    print('\tQuery : '+ query)
    cur.execute(query)
    # db 저장
    conn.commit
    print('[End] update table')
    
# 모든 출석 데이터 들고 오기
def selectAll():
    query = "SELECT * FROM attendance"
    cur.execute("SELECT * FROM attendance")
    print('\tQuery : '+ query)
    rows = cur.fetchall()

    cols = [column[0] for column in cur.description]
    data_df = pd.DataFrame.from_records(data=rows, columns=cols)
    print('#########################################')
    print(data_df)
    print('#########################################')
    '''
    for row in rows:
        print(row)
    '''

# test
def execute():
    dbOpen()
    dropTable()
    createTable()
    insertAttendance("kjh")
    updateAttendance(1, "hgd")
    selectAll()
    dbClose()

execute()