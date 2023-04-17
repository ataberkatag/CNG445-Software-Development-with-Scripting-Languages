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
	<link type="text/css" rel="stylesheet" href="index.css" />
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">		
	<link href="https://fonts.googleapis.com/css2?family=Fjalla+One&family=Pacifico&display=swap" rel="stylesheet">
	<title>{}</title>
	</head>\r\n\r\n
	<body>""".format(title)
    print(html)


def printFooter():
    html = """
    </body>
    </html>"""
    print(html)


def printNavbar():
    html = """<div class="topnav">
    <label class="Logo">Cyprus Rent-House</label>
    <a href="/rent-house/login.html"><span class="material-icons md-24 md-light">login</span></a>
    <a href="/rent-house/register.html"><span class="material-icons md-24 md-light">person_add</span></a>
    <a href="/rent-house/index.py"><span class="material-icons md-24 md-light">home</span></a>
    </div>
    <h1>Welcome To Cyprus Rent-House</h1>
    <p><span class="tab"></span>If you want your house to be rented quickly, <a href="#">register</a> now to not miss opportunities.<p>
    """
    print(html)


def printNavbarLoggedIn():
    html = """<div class="topnav">
    <label class="Logo">Cyprus Rent-House</label>
    <a href="/rent-house/logout.py"><span class="material-icons md-24 md-light">logout</span></a>
    <a href="/rent-house/history.py"><span class="material-icons md-24 md-light">history</span></a>
    <a href="/rent-house/advertise.html"><span class="material-icons md-24 md-light">add</span></a>
    <a href="/rent-house/index.py"><span class="material-icons md-24 md-light">home</span></a>
    </div>
    <h1>Welcome To Cyprus Rent-House</h1>
    <p><span class="tab"></span>Welcome back to Cyprus Rent-House. If you want to see previous advertisements that you posted, <a href="/rent-house/history.py">click</a>.<p>
    """
    print(html)


def printTable(rows):
    count = 0
    html = """<table id="houses" style="width:100%">
    <tr>
    <th>Street</th>
    <th>City</th>
    <th>Number Of Bedrooms</th>
    <th>Monthly Fee($)</th>
    <th>Contact E-mail</th>
    <th>Contact Phone</th>
    </tr>"""
    for items in rows[::-1]:  # In order to make my list listed last 10 active
        if count < 10:
            html = html + """<tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            </tr>
            """.format(items[0], items[1], items[2], items[3], items[4], items[5])
            count += 1
        else:
            break

    html = html + "</table>"
    print(html)


def checkLoginStatus():
    if "HTTP_COOKIE" in os.environ:
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        if "session" in cookie.keys():
            conn = sqlite3.connect("rent-house.db")
            c = conn.cursor()
            c.execute("SELECT * FROM USER WHERE sessionID = ?", (cookie["session"].value,))
            row = c.fetchone()
            conn.close()
            if row is not None:
                return True
            else:
                return False


def getRows():
    # query string
    filters = {}
    storage = cgi.FieldStorage()
    keys = storage.keys()
    if 'city' in keys:
        filters['city'] = storage['city'].value
    if 'bedrooms' in keys:
        filters['bedrooms'] = storage['bedrooms'].value
    if 'fee' in keys:
        filters['fee'] = storage['fee'].value

    sql = """SELECT HOUSE.street, CITY.cname, HOUSE.number_of_bedrooms,
              HOUSE.monthly_fee, USER.email, USER.phone_number 
              FROM 
              HOUSE 
              LEFT JOIN USER ON HOUSE.username = USER.username 
              LEFT JOIN CITY ON HOUSE.cid = CITY.cid"""

    if len(filters) > 0:

        sqlWheres = []
        for filterKey in filters:
            value = filters[filterKey]
            key = ""
            if filterKey == 'city':
                key = 'CITY.cname'
                sqlWheres.append(f"{key}='{value}'")
            if filterKey == 'bedrooms':
                key = 'HOUSE.number_of_bedrooms'
                sqlWheres.append(f"{key}>={value}")
            if filterKey == 'fee':
                key = 'HOUSE.monthly_fee'
                sqlWheres.append(f"{key}>={value}")

        sqlWhereString = " AND ".join(sqlWheres)

        sql = sql + f" WHERE {sqlWhereString}"

    conn = sqlite3.connect("rent-house.db")
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    return rows


def printFilter():
    html = """<form class="filterForm" name="myForm" action="index.py" method="get">
    <label for="city">City:</label>
    <input type="text" id="city" name="city">
	<label for="street">Minimum fee:</label>
  	<input type="text" id="fee" name="fee">
  	<label for="bedrooms">Minimum number of bedrooms:</label>
  	<input type="text" id="bedrooms" name="bedrooms">
  	<input type="submit" value="Filter">
  	</form>
    """
    print(html)


logged_in = checkLoginStatus()

printHeader("Welcome")
if logged_in:
    printNavbarLoggedIn()
else:
    printNavbar()

printFilter()

rows = getRows()
if rows:
    printTable(rows)
else:
    html = """<p>No advertisement found</p>
    """

printFooter()
