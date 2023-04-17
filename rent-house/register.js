function validateForm() {
	var username = document.forms["myForm"]["username"].value;
	var password = document.forms["myForm"]["password"].value;
	var name = document.forms["myForm"]["name"].value;
	var email = document.forms["myForm"]["email"].value;
	var phone = document.forms["myForm"]["phone"].value;
	var errorCount = 0;
	var flag1 = 0, flag2 = 0;
	if (username == "") {
		document.getElementById('username_error').innerHTML = '*Username must be filled out!'
		errorCount++;
	}
	if (password == "") {
		document.getElementById('password_error').innerHTML = '*Password must be filled out!'
		errorCount++;
	}
	else {
		if (password.length < 6){
			flag1 = 1;
			errorCount++;
			document.getElementById('password_error').innerHTML = '*Password should include at least 6 characters!'
		}
		if (password.replace(/[^0-9]/g,"").length < 2){
			flag1 = 1;
			errorCount++;
			document.getElementById('password_error').innerHTML = '*Password should include at least 2 digits!'
		}
	}
	if (name == "") {
		document.getElementById('name_error').innerHTML = '*Full name must be filled out!'
		errorCount++;
	}
	if (email == "") {
		document.getElementById('email_error').innerHTML = '*E-mail field must be filled out!'
		errorCount++;
	}
	if (phone == "") {
		document.getElementById('phone_error').innerHTML = '*Phone number must be filled out!'
		errorCount++;
	}
	if (errorCount > 0){
		return false;
	}
	else{
		return true;
	}
}
