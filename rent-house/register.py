#!\venv\bin\python3
import cgi
import sqlite3


def printHeader(title):
    html = """Content-type:text/html\r\n\r\n
	<html>
	<head>
	<meta charset="UTF-8">
	<meta name="author" content="Ahmet Kutay Ural">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">	
	<link rel="stylesheet" type="text/css" href="register.css">								<!-- Link to Css file -->
	<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">	
	<title>{}</title>
	</head>\r\n\r\n
	<body>""".format(title)
    print(html)


def countDigits(value):
    counter = 0
    for p in value:
        if p.isdigit():
            counter += 1
    return counter


def printBodyContent(formData):
    html = """<div class="container">
	<h1>Register to Cyprus<br> Rent-House</h1>
	<span class="material-icons md-100 md-light">person_add</span><br>
	<form class="RegisterForm" action="register.py method="post">
    """
    check1 = True
    check2 = True
    check3 = True
    check4 = True
    check5 = True

    if "username" not in formData.keys():
        html = html + """<label for="username">Username:</label>
  		<input type="text" id="username" name="username"><br>
  		<p>*Username should be entered!</p>
        """
        print(html)
        check1 = False
    else:
        html = html + """<label for="username">Username:</label>
        <input type="text" id="username" name="username"><br>
        """
        print(html)

    if "pwd" not in formData.keys():
        html = html + """<label for="password">Password:</label>
		<input type="text" id="password" name="pwd"><br>
		<p>*Password should be entered!</p>
        """
        print(html)
        check2 = False
    else:
        flag1 = False
        flag2 = False
        if len(formData["pwd"].value) < 6:
            flag1 = True
        if countDigits(formData["pwd"].value) < 2:
            flag2 = True

        if flag1 and flag2:  # Password don't include 6 chars & 2 digits
            html = html + """<label for="password">Password:</label>
                        <input type="text" id="password" name="pwd"><br>
                        <p>*Password should include at least 6 characters!</p>
                        <p>*Password should include at least 2 digits!</p>
                        """
            check2 = False
        elif flag1 and not flag2:  # Password doesn't include 6 chars
            html = html + """<label for="password">Password:</label>
            <input type="text" id="password" name="pwd"><br>
            <p>*Password should include at least 6 characters!</p>
            """
            check2 = False
        elif not flag1 and flag2:  # Password doesn't include 2 digits
            html = html + """<label for="password">Password:</label>
            <input type="text" id="password" name="pwd"><br>
            <p>*Password should include at least 2 digits!</p>
            """
            check2 = False
        else:  # Password okay!
            html = html + """<label for="password">Password:</label>
            <input type="text" id="password" name="pwd"><br>
            """
        print(html)

    if "name" not in formData.keys():
        html = html + """<label for="name">Full name:</label>
  		<input type="text" id="name" name="name"><br>
  		<p>*Full name should be entered!</p>
        """
        print(html)
        check3 = False
    else:
        html = html + """<label for="name">Full name:</label>
        <input type="text" id="name" name="name"><br><br>
        """
        print(html)

    if "email" not in formData.keys():
        html = html + """<label for="email">E-mail:</label>
		<input type="text" id="email" name="email"><br>
		<p>*E-mail should be entered!</p>
        """
        print(html)
        check4 = False
    else:
        html = html + """<label for="email">E-mail:</label>
        <input type="text" id="email" name="email"><br><br>
        """
        print(html)

    if "phone" not in formData.keys():
        html = html + """<label for="phone">Phone Number:</label>
		<input type="text" id="phone" name="phone"><br>
		<p>*Phone number should be entered!</p>
        """
        print(html)
        check5 = False
    else:
        html = html + """<label for="phone">Phone Number:</label>
        <input type="text" id="phone" name="phone"><br><br>
        """
        print(html)

    if check1 and check2 and check3 and check4 and check5:
        print(html)
        conn = sqlite3.connect("rent-house.db")
        c = conn.cursor()
        c.execute("SELECT * FROM USER WHERE username = ?", (formData["username"].value,))
        row = c.fetchone()
        print("row = {} ".format(row))
        if row is not None:
            html = html + """<input type="button" value="Go Back!" onclick="history.back()"><br><br>
            </form>
            """
            html = html + """<p>Username is already in use. Please try another username.</p>
            """
            print(html)
        else:
            c.execute("INSERT INTO USER VALUES (?,?,?,?,?,?)", (formData["username"].value, formData["pwd"].value,
                                                                formData["name"].value, formData["email"].value, -1,
                                                                formData["phone"].value))

            html = html + """<input type="submit" value="Register"><br><br>
		    </form>
            <p> Successfully Registered.<p>
            """
            print(html)
            conn.commit()
            conn.close()
            print("<script>")
            print("window.location = 'index.py';")
            print("</script>")
    else:
        html = html + """<input type="button" value="Go Back!" onclick="history.back()"><br><br>
        </form>
        """
    html = html + """</div>
    """
    print(html)


def printFooter():
    html = """
    </body>
    </html>"""
    print(html)


formData = cgi.FieldStorage()

printHeader("Register")
printBodyContent(formData)
printFooter()
