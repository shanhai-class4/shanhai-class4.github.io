import sqlite3
from datetime import *

def b_render(content):
    content = content.replace("\n", "   ")
    content = content.replace(r"\\", '\\')

    content = content.replace("\\==", "[高亮]")
    content = content.replace("\\=?", "")
    content = content.replace("\\>", "[引用]")
    content = content.replace("\\>>", "")
    content = content.replace(r"\##", "[标题]")
    content = content.replace(r"\@@", "")
    content = content.replace(r"\#", "[小标题]")
    content = content.replace(r"\@", "")
    content = content.replace(r"\*\*", "[粗体]")
    content = content.replace(r"\*", "")
    content = content.replace(r"\?\?", "[斜体]")
    content = content.replace(r"\?", "")
    content = content.replace(r"\_\_", "[下划线]")
    content = content.replace(r"\_", "")
    content = content.replace(r"\+", "[链接]")
    content = content.replace(r"\-", "")
    content = content.replace(r"\=", "")
    
    content = content.replace("\\![", "[图片]")
    content = content.replace("\\]", "")

    content = content.replace("\\/", "[文件]")
    content = content.replace("\\~", "")
    
    
    #content = content.replace("\\+", "<a href = \"")
    #content = content.replace("\\-", "\">")
    
    return content


def render(content, tmp = False):
    content = content.replace("\n", "<br />")
    content = content.replace("\\\\", "\\")

    content = content.replace("\\==", "<mark>")
    content = content.replace("\\=?", "</mark>")
    content = content.replace("\\>", "<blockquote>")
    content = content.replace("\\>>", "</blockquote>")
    content = content.replace("\\##", "<h2>")
    content = content.replace("\\@@", "</h2>")
    content = content.replace("\\#", "<h3>")
    content = content.replace("\\@", "</h3>")
    content = content.replace("\\*\\*", "<strong>")
    content = content.replace("\\*", "</strong>")
    content = content.replace("\\?\\?", "<i>")
    content = content.replace("\\?", "</i>")
    content = content.replace("\\_\\_", "<u>")
    content = content.replace("\\_", "</u>")
    content = content.replace("\\+", "<a href = \"")
    content = content.replace("\\-", "\">")
    content = content.replace("\\/", "<a href = \"path")
    content = content.replace("\\~", '\" download>')
    content = content.replace("\\=", "</a>")
    
    if not tmp:
        content = content.replace("\\![", "<img src = \"../../static/discuss_img/")
        content = content.replace("path", "../../static/discuss_file/")
    else:
        content = content.replace("\\[", "<img src = \"../../../static/discuss_img/")
        content = content.replace("path", "../../../static/discuss_file/")
    content = content.replace("\\]", "\" />")
    
    
    #content = content.replace("\\+", "<a href = \"")
    #content = content.replace("\\-", "\">")
    
    return content


def get_cursor():
    # conn = sqlite3.connect("./database.db")
    conn = sqlite3.connect("./0.db")
    cursor = conn.cursor()
    return (conn, cursor)

def all_users():
    c = get_cursor()
    c[1].execute("SELECT * FROM users")
    aus = c[1].fetchall()
    kd = []
    for au in aus:
        kd.append(str(au[0]))
    c[0].commit()
    c[0].close()
    return ','.join(kd)

def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')