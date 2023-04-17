#!\venv\bin\python3
import http.cookies as Cookie
import sqlite3
import os


def printHeader(title):
    print("Content-type: text/html")
    print("")
    print("<html><head><title>{}</title></head><body>".format(title))


def printFooter():
    print("</body></html>")


printHeader("Logout process")
if "HTTP_COOKIE" in os.environ:
    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
    if "session" in cookie.keys():
        conn = sqlite3.connect("rent-house.db")
        c = conn.cursor()
        c.execute("SELECT * FROM USER WHERE sessionID= ?", (cookie["session"].value,))
        row = c.fetchone()
        if row is not None:
            c.execute("UPDATE USER SET sessionID = -1 WHERE username = ?", (row[0],))
            conn.commit()
            conn.close()
            print("<script>")
            print("document.cookie = 'session=; expires=Thu, 01 Jan 1970 00:00:00 UTF; path=/;';")
            print("window.location = 'index.py';")
            print("</script>")
