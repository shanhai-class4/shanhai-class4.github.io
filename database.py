import sqlite3
from utils import *

'''
# 父讨论为father的所有讨论
# 自动排序
def discuss_all_t(father = None):
    c = get_cursor()
    c[1].execute("SELECT * FROM discuss;")
    d = c[1].fetchall()
    c[0].commit()
    c[0].close()
    topd = []
    pd = []
    for i in d:
        if i[1] == father:
            if i[7]:
                topd.append(i)
            else:
                pd.append(i)
    pd = sorted(pd, key = lambda s: s[4])
    topd.extend(pd)
    return topd

# 转换为id
def toid(d):
    ids = []
    for i in d:
        ids.append(i[0])
    return ids

# 父讨论为father的所有讨论id
# 自动排序
def discuss_all(father = None):
    return toid(discuss_all_t(father))

def discuss_t(user_id, father = None):
    d = discuss_all_t(father)
    nd = []
    for i in d:
        if str(user_id) in i[6].split(','): # user_id可见
            nd.append(i)
    return nd

# 父讨论为father的user_id可见讨论id
# 自动排序
def discuss(user_id, father = None):
    d = discuss_all_t(father)
    nd = []
    for i in d:
        if str(user_id) in i[6].split(','): # user_id可见
            nd.append(i)
    return toid(nd)

# 发布者为pub_id（Ta的讨论），且父讨论为None的user_id可见讨论id
# 自动排序
def discuss_f(user_id, pub_id):
    d = discuss_all_t(None)
    nd = []
    for i in d:
        if i[5] == pub_id and str(user_id) in i[6].split(','): # pub_id发出且user_id可见
            nd.append(i)
    return toid(nd)

# 自动打开news_id新闻id文件，并返回新闻id
# 不排序
def news_discuss():
    f = open("./news_id.txt", 'r', encoding = 'utf-8')
    data = f.readlines()
    f.close()
    news_id = []
    for d in data:
        news_id.append(int(d))
    return news_id
'''

def all_discuss(father = None, pub = None, visiter = None):
    c = get_cursor()
    if pub:
        if father:
            c[1].execute(f"SELECT * FROM discuss WHERE father = {father}, pub = {pub}")
        else:
            c[1].execute(f"SELECT * FROM discuss WHERE pub = {pub}")
    else:
        if father:
            c[1].execute(f"SELECT * FROM discuss WHERE father = {father}")
        else:
            c[1].execute("SELECT * FROM discuss")
    ls = c[1].fetchall()
    cooked = []
    if visiter:
        for item in ls:
            if item[6] == 'all' or str(visiter) in item[6].split(','):
                cooked.append(item)
    else:
        cooked = ls
    cooked = sorted(cooked, key = lambda s : s[4])
    toped = []
    normal = []
    for item in cooked:
        if item[7]:
            toped.append(item)
        else:
            normal.append(item)
    toped.extend(normal)
    ans = toped
    cans = []
    for item in ans:
        if item[8] == 0:
                cans.append(item)
    c[0].commit()
    c[0].close()
    return cans

class Discuss:
    def __init__(self, id):
        c = get_cursor()
        c[1].execute(f"SELECT * FROM discuss WHERE id = '{id}'")
        dis = c[1].fetchall()[0]
        print(dis)
        self.info = dis # 全部信息 
        self.id = dis[0]
        if dis[9] == None:
            self.fname = None # 文件名
            if dis[2] == None:
                self.type = 1 # 类型
                self.type_sh = "短评"
            else:
                self.type = 0
                self.type_sh = "文章"
        else:
            self.type = 2
            self.type_sh = "文件" # 对外显示
            self.fname = dis[9] 
        self.url = f"/discuss/{dis[0]}"
        self.turl = f"./discuss/{dis[0]}.txt" 
        self.father = dis[1]
        if self.father == None:
            self.father = 0
        self.title = dis[2]
        self.subject = dis[3]
        self.pub_time = dis[4]
        self.pub_id = dis[5]
        c[1].execute(f"SELECT * FROM users WHERE id = {self.pub_id}")
        dat = c[1].fetchall()[0]
        self.pub_name = dat[1]
        self.pub_pic = dat[8]
        self.csee = dis[6] # 可见人群
        self.csee_cnt = -1
        if self.csee != "all":
            self.csee_cnt = len(self.csee.split(','))
        self.top = dis[7]
        self.temp = dis[8] # 是否为临时文章
        f = open(self.turl, 'r', encoding = 'utf-8') # 具体内容
        self.all_data = f.read() # 未经渲染的内容
        f.close()
        self.main_data = b_render(self.all_data)[0:50] # 摘要
        self.main_data += "..."
        if self.title != None:
            self.title_sh = self.title
        else:
            self.title_sh = "[短评]" + b_render(self.all_data)
        if len(self.title_sh) >= 16:
            self.title_sh = self.title_sh[0:16] + "..."
        self.desc = dis[10]
        c[0].commit()
        c[0].close()
    
    def cos(self): # 自洽
        c = get_cursor()
        c[1].execute(f"SELECT * FROM users WHERE id = '{self.pub_id}'")
        dat = c[1].fetchone()
        self.pub_name = dat[1]
        self.pub_pic = dat[8]
        self.csee_cnt = -1
        if self.csee != "all":
            self.csee_cnt = len(self.csee.split(','))
        if self.title != None:
            self.title_sh = self.title
        else:
            self.title_sh = "[短评]" + b_render(self.all_data)
        if len(self.title_sh) >= 16:
            self.title_sh = self.title_sh[0:16] + "..."
        self.main_data = b_render(self.all_data)[0:50]
        self.main_data += "..."
        if self.type == 0:
            if self.title == None:
                self.title = "[无标题]"
            if self.fname != None:
                self.fname = None
        elif self.type == 1:
            if self.title != None:
                self.title = None
            if self.fname != None:
                self.fname = None
        else:
            if self.title == None:
                self.title = "[无标题]"
            if self.fname == None:
                self.fname = "未知.txt"
        c[0].commit()
        c[0].close()
    
    def save(self, id): # 保存到discuss
        if id == None:
            id = self.id
        self.cos()
        c = get_cursor()
        c[1].execute(f"UPDATE discuss SET father = {self.father}, title = '{self.title}', subject = '{self.subject}', date = '{self.pub_time}', pub = {self.pub_id}, csee = '{self.csee}', top = {self.top}, temp = {self.temp}, fname = '{self.fname}', desc = '{self.desc}' WHERE id = {id}")
        c[0].commit()
        c[0].close()
    
    def insert(self): # 复制一份插入
        self.cos()
        c = get_cursor()
        c[1].execute(f"INSERT INTO discuss (father, title, subject, date, pub, csee, top, temp, fname, desc) VALUES ({self.father}, {self.title}, {self.subject}, {self.pub_time}, {self.pub_id}, {self.csee}, {self.top}, {self.temp}, {self.fname}, {self.desc})")
        nowid = c[1].lastrowid
        c[0].commit()
        c[0].close()
        return nowid
    
    def insert_tr(self): # 自己复制一份插入到resourse
        self.cos()
        c = get_cursor()
        c[1].execute(f"INSERT INTO resource (father, title, subject, date, pub, csee, top, temp, fname, desc) VALUES ({self.father}, {self.title}, {self.subject}, {self.pub_time}, {self.pub_id}, {self.csee}, {self.top}, {self.temp}, {self.fname}, {self.desc})")
        nowid = c[1].lastrowid
        c[0].commit()
        c[0].close()
        return nowid
        
'''
            
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
'''

class User:
    def __init__(self, id):
        if id == 0:
            self.info = "未登录"
            self.admin = 0
        else:
            c = get_cursor()
            c[1].execute(f"SELECT * FROM users WHERE id = '{id}'")
            dis = c[1].fetchall()[0]
            self.info = dis
            self.id = dis[0]
            self.url = f"/user/{dis[0]}" # 访问个人主页的路径
            self.username = dis[1] # 用户名
            self.password = dis[2] # 密码
            self.name = dis[3] # 真实姓名
            self.lsc = (dis[4], dis[5], dis[6]) # 暂时没用的（4:性别，5:教育ID，6:手机号）
            self.admin = dis[7] # 是否为管理员（1，0）
            self.picpath = dis[8] # 头像路径
            self.desc = dis[9] # 个性签名
            c[0].commit()
            c[0].close()
    
    def save(self, id): # 将用户信息保存
        if id == None:
            id = self.id
        c = get_cursor()
        print(f"UPDATE users SET username = '{self.username}', password = '{self.password}', name = '{self.name}', level = {self.lsc[0]}, score = {self.lsc[1]}, active = {self.lsc[2]}, admin = {self.admin}, picpath = {self.picpath},  desc = {self.desc} WHERE id = {id}")
        c[1].execute(f"UPDATE users SET username = '{self.username}', password = '{self.password}', name = '{self.name}', level = {self.lsc[0]}, score = {self.lsc[1]}, active = {self.lsc[2]}, admin = {self.admin}, picpath = '{self.picpath}', desc = '{self.desc}' WHERE id = {id}")
        c[0].commit()
        c[0].close()











'''
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  0
username TEXT NOT NULL,                         1
password TEXT NOT NULL,                         2
name TEXT NOT NULL,                             3
level INT NOT NULL,                             4
score INT NOT NULL,                             5
active INT NOT NULL,                            6
admin INT NOT NULL,                             7
picpath TEXT NOT NULL,                          8
desc TEXT                                       9
'''