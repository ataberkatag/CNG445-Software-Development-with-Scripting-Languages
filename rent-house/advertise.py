#!\venv\bin\python3
import cgi
import http.cookies as Cookie
import os
import sqlite3


def printHeader(title):
    html = """Content-type:text/html\r\n\r\n
	<html>
	<head>
	<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<link type="text/css" rel="stylesheet" href="advertise.css" />
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


def printBodyContent(formData):
    html = """<div class="container">
	<h1>Advertise Your Home<br></h1>
	<form class="AdvertiseForm" name="myForm">
    """
    check1 = True
    check2 = True
    check3 = True
    if "street" not in formData.keys():
        html = html + """<label for="street">Street:</label>
  		<input type="text" id="street" name="street"><br>
  		<p>*Street should be entered!</p>
        """
        print(html)
        check1 = False
    else:
        html = html + """<label for="street">Street:</label>
        <input type="text" id="street" name="street"><br><br>
        """
        print(html)

    if "noOfBedrooms" not in formData.keys():
        html = html + """<label for="noOfBedrooms">No of Bedrooms:</label>
  		<input type="text" id="noOfBedrooms" name="noOfBedrooms"><br>
  		<p>*Number of Bedrooms should be entered!</p>
        """
        print(html)
        check2 = False
    else:
        html = html + """<label for="noOfBedrooms">No of Bedrooms:</label>
        <input type="text" id="noOfBedrooms" name="noOfBedrooms"><br><br>
        """
        print(html)

    if "monthlyFee" not in formData.keys():
        html = html + """<label for="monthlyFee">Monthly Fee:</label>
		<input type="text" id="monthlyFee" name="monthlyFee"><br>
		<p>*Monthly Fee should be entered!</p>
        """
        check3 = False
        print(html)
    else:
        html = html + """<label for="monthlyFee">Monthly Fee:</label>
        <input type="text" id="monthlyFee" name="monthlyFee"><br><br>
        """
        print(html)

    html = html + """<label for="city">City:</label>
    <select class="selectCity" id="city">
	<option value="1">Lefkosa</option>
	<option value="2">Girne</option>
	<option value="3">Gazi Magusa</option>
	<option value="4">Iskele</option>
	<option value="5">Guzelyurt</option>
	<option value="6">Lefke</option>
	</select><br><br>
    """
    print(html)

    if check1 and check2 and check3:
        if "HTTP_COOKIE" in os.environ:
            cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])

            if "session" in cookie.keys():
                conn = sqlite3.connect("rent-house.db")
                c = conn.cursor()
                c.execute("SELECT * FROM USER WHERE sessionID= ?", (cookie["session"].value,))
                row = c.fetchone()

                c.execute("INSERT INTO HOUSE(street,number_of_bedrooms,monthly_fee,username,cid) VALUES (?,?,?,?,?)", (
                formData["street"].value, formData["noOfBedrooms"].value, formData["monthlyFee"].value, row[0],
                formData["city"].value))
                conn.commit()
                html = html + """<input type="button" value="Go Back!" onclick="history.back()"><br><br>
                <span class="success"><p id="success"></p></span>
		        </form>
	            </div>
                """
                print(html)
                print("<script>")
                print("document.getElementById('success').innerHTML = 'Succesfully added.'")
                print("</script>")
                conn.close()
        else:
            print("<p>Login Required!")
    else:
        html = html + """<input type="button" value="Go Back!" onclick="history.back()"><br><br>
        </form>
        </div>
        """
        print(html)


def printFooter():
    html = """
    </body>
    </html>"""
    print(html)


formData = cgi.FieldStorage()

printHeader("Advertise Your Home")
printNavBar()
printBodyContent(formData)
printFooter()
