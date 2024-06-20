import sqlite3, sys

name = input(" >>>")
if name == "AUTO":
    f = open("./database_name.txt", 'r')
    name = f.read()
    f.close()

conn = sqlite3.connect("./" + name + ".db")
cursor = conn.cursor()

print("\033[33mSQL\033[0m \033[31mCOMMANDER\033[0m 1.1")

while True:
    cmd = ""
    while True:
        c = input(" >>>")
        cmd += c
        if not c.endswith(';'):
            cmd += '\n'
        else:
            break
    if cmd == "QUIT;":
        conn.commit()
        conn.close()
        break
    try:
        cursor.execute(cmd)
        
        raise TypeError("BUGED")
        
    except sqlite3.OperationalError:
        print("\033[31m[ERROR]\033[0m SQL错误：语句错误")
        print(f"\033[32m{cmd}\033[0m")
    except Exception as err:
        print("\033[31m[FATAL]\033[0m 未知错误")
        print("是否输出调试信息？(y/n)")
        r = input(" >>>")
        if r == 'y':
            print("ERR DATA: ")
            print("{0}".format(err))
            print("SYS EXC_INFO DATA: ")
            print(sys.exc_info()[0])
            print("-------------------")
            raise err;
        break
    print(cursor.fetchall())