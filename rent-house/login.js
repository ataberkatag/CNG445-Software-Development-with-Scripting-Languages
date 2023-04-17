function ValidationForm(){
	var username = document.forms["LoginForm"]["username"].value;
	var password = document.forms["LoginForm"]["password"].value;
    var errorCount = 0;
    if (username == "") {
		document.getElementById('username_error').innerHTML = '*Username must be filled out!'
		errorCount++;
	}
	if (password == "") {
		document.getElementById('password_error').innerHTML = '*Password must be filled out!'
		errorCount++;
	}
    if (errorCount > 0){
		return false;
	}
	else{
		return true;
	}
}