
# test codes & reload codes
#'''
import sqlite3
from database import *
from utils import *


id = 1
c = get_cursor()

cursor = c[1]
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("""CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
username TEXT NOT NULL,  
password TEXT NOT NULL, 
name TEXT NOT NULL,     
level INT NOT NULL,      
score INT NOT NULL, 
active INT NOT NULL,
admin INT NOT NULL, 
picpath TEXT NOT NULL, 
desc TEXT
);""")

cursor.execute("DROP TABLE IF EXISTS discuss;")
cursor.execute("""CREATE TABLE discuss (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
father INT,
title TEXT,
subject TEXT,   
date TEXT NOT NULL,   
pub INT NOT NULL,  
csee TEXT NOT NULL,
top INT NOT NULL,
temp INT NOT NULL, 
fname TEXT, 
desc TEXT
);""")

cursor.execute("DROP TABLE IF EXISTS resource;")
cursor.execute("""CREATE TABLE resource (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
father INT,
title TEXT,
subject TEXT,   
date TEXT NOT NULL,   
pub INT NOT NULL,  
csee TEXT NOT NULL,
top INT NOT NULL,
temp INT NOT NULL, 
fname TEXT, 
desc TEXT
);""")


cursor.execute("INSERT INTO users (username, password, name, level, score, active, admin, picpath) VALUES ('可爱的xiaoyin2011', 'xin780601', '尹怀杰', 50, 2000, 89, 1, '1.png')")
cursor.execute("INSERT INTO users (username, password, name, level, score, active, admin, picpath) VALUES ('可爱的dyc1919', '123456', '董雨宸', 50, 2000, 89, 1, '1.png')")
cursor.execute("INSERT INTO discuss (id, title, date, pub, csee, top, temp) VALUES (1, '关于管理', '2022-9-25 18:31:24', 1, '1,2,0', 1, 0)")

c[0].commit()
c[0].close()


#'''




from database import *
d = Discuss(1)




from flask import *
import flask
from database import *
import string, random
from datetime import *
import os
from utils import *
def randstr(charset = list(string.ascii_lowercase + string.ascii_uppercase + string.digits), k = 24):
    return ''.join(random.choices(charset, k = 24))
app = Flask(__name__)
app.config['SECRET_KEY'] = "74CNYMBDServerExSEPassword"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days = 7)
# session.permanent = True

#session = {'login' : True, 'id' : 1}
id = 1

'''
session = {}
id : int
login : True / False
admin : True / False
username : 'xiaoyin2011'


'''








@app.route('/')
def index():
    f = open("./data/tops_info.txt", 'r', encoding = "utf-8")
    word1, link1, word2, link2, word3, link3 = f.readlines()
    f.close()
    return render_template("index.html", session = session, cex_words_1 = word1, cex_words_2 = word2, cex_words_3 = word3, cex_link_1 = link1, cex_link_2 = link2, cex_link_3 = link3)

@app.route('/login/')
def login():
    err = session.get('err')
    session['err'] = []
    if err == None:
        err = []
    return render_template("login.html", errors = err)

@app.route('/login/handle/', methods = ['POST'])
def login_handle():
    username = flask.request.values.get('username')
    password = flask.request.values.get('password')
    error1 = False
    error2 = False
    c = get_cursor()
    c[1].execute(f"SELECT password FROM users WHERE username = '{username}'")
    data = c[1].fetchone()
    if data == None:
        error1 = True
    else:
        error2 = password != data[0]
    if not error1 and not error2:
        c[1].execute(f"SELECT * FROM users WHERE username = '{username}'")
        data = c[1].fetchone()
        #print(data)
        session['id'] = data[0]
        session['login'] = True
        session['username'] = data[1]
        session['admin'] = data[7]
        session['datas'] = data
        c[0].commit()
        c[0].close()
        session.permanent = True
        return redirect("/")
    else:
        session['err'] = []
        if error1:
            session['err'].append("用户不存在")
        elif error2:
            session['err'].append("用户名或密码错误")
        c[0].commit()
        c[0].close()
        return redirect("/login/")

@app.route('/users/')
def user():
    dis = []
    lsc = "Level " + str(session.get('datas')[4]) + " 积分" + str(session.get('datas')[5]) + " 活跃度" + str(session.get('datas')[6])
    return render_template("users_me.html", session = session, tname = session.get('datas')[3], lvlsc = lsc, hedis = dis)

@app.route('/users/<int:id>/')
def users(id):
    dis = []
    dis_id = discuss_f(-1 if not session.get('login') else session.get('id'), id)
    for did in dis_id:
        dis.append(Discuss(did))
    c = get_cursor()
    c[1].execute(f"SELECT * FROM users WHERE id = '{id}'")
    data = c[1].fetchone()
    lsc = "Level " + str(data[4]) + " 积分" + str(data[5]) + " 活跃度" + str(data[6])
    c[0].commit()
    c[0].close()
    picpath = "./../user/user_pic/{{ id }}."
    return render_template("users.html", login = session.get('login'), username = data[1], admin = data[7], tname = data[3], lvlsc = lsc, hedis = dis)

@app.route('/discuss/list/')
def discuss():
    Ds = discuss_all_t()
    print(Ds)
    return render_template("discuss.html", session = session, discuss = Ds)

@app.route('/discuss/<int:id>/')
def dicuss_detail(id):
    try:
        d = Discuss(id)
    except:
        return "Discuss Not Found", 404
    if d.temp:
        return redirect(f'/discuss/{id}/tmp')
    if d.father == 0:
        fid = 0
        fname = ""
    else:
        dtmp = Discuss(d.father)
        fid = dtmp.id
        fname = dtmp.title
    '''
    fid = d.father
    if fid == None:
        fid = 0
        fname = ''
    else:
        fname = Discuss(fid).title
    ptime = d.date
    subject = d.subject
    if subject:
        subject = '无'
    cse = d.csee
    csc = d.csee_cnt
    toped = d.top
    pubid = d.pub_id
    c = get_cursor()
    c[1].execute(f"SELECT * FROM users WHERE id = '{pubid}'")
    dat = c[1].fetchone()
    pubname = dat[1]
    pubpic = dat[8]
    c[0].commit()
    c[0].close()
    title = d.title
    con = render(d.all_data)
    '''
    return render_template("discuss_detail.html", session = session, 
    title = d.title, 
    pub_id = d.pub_id, 
    pub_name = d.pub_name, 
    pub_pic = d.pub_pic, 
    father_id = d.father, 
    father_name = fid, 
    pub_time = fname, 
    subjects = d.subject, 
    csee = d.csee, 
    csee_cnt = d.csee_cnt, 
    toped = d.top, 
    content = render(d.all_data)
    )
    
@app.route('/discuss/<int:id>/csee/')
def discuss_detail_csee(id):
    try:
        d = Discuss(id)
    except:
        return "Discuss Not Found", 404
    if d.temp:
        return redirect(f'/discuss/{id}/tmp/csee')
    cse = d.csee
    if cse == 'all':
        cse = all_users()
    cse = cse.split(',')
    csee = []
    c = get_cursor()
    for cs in cse:
        if cs == 0:
            ls = [0, '游客', '0.PNG']
        else:
            c[1].execute(f"SELECT * FROM users WHERE id = '{cs}'")
            dat = c[1].fetchone()
            if dat != None:
                ls = [cs, dat[1], dat[8]]
                csee.append(ls)
    c[0].commit()
    c[0].close()
    return render_template("discuss_detail_csee.html", session = session, csee = csee)

@app.route('/discuss/<int:id>/tmp/')
def discuss_detail_tmp(id):
    try:
        d = Discuss(id)
    except:
        return "Discuss Not Found", 404
    if not d.temp:
        return redirect(f'/discuss/{id}')
    if d.father == 0:
        fid = 0
        fname = ""
    else:
        dtmp = Discuss(d.father)
        fid = dtmp.id
        fname = dtmp.title
    '''
    fid = d.father
    if fid == None:
        fid = 0
        fname = ''
    else:
        fname = Discuss(fid).title
    ptime = d.date
    subject = d.subject
    if subject:
        subject = '无'
    cse = d.csee
    csc = d.csee_cnt
    toped = d.top
    pubid = d.pub_id
    c = get_cursor()
    c[1].execute(f"SELECT * FROM users WHERE id = '{pubid}'")
    dat = c[1].fetchone()
    pubname = dat[1]
    pubpic = dat[8]
    c[0].commit()
    c[0].close()
    title = d.title
    con = render(d.all_data)
    '''
    return render_template("discuss_detail.html", session = session, 
    title = d.title, 
    pub_id = d.pub_id, 
    pub_name = d.pub_name, 
    pub_pic = d.pub_pic, 
    father_id = d.father, 
    father_name = fid, 
    pub_time = fname, 
    subjects = d.subject, 
    csee = d.csee, 
    csee_cnt = d.csee_cnt, 
    toped = d.top, 
    content = render(d.all_data)
    )

@app.route('/discuss/<int:id>/tmp/csee/')
def discuss_detail_tmp_csee(id):
    try:
        d = Discuss(id)
    except:
        return "Discuss Not Found", 404
    if not d.tmp:
        return redirect(f'/discuss/{id}/csee')
    cse = d.csee
    if cse == 'all':
        cse = all_users()
    cse = cse.split(',')
    csee = []
    c = get_cursor()
    for cs in cse:
        if cs == 0:
            ls = [0, '游客', '0.PNG']
        else:
            c[1].execute(f"SELECT * FROM users WHERE id = '{cs}'")
            dat = c[1].fetchone()
            if dat != None:
                ls = [cs, dat[1], dat[8]]
                csee.append(ls)
    c[0].commit()
    c[0].close()
    return render_template("discuss_detail_tmp_csee.html", session = session, csee = csee)

@app.route('/discuss/new/')
def discuss_new():
    fid = request.args.get('fid')
    return render_template("discuss_new.html", session = session, fid = fid)

@app.route('/discuss/new_notitle/')
def discuss_new_notitle():
    fid = request.args.get('fid')
    return render_template("discuss_new_notitle.html", session = session, fid = fid)

@app.route('/discuss/new_file/')
def discuss_new_file():
    fid = request.args.get('fid')
    return render_template("discuss_new_file.html", session = session, fid = fid)

@app.route('/discuss/new/handle/save/', methods = ['POST'])
def discuss_new_handle1():
    data = flask.request.get_json()
    title = data.get('title')
    father = data.get('father')
    subject = data.get('subject')
    pub = session['id']
    csee = data.get('csee')
    content = data.get('text')
    c = get_cursor()
    if csee == '':
        csee = 'all'
    if father != '':
        father = int(father)
        print(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES ({father}, {title}, {subject}, {get_time()}, {pub}, {csee}, 0, 1)")
        c[1].execute(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES ({father}, '{title}', '{subject}', '{get_time()}', {pub}, '{csee}', 0, 1)")
    else:
        print(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES ({-1}, {title}, {subject}, {get_time()}, {pub}, {csee}, 0, 1)")
        c[1].execute(f"INSERT INTO discuss (title, subject, date, pub, csee, top, temp) VALUES ('{title}', '{subject}', '{get_time()}', {pub}, '{csee}', 0, 1)")
    nowid = c[1].lastrowid
    c[0].commit()
    c[0].close()
    f = open(f"./discuss/{nowid}.txt", 'w', encoding = 'utf-8')
    print(f"Write to ./discuss/{nowid}.txt : {content}")
    f.write(content)
    f.close()
    return f"/discuss/edit/{nowid}/"

@app.route('/discuss/new/handle/render/', methods = ['POST'])
def discuss_new_handle2():
    data = flask.request.get_json()
    title = data.get('title')
    father = data.get('father')
    subject = data.get('subject')
    pub = session['id']
    csee = data.get('csee')
    content = data.get('text')
    c = get_cursor()
    if csee == '':
        csee = 'all'
    if father != '':
        father = int(father)
        print(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES ({father}, {title}, {subject}, {get_time()}, {pub}, {csee}, 0, 1)")
        c[1].execute(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES ({father}, '{title}', '{subject}', '{get_time()}', {pub}, '{csee}', 0, 1)")
    else:
        print(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES ({-1}, {title}, {subject}, {get_time()}, {pub}, {csee}, 0, 1)")
        c[1].execute(f"INSERT INTO discuss (title, subject, date, pub, csee, top, temp) VALUES ('{title}', '{subject}', '{get_time()}', {pub}, '{csee}', 0, 1)")
    nowid = c[1].lastrowid
    c[0].commit()
    c[0].close()
    f = open(f"./discuss/{nowid}.txt", 'w', encoding = 'utf-8')
    f.write(content)
    f.close()
    return f"/discuss/{nowid}/tmp"

@app.route('/discuss/new/handle/publish/', methods = ['POST'])
def discuss_new_handle3():
    data = flask.request.get_json()
    title = data.get('title')
    father = data.get('father')
    subject = data.get('subject')
    pub = session['id']
    csee = data.get('csee')
    content = data.get('text')
    c = get_cursor()
    if csee == '':
        csee = 'all'
    if father != '':
        father = int(father)
        print(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES ({father}, {title}, {subject}, {get_time()}, {pub}, {csee}, 0, 1)")
        c[1].execute(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES ({father}, '{title}', '{subject}', '{get_time()}', {pub}, '{csee}', 0, 1)")
    else:
        print(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES ({-1}, {title}, {subject}, {get_time()}, {pub}, {csee}, 0, 1)")
        c[1].execute(f"INSERT INTO discuss (title, subject, date, pub, csee, top, temp) VALUES ('{title}', '{subject}', '{get_time()}', {pub}, '{csee}', 0, 1)")
    nowid = c[1].lastrowid
    c[0].commit()
    c[0].close()
    f = open(f"./discuss/{nowid}.txt", 'w', encoding = 'utf-8')
    f.write(content)
    f.close()
    f = open("./templist.txt", 'a', encoding = 'utf-8')
    f.write(id)
    f.close()
    return f"/discuss/{nowid}/tmp"

@app.route('/discuss/edit/<int:id>/')
def discuss_edit(id):
    try:
        d = Discuss(id)
    except:
        return "Discuss Not Found", 404
    fid = d.father
    if fid == None or fid == 0:
        fid = 0
        fname = ""
    else:
        fname = Discuss(fid).title
    subject = d.subject
    if not subject:
        subject = '无'
    return render_template("discuss_edit.html", session = session, 
    title = d.title, 
    fid = fid, 
    subject = subject, 
    csee = d.csee, 
    content = d.all_data
    )

@app.route('/discuss/edit/<int:id>/handle/save/', methods = ['POST'])
def discuss_edit_handle1(id):
    data = flask.request.get_json()
    title = data.get('title')
    father = data.get('father')
    subject = data.get('subject')
    pub = session['id']
    csee = data.get('csee')
    content = data.get('text')
    c = get_cursor()
    if csee == '':
        csee = 'all'
    print(f"UPDATE discuss SET title = '{title}', subject = '{subject}', date = '{get_time()}', pub = {pub}, csee = '{csee}', top = 0, temp = 1 WHERE id = {id}")
    c[1].execute(f"UPDATE discuss SET title = '{title}', subject = '{subject}', date = '{get_time()}', pub = {pub}, csee = '{csee}', top = 0, temp = 1 WHERE id = {id}")
    c[0].commit()
    c[0].close()
    f = open(f"./discuss/{id}.txt", 'w', encoding = 'utf-8')
    print(f"Write to ./discuss/{id}.txt : {content}")
    f.write(content)
    f.close()
    return f"/discuss/edit/{id}"

@app.route('/discuss/edit/<int:id>/handle/render/', methods = ['POST'])
def discuss_edit_handle2(id):
    data = flask.request.get_json()
    title = data.get('title')
    father = data.get('father')
    subject = data.get('subject')
    pub = session['id']
    csee = data.get('csee')
    content = data.get('text')
    c = get_cursor()
    if csee == '':
        csee = 'all'
    print(f"UPDATE discuss SET title = '{title}', subject = '{subject}', date = '{get_time()}', pub = {pub}, csee = '{csee}', top = 0, temp = 1 WHERE id = {id}")
    c[1].execute(f"UPDATE discuss SET title = '{title}', subject = '{subject}', date = '{get_time()}', pub = {pub}, csee = '{csee}', top = 0, temp = 1 WHERE id = {id}")
    c[0].commit()
    c[0].close()
    f = open(f"./discuss/{id}.txt", 'w', encoding = 'utf-8')
    f.write(content)
    f.close()
    return f"/discuss/{id}/tmp"

@app.route('/discuss/edit/<int:id>/handle/publish/', methods = ['POST'])
def discuss_edit_handle3(id):
    data = flask.request.get_json()
    title = data.get('title')
    father = data.get('father')
    subject = data.get('subject')
    pub = session['id']
    csee = data.get('csee')
    content = data.get('text')
    c = get_cursor()
    if csee == '':
        csee = 'all'
    print(f"UPDATE discuss SET title = '{title}', subject = '{subject}', date = '{get_time()}', pub = {pub}, csee = '{csee}', top = 0, temp = 1 WHERE id = {id}")
    c[1].execute(f"UPDATE discuss SET title = '{title}', subject = '{subject}', date = '{get_time()}', pub = {pub}, csee = '{csee}', top = 0, temp = 1 WHERE id = {id}")
    c[0].commit()
    c[0].close()
    f = open(f"./discuss/{id}.txt", 'w', encoding = 'utf-8')
    f.write(content)
    f.close()
    f = open("./templist.txt", 'a', encoding = 'utf-8')
    f.write(id)
    f.close()
    return f"/discuss/{id}/tmp"

@app.route('/discuss/pic_upload/')
def pic_upload():
    return render_template("discuss_pic_upload.html", session = session)

@app.route('/discuss/pic_handle/', methods = ['POST'])
def pic_handle():
    if 'file' not in request.files:
        return '上传失败'
 
    file = request.files['file']
    if file.filename == '':
        return '上传失败'
 
    if file:
        f = open("./static/discuss_files/file_cnt.txt", 'r')
        dat = int(f.read()) + 1
        f.close()
        f = open("./static/discuss_files/file_cnt.txt", 'w')
        f.write(str(dat))
        f.close()
        filepath = str(dat) + os.path.splitext(file.filename)[1]
        file.save(os.path.join('./static/discuss_files/', filepath))
        return render_template("discuss_pic_upload.html", session = session, postad = filepath)

@app.route('/search/')
def search():
    rsearch = request.form.get('resource_search', '')
    gettypes = request.form.get('cb', '2,3')
    sortways = request.form.get('sw', 'a')
    print("Log To Console : ", rsearch, gettypes, sortways)
    return render_template("search.html", session = session, rsearch = rsearch, cw = gettypes, sw = sortways)
    # prs = rsearch, sc = gettypes, ff = sortways















# 暂且先如此处理
@app.route('/information/')
def information():
    return render_template("information.html", session = session)

'''
@app.route('/information/<string:path>/')
def information(path):
    f = open("./info/filename.txt")
    kk = f.readlines()
    f.close()
    ls = []
    for k in kk:
        ls.append(k.split(' '))
    f = open(f"./info/{path.replace('-', '/')}.txt")
    cc = f.readlines()
    f.close()
    try:
        title = cc[0]
    except:
        title = "无标题班规"
    cc = '<br>'.join(cc)
    return render_template("information_shell.html", session = session, ls = ls, title = title, content = cc)
@app.route('/docs/<string:path>/')
def information_docs(path):
    f = open("./info/filename.txt")
    kk = f.readlines()
    f.close()
    ls = []
    for k in kk:
        ls.append(k.split(' '))
    f = open(f"./info/docs/{path.replace('-', '/')}.txt")
    cc = f.readlines()
    f.close()
    try:
        title = cc[0]
    except:
        title = "无标题"
    cc = '<br>'.join(cc[1:])
    return render_template("information_shell.html", session = session, ls = ls, title = title, content = cc)
'''

@app.errorhandler(404)
def error404(error):
    return render_template("404.html", session = session), 404

@app.errorhandler(500)
def error500(error):
    return render_template("500.html", session = session), 500

if __name__ == "__main__":
    app.run(port = 5000)