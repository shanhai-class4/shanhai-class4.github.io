
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
cursor.execute("INSERT INTO users (username, password, name, level, score, active, admin, picpath) VALUES ('可爱的dyc1919', '123456', '董雨宸', 50, 2000, 89, 1, '2.png')")
cursor.execute("INSERT INTO users (username, password, name, level, score, active, admin, picpath) VALUES ('贠涵', '123456', '贠涵', 50, 2000, 89, 1, '2.png')")
cursor.execute("INSERT INTO users (username, password, name, level, score, active, admin, picpath) VALUES ('我不知道', '123456', '测试用户【非admin】', 50, 2000, 89, 0, '2.png')")
cursor.execute("INSERT INTO discuss (id, title, date, pub, csee, top, temp) VALUES (1, '班级圈网站规定', '2024-6-1 17:00:00', 1, '1,2,0', 1, 0)")
c[0].commit()
c[0].close()


#'''




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
app.config['SECRET_KEY'] = "74CNYMBDServerExSEPassword-1.1.3.8.11.4-Hotfix5-ORWT-Debug1"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days = 7)
# session.permanent = True

id = 1

'''
session = {}
id : int
login : True / False
admin : True / False
username : 'xiaoyin2011'


'''





@app.before_request
def default_session():
    if 'id' not in session:
        session['id'] = 0
    if 'login' not in session:
        session['login'] = False
    if 'admin' not in session:
        session['admin'] = False

@app.route('/')
def index():
    f = open("./data/tops_info.txt", 'r', encoding = "utf-8")
    word1, link1, word2, link2, word3, link3 = f.readlines()
    f.close()
    f = open("./homework.txt", 'r', encoding = "utf-8")
    hwid, hwpid = f.readlines()
    f.close()
    f = open("./redt.txt", 'r', encoding = "utf-8")
    raw_grs = f.readlines()
    f.close()
    cooked_grs = []
    for rg in raw_grs:
        cooked_grs.append(rg.split(' '))
    d = all_discuss(0, None, session['id'])
    d = sorted(d, key = lambda s : s[4])
    showd = []
    for i in range(min(len(d), 5)):
        showd.append(Discuss(d[i][0]))
    return render_template("index.html", session = session, cex_words_1 = word1, cex_words_2 = word2, cex_words_3 = word3, cex_link_1 = link1, cex_link_2 = link2, cex_link_3 = link3, hwid = hwid, hwpid = hwpid, grs = cooked_grs, dis = showd)

@app.route('/lookforsession/')
def lsessioner():
    print(session)
    return session

@app.route('/lookforuser/')
def luser():
    u = User(session['id'])
    print(u.info, u.desc)
    return session

@app.route('/login/')
def login():
    if session['login']:
        return redirect('/')
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
        data = c[1].fetchall()[0]
        session['id'] = data[0]
        session['login'] = True
        session['username'] = data[1]
        session['admin'] = data[7]
        session['datas'] = data
        session.permanent = True
        c[0].commit()
        c[0].close()
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

@app.route('/login/logout/')
def logout():
    if not session['login']:
        return redirect('/login/')
    session['id'] = 0
    session['login'] = False
    session['username'] = None
    session['admin'] = False
    session['datas'] = None
    return redirect("/login/")

@app.route('/login/forgetpwd/')
def forgetpwd():
    if session['login']:
        return redirect('/')
    return render_template("login_fpwd.html", session = session)


@app.route("/login/forgetpwd/handle/", methods=['POST'])
def forgetpwd_handle():
    userid = request.form.get("id")
    rname = request.form.get("rname")
    eduid = request.form.get("eduid")
    pwd = request.form.get("pwd")
    session['tmp-id'] = userid
    session['tmp-rname'] = rname
    session['tmp-eduid'] = eduid
    session['tmp-pwd'] = pwd
    return render_template("sucess.html", session = session)

'''
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
'''
'''
@app.route('/discuss/list/')
def discuss():
    Ds = discuss_all_t()
    print(Ds)
    return render_template("discuss.html", session = session, discuss = Ds)
'''
@app.route('/discuss/<int:id>/')
def dicuss_detail(id):
    #try:
    d = Discuss(id)
    #except:
    #    return "Discuss Not Found", 404
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
    #try:
    d = Discuss(id)
    #except:
    #    return "Discuss Not Found", 404
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
    if not session['login']:
        return redirect('/login/')
    #try:
    d = Discuss(id)
    #except:
    #    return "Discuss Not Found", 404
    if not d.temp:
        return redirect(f'/discuss/{id}')
    seer = User(session['id'])
    if not seer.admin and seer.id != d.pub_id:
        return '你没有查看该临时帖子的权限'
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
    return render_template("discuss_detail_tmp.html", session = session, 
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
    content = d.all_data
    )

@app.route('/discuss/<int:id>/tmp/handle/accept/')
def discuss_detail_tmp_handle1(id):
    if not session['login']:
        return redirect('/login/')
    #try:
    d = Discuss(id)
    #except:
    #    return "Discuss Not Found", 404
    if not d.temp:
        return "Discuss Not Found", 404
    seer = User(session['id'])
    if not seer.admin:
        return '你没有查看该临时帖子的权限'
    d.temp = 0
    d.save(None)
    return """
    <!--  -->
<!DOCTYPE html>
<html lang = "zh">
	<head>
		<meta charset = "UTF-8">
		<meta name = "viewport" content = "width=device-width, initial-scale=1.0">
		
		<title>班级圈计划 - ClassNet</title>
		
<!--<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">-->
<link rel="stylesheet" href="../../../../../static/bootstrap-4.6.2/css/bootstrap.min.css">
		
		<link rel="stylesheet" href="../../../../../static/css/std.css">
		<style>
			
		</style>
		
	</head>

	<body>
	<!-- 顶部信息 -->
		<header>
			<a href="/" id = "head_logo_text">
				<div>
					<img src="../../../../../static/img/logo.png" alt="logo" id = "logo_img" />
				</div>
				<div>
					<div id = "logo_text_h">
						&nbsp; 人大附通·北京学校 2023级四班 班级圈
					</div>
					<div id = "logo_text_l">
						&nbsp;&nbsp; Grade 2023 Class 4 - Class Net
					</div>
				</div>
			</a>
			<div id = "header_buttons">
				<a href="/discuss/new/" target="_blank">
					<img src="../../../../../static/img/new_ico.png" alt="新建" class = "header_button_img" />
				</a>
				<a href="/discuss/list/" target="_blank">
					<img src="../../../../../static/img/search_ico.png" alt="搜索" class = "header_button_img" />
				</a>
				<a href="/user/me/" target="_blank">
					<img src="../../../../../static/img/person_ico.png" alt="个人" class = "header_button_img" />
				</a>
				<a href="/setting/" target="_blank">
					<img src="../../../../../static/img/setting_ico.png" alt="设置" class = "header_button_img" />
				</a>
			</div>
		</header>
		<nav id = "navbar" class = "nav nav-pills nav-justified">
			<div class = "nav-link">
				<a class = "nav_link" href="/information/" target="_blank">
					<div class = "nav_text">班级信息</div>
				</a>
			</div>
			<div class = "nav-link">
				<a class = "nav_link" href="/resource/" target="_blank">
					<div class = "nav_text">班级资源</div>
				</a>
			</div>
			<div class = "nav-link">
				<a class = "nav_link" href="/forum/" target="_blank">
					<div class = "nav_text">班级论坛</div>
				</a>
			</div>
			<div class = "nav-link">
				<a class = "nav_link" href="/activity/" target="_blank">
					<div class = "nav_text">班级活动</div>
				</a>
			</div>
			<div class = "nav-link">
				<a class = "nav_link" href="/album/" target="_blank">
					<div class = "nav_text">班级相册</div>
				</a>
			</div>
			<div class = "nav-link">
				<a class = "nav_link" href="/about/" target="_blank">
					<div class = "nav_text">帮助中心</div>
				</a>
			</div>
		</nav>
		<section>
            <div class="main-content">
            <h2>通过成功！帖子访问链接：
            """f"/discuss/{id}/""""</h2></div>
		</section>
		<footer>
			<div>
				<p class="footer_data"><b>©人大附通·北京学校 初一4班 班级网站</b></p>
				<p class="footer_data"><b>制作团队：</b>4班班级圈网站开发组</p>
				<p class="footer_data"><b>网站主要设计者：</b>贠涵，闫嘉桐，王岩杉，袁立之，董雨宸，尹怀杰</p>
				<p class="footer_data"><b>内容责任编辑：</b>贠涵，闫嘉桐</p>
				<p class="footer_data"><a href = "#">查看更多</a></p>
			</div>
		</footer>
		

<!-- Bookstrap -->
<script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="../../../../../static/bootstrap-4.6.2/js/bootstrap.min.js"></script>

		<script src = "../../../../../static/js/refresh_color.js"></script>
		<script src = "../../../../../static/js/checker.js"></script>
	</body>
</html>
    """

@app.route('/discuss/<int:id>/tmp/handle/reject/')
def discuss_detail_tmp_handle2(id):
    if not session['login']:
        return redirect('/login/')
    #try:
    d = Discuss(id)
    #except:
    #    return "Discuss Not Found", 404
    if not d.temp:
        return "Discuss Not Found", 404
    seer = User(session['id'])
    if not seer.admin:
        return '你没有查看该临时帖子的权限'
    d.temp = 1
    d.save(None)
    return f"/discuss/{id}/tmp/"

@app.route('/discuss/<int:id>/tmp/handle/delete/')
def discuss_detail_tmp_handle3(id):
    if not session['login']:
        return redirect('/login/')
    #try:
    d = Discuss(id)
    #except:
    #    return "Discuss Not Found", 404
    if not d.temp:
        return "Discuss Not Found", 404
    seer = User(session['id'])
    if not seer.admin:
        return '你没有查看该临时帖子的权限'
    c = get_cursor()
    c[1].execute(f"DELETE FROM discuss WHERE id = {id};")
    c[0].commit()
    c[0].close()
    return "/discuss/list/"

@app.route('/discuss/<int:id>/tmp/csee/')
def discuss_detail_tmp_csee(id):
    if not session['login']:
        return redirect('/login/')
    #try:
    d = Discuss(id)
    #except:
    #    return "Discuss Not Found", 404
    if not d.tmp:
        return redirect(f'/discuss/{id}/csee')
    seer = User(session['id'])
    if not seer.admin and seer.id != d.pub_id:
        return '你没有查看该临时帖子的权限'
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
    if not session['login'] or session['id'] == 0:
        return redirect('/login/')
    fid = request.args.get('fid')
    return render_template("discuss_new.html", session = session, fid = fid)

@app.route('/discuss/new_notitle/')
def discuss_new_notitle():
    if not session['login'] or session['id'] == 0:
        return redirect('/login/')
    fid = request.args.get('fid')
    return render_template("discuss_new_notitle.html", session = session, fid = fid)

@app.route('/discuss/new_file/')
def discuss_new_file():
    if not session['login']:
        return redirect('/login/')
    fid = request.args.get('fid')
    return render_template("discuss_new_file.html", session = session, fid = fid)

@app.route('/discuss/new/handle/save/', methods = ['POST'])
def discuss_new_handle1():
    if not session['login']:
        return redirect('/login/')
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
        c[1].execute(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES (0, '{title}', '{subject}', '{get_time()}', {pub}, '{csee}', 0, 1)")
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
    if not session['login']:
        return redirect('/login/')
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
        c[1].execute(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES (0, '{title}', '{subject}', '{get_time()}', {pub}, '{csee}', 0, 1)")
    nowid = c[1].lastrowid
    c[0].commit()
    c[0].close()
    f = open(f"./discuss/{nowid}.txt", 'w', encoding = 'utf-8')
    f.write(content)
    f.close()
    return f"/discuss/{nowid}/tmp/"

@app.route('/discuss/new/handle/publish/', methods = ['POST'])
def discuss_new_handle3():
    if not session['login']:
        return redirect('/login/')
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
        c[1].execute(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp) VALUES (0, '{title}', '{subject}', '{get_time()}', {pub}, '{csee}', 0, 1)")
    nowid = c[1].lastrowid
    c[0].commit()
    c[0].close()
    f = open(f"./discuss/{nowid}.txt", 'w', encoding = 'utf-8')
    f.write(content)
    f.close()
    f = open("./templist.txt", 'a', encoding = 'utf-8')
    f.write(',' + str(nowid))
    f.close()
    return f"/discuss/{nowid}/tmp/"

@app.route('/discuss/edit/<int:id>/')
def discuss_edit(id):
    if not session['login']:
        return redirect('/login/')
    #try:
    d = Discuss(id)
    #except:
    #    return "Discuss Not Found", 404
    seer = User(session['id'])
    if not seer.admin and seer.id != d.pub_id:
        return '你没有修改该临时帖子的权限'
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
    seer = User(session['id'])
    if not seer.admin and seer.id != d.pub_id:
        return '你没有修改该临时帖子的权限'
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
    seer = User(session['id'])
    if not seer.admin and seer.id != d.pub_id:
        return '你没有修改该临时帖子的权限'
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
    seer = User(session['id'])
    if not seer.admin and seer.id != d.pub_id:
        return '你没有修改该临时帖子的权限'
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
    if not session['login']:
        return redirect('/login/')
    return render_template("discuss_pic_upload.html", session = session)

@app.route('/discuss/pic_handle/', methods = ['POST'])
def pic_handle():
    if not session['login']:
        return redirect('/login/')
    
    
    if 'file' not in request.files:
        return '上传失败'
 
    file = request.files['file']
    if file.filename == '':
        return '上传失败'
 
    if file:
        f = open("./static/discuss_img/file_cnt.txt", 'r')
        dat = int(f.read()) + 1
        f.close()
        f = open("./static/discuss_img/file_cnt.txt", 'w')
        f.write(str(dat))
        f.close()
        filepath = str(dat) + os.path.splitext(file.filename)[1]
        file.save(os.path.join('./static/discuss_img/', filepath))
        return render_template("discuss_pic_upload.html", session = session, postad = filepath)

@app.route('/discuss/file_upload/')
def file_upload():
    if not session['login']:
        return redirect('/login/')
    return render_template("discuss_file_upload.html", session = session)

@app.route('/discuss/file_handle/', methods = ['POST'])
def file_handle():
    if not session['login']:
        return redirect('/login/')
    
    
    if 'file' not in request.files:
        return '上传失败'
 
    file = request.files['file']
    if file.filename == '':
        return '上传失败'
 
    if file:
        f = open("./static/discuss_file/file_cnt.txt", 'r')
        dat = int(f.read()) + 1
        f.close()
        f = open("./static/discuss_file/file_cnt.txt", 'w')
        f.write(str(dat))
        f.close()
        filepath = str(dat) + os.path.splitext(file.filename)[1]
        file.save(os.path.join('./static/discuss_file/', filepath))
        return render_template("discuss_file_upload.html", session = session, postad = filepath)


'''
@app.route('/search/')
def search():
    rsearch = request.form.get('resource_search', '')
    gettypes = request.form.get('cb', '2,3')
    sortways = request.form.get('sw', 'a')
    print("Log To Console : ", rsearch, gettypes, sortways)
    return render_template("search.html", session = session, rsearch = rsearch, cw = gettypes, sw = sortways)
    # prs = rsearch, sc = gettypes, ff = sortways
'''

@app.route('/discuss/list/')
def discuss_search():
    session['id'] = 0
    rsearch = request.args.get('resource_search', '')
    fr = all_discuss(None, None, session['id'])
    ft = []
    for it in fr:
        if rsearch in it[2]:
            ft.append(it[0])
    fg = []
    for it in ft:
        fg.append(Discuss(it))
    return render_template("discuss.html", session = session, rsearch = rsearch, dis = fg)

@app.route('/activity/')
def activity():
    return render_template("activity.html", session = session)

@app.route('/activity/learn/')
def learn():
    return render_template("learn.html", session = session)

@app.route('/activity/learn/yuwen/')
def yuwen():
    # items每项是列表，第0项是item-20xx_xx，第1项是“20xx年第x期”，第2项是discuss content
    f = open('learn.txt', 'r', encoding='utf-8')
    content = f.read().split('>\n')
    f.close()
    yuwen = content[0]
    yuwen = yuwen.split('\n')
    idx = 0
    items = []
    for i in yuwen:
        if i == '':
            continue
        item = i.split(':')
        ic = 'item-' + item[0]
        l = item[0].split('_')
        wd = l[0] + '年第' + str(int(l[1])) + '期'
        fd = open(f'./discuss/{item[1]}.txt', 'r', encoding="utf-8")
        ct = fd.read()
        fd.close()
        items[idx] = [ic, wd, ct]
    return render_template("yuwen.html", session = session, items = items)

@app.route('/activity/learn/shuxue/')
def shuxue():
    return render_template("shuxue.html", session = session)

@app.route('/activity/learn/yingyu/')
def yingyu():
    return render_template("yingyu.html", session = session)

@app.route('/activity/learn/daodeyufazhi/')
def daodeyufazhi():
    return render_template("daodeyufazhi.html", session = session)

@app.route('/activity/learn/lishi/')
def lishi():
    return render_template("lishi.html", session = session)

@app.route('/activity/learn/dili/')
def dili():
    return render_template("dili.html", session = session)

@app.route('/activity/learn/shengwu/')
def shengwu():
    return render_template("shengwu.html", session = session)

@app.route('/activity/learn/huaxue/')
def huaxue():
    return render_template("huaxue.html", session = session)

@app.route('/activity/learn/wuli/')
def wuli():
    return render_template("wuli.html", session = session)

@app.route('/activity/learn/yishu/')
def yishu():
    return render_template("yishu.html", session = session)


@app.route('/resource/')
def resource():
    return render_template('resource.html', session = session)

@app.route('/album/')
def album():
    return render_template("album.html", session = session)

@app.route('/forum/')
def forum():
    return redirect('/discuss/list')

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

@app.route("/user/me/")
def user_me():
    if not session['login']:
        return redirect('/login/')
    u = User(session['id'])
    return render_template("user_me.html", user = u, session = session)


@app.route("/user/<int:id>/")
def user(id):
    if id == session['id']:
        return redirect('../me/')
    u = User(id)
    return render_template("user.html", user = u, session = session)

@app.route("/user/<int:id>/fix/")
def user_fix(id):
    if not session['login']:
        return redirect('/login/')
    if session['id'] != id or not User(session['id']).admin:
        return '你没有更改该用户的权限'
    u = User(id)
    return render_template("user_fix.html", user = u, session = session)

@app.route("/user/<int:id>/fix/handle/", methods = ["POST"])
def user_fix_handle(id):
    if not session['login']:
        return redirect('/login/')
    if session['id'] != id or not User(session['id']).admin:
        return '你没有更改该用户的权限'
    u = User(id)
    username = request.args.get("username")
    rname = request.args.get("rname")
    sign = request.args.get("sign")
    avatar = request.args.get("avatar")
    if 'avatar' in request.files:
        ava = request.files['avatar']
        if ava.filename != '' and ava:
            filepath = str(dat) + os.path.splitext(ava.filename)[1]
            ava.save(os.path.join('../static/user_pic/', filepath))
            u.picpath = ava
    old_pwd = request.args.get("old_pwd")
    new_pwd = request.args.get("new_pwd")
    if old_pwd == u.password:
        u.password = new_pwd
    if username:
        u.username = username
    if rname:
        u.name = rname
    if sign:
        u.desc = sign
    u.save(None)
    return redirect("../../")

@app.route("/setting/")
def setting():
    # a = session['tmp-rname']
    # b = session['tmp-eduid']
    # c = session['tmp-pwd']
    # try:
    #     d = session['tmp-id']
    # except:
    #     d = 0
    if not session['login']:
        return redirect('/login/')
    if not session['admin']:
        return redirect('/')
    return render_template("settings.html", session = session, content = '') # , a = a, b = b, c = c, d = d) 

@app.route("/setting/handle1/")
def setting_handle1():
    if not session['login']:
        return redirect('/login/')
    if not User(session['id']).admin:
        return redirect('/')
    name = request.args.get('docname', '')
    f = open(f"./{name}.txt", "r", encoding='utf-8')
    con = f.read()
    f.close()
    return render_template("settings.html", session = session, content = con) 

@app.route("/setting/handle2/")
def setting_handle2():
    if not session['login']:
        return redirect('/login/')
    if not User(session['id']).admin:
        return redirect('/')
    name = request.args.get('docname', '')
    con = request.args.get('txt', '')
    f = open(f"./{name}.txt", "w", encoding='utf-8')
    f.write(con)
    f.close()
    return render_template("settings.html", session = session, content = '') 

# @app.route("/setting/handle3", methods=['GET','POST'])
# def setting_handle3():
#     id = request.form.get("id")
#     u = User(id = id)
#     return render_template("user.html", session = session, user = u)


@app.route('/about/')
def about():
    return render_template('about.html', session = session)

@app.route('/about/course/')
def course():
    return render_template('course.html', session = session)

@app.route('/about/manage/')
def manage():
    return render_template('manage.html', session = session)

@app.route('/about/ula/')
def ula():
    return render_template('ula.html', session = session)

@app.route("/about/feedback/")
def feedback():
    return render_template("feedback.html", session = session)

@app.route("/error500/")
def error500page():
    return render_template("500.html", session = session)

@app.route("/error404")
def error404page():
    return render_template("404.html", session = session)

@app.errorhandler(404)
def error404(error):
    return redirect("/error404/"), 404

@app.errorhandler(500)
def error500(error):
    return redirect("/error500/"), 500

if __name__ == "__main__":
    app.run(port = 5000)