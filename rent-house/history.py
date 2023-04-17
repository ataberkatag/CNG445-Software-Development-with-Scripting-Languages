#!\venv\bin\python3
import cgi
import http.cookies as Cookie
import os
import sqlite3


def printHeader(title):
    html = """Content-type:text/html\r\n\r\n
	<html>
	<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link type="text/css" rel="stylesheet" href="history.css" />
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">		
	<link href="https://fonts.googleapis.com/css2?family=Fjalla+One&family=Pacifico&display=swap" rel="stylesheet">
	<title>{}</title>
	</head>\r\n\r\n
	<body>""".format(title)
    print(html)


def printNavBar():
    html = """<div class="topnav">
	<label class="Logo">Cyprus Rent-House</label>
    <a href="/rent-house/logout.py"><span class="material-icons md-24 md-light">logout</span></a>
    <a href="/rent-house/history.py"><span class="material-icons md-24 md-light">history</span></a>
    <a href="/rent-house/advertise.html"><span class="material-icons md-24 md-light">add</span></a>
    <a href="/rent-house/index.py"><span class="material-icons md-24 md-light">home</span></a>
	</div>
    """
    print(html)


def printFooter():
    html = """
    </body>
    </html>"""
    print(html)


def getCity(cityId):
    if cityId == 1:
        return "LEFKOSA"
    elif cityId == 2:
        return "GIRNE"
    elif cityId == 3:
        return "GAZI MAGUSA"
    elif cityId == 4:
        return "ISKELE"
    elif cityId == 5:
        return "GUZELYURT"
    elif cityId == 6:
        return "LEFKE"


def printTable(rows):
    count = 0
    html = """<h1>Previously Posted Advertisements</h1>
    <form class="filterForm" name="myForm" action="history.py" method="get">
    <table id="houses" style="width:100%">
    <tr>
    <th>Street</th>
    <th>City</th>
    <th>Number Of Bedrooms</th>
    <th>Monthly Fee($)</th>
    <th>Delete</th>
    </tr>"""
    for items in rows:  # In order to make my list listed last 10 active
        if count < 10:
            html = html + """<tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td><input type="submit" name="delete{}" value="Delete"></td>
            </tr>
            """.format(items[1], getCity(items[5]), items[2], items[3], count)
            count += 1
        else:
            break

    html = html + "</table></form>"
    print(html)


def delete(houseId):
    conn = sqlite3.connect("rent-house.db")
    c = conn.cursor()
    c.execute("DELETE FROM HOUSE WHERE houseid= ?", (houseId,))
    row = c.fetchone()
    conn.commit()
    conn.close()
    print("<script>")
    print("window.location = 'history.py';")
    print("</script>")


def deleteRecord(formData, rows):
    if "delete0" in formData.keys():
        houseId = rows[0][0]
        delete(houseId)
    elif "delete1" in formData.keys():
        houseId = rows[1][0]
        delete(houseId)
    elif "delete2" in formData.keys():
        houseId = rows[2][0]
        delete(houseId)
    elif "delete3" in formData.keys():
        houseId = rows[3][0]
        delete(houseId)
    elif "delete4" in formData.keys():
        houseId = rows[4][0]
        delete(houseId)
    elif "delete5" in formData.keys():
        houseId = rows[5][0]
        delete(houseId)
    elif "delete6" in formData.keys():
        houseId = rows[6][0]
        delete(houseId)
    elif "delete7" in formData.keys():
        houseId = rows[7][0]
        delete(houseId)
    elif "delete8" in formData.keys():
        houseId = rows[8][0]
        delete(houseId)
    elif "delete9" in formData.keys():
        houseId = rows[9][0]
        delete(houseId)



def getRows():
    if "HTTP_COOKIE" in os.environ:
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        if "session" in cookie.keys():
            conn = sqlite3.connect("rent-house.db")
            c = conn.cursor()
            c.execute("SELECT * FROM USER WHERE sessionID= ?", (cookie["session"].value,))
            row = c.fetchone()
            print()
            username = row[0]
            c.execute("SELECT * FROM HOUSE WHERE username= ?", (username,))
            rows = c.fetchall()
            return rows


printHeader("Previous Advertisements")
printNavBar()
rows = getRows()
if rows:
    printTable(rows)
else:
    html = """<p>No advertisement found</p>
    """
    print(html)
formData = cgi.FieldStorage()
deleteRecord(formData, rows)

printFooter()
