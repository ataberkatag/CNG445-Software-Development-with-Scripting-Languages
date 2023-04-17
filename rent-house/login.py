#!\usr\bin\python3
import cgi
import random
import sqlite3
import http.cookies as Cookie


def printHeader(title):
    html = """Content-type:text/html\r\n\r\n
	<html>
	<head>
	<meta charset="UTF-8">
	<meta name="description" content="This is Cyprus rent-house web application">
	<meta name="author" content="Ahmet Kutay Ural">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">													<!-- This gives the browser instructions on how to control the page's dimensions 																																and scaling. -->
	<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">									<!-- I used Icon in my div that's why i import google material icons library. 																																	Information gathered from:																																										http://www-db.deis.unibo.it/courses/TW/DOCS/w3schools/icons/default.asp.html  -->
	<link rel="stylesheet" type="text/css" href="login.css">
	<title>{}</title>
	</head>\r\n\r\n
	<body>""".format(title)
    print(html)


def printFooter():
    html = """
    </body>
    </html>"""
    print(html)


def countDigits(value):
    counter = 0
    for p in value:
        if p.isdigit():
            counter += 1
    return counter


def printBodyContent(formData):
    html = """<div class="container">
	<h1>Login to Cyprus<br> Rent-House</h1>
	<span class="material-icons md-100 md-light">account_circle</span><br><br>
	<form class="loginForm" name="myLoginForm">
    """

    check1 = True
    check2 = True

    if "username" not in formData.keys():
        html = html + """<label for="username">Username:</label>
      	<input type="text" id="username" name="username"><br>
      	<p>*Username should be entered!</p>
        """
        print(html)
        check1 = False
    else:
        html = html + """<label for="username">Username:</label>
        <input type="text" id="username" name="username"><br><br>
        """
        print(html)

    if "password" not in formData.keys():
        html = html + """<label for="password">Password:</label>
        <input type="text" id="password" name="password"><br>
        <p>*Password should be entered!</p>
        """
        print(html)
        check2 = False
    else:
        html = html + """<label for="password">Password:</label>
        <input type="text" id="password" name="password"><br><br>
        """
        print(html)

    if check1 and check2:
        conn = sqlite3.connect("rent-house.db")
        c = conn.cursor()
        c.execute("SELECT * FROM USER WHERE username = ? AND password = ?",
                  (formData["username"].value, formData["password"].value,))
        row = c.fetchone()

        if row is not None:
            html = html + """<input type="submit" value="Login"><br><br>
            </form>
            """
            print(html)
            cookie = Cookie.SimpleCookie()
            cookie["session"] = random.randint(1, 1000000)
            cookie["session"]["domain"] = "localhost"
            cookie["session"]["path"] = "/"
            c.execute("UPDATE USER SET sessionID = ? WHERE username = ?",
                      (cookie["session"].value, formData["username"].value))
            conn.commit()
            print("<script>")
            print("document.cookie = '{}';".format(
                cookie.output().replace("Set-Cookie: ", "")))  # Seting cookie with JS
            print("window.location = 'index.py';")
            print("</script>")

        else:
            html = html + """<input type="button" value="Go Back!" onclick="history.back()"><br><br>
            </form>
            """
            html = html + """<p>Username or Password incorrect! Please try it again. <p>
            """
            print(html)
    else:
        html = html + """<input type="button" value="Go Back!" onclick="history.back()"><br><br>
        </form>
        """
    html = html + """</div>
    """
    print(html)


formData = cgi.FieldStorage()

printHeader("Login")
printBodyContent(formData)
printFooter()
