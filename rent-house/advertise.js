function validateForm(){
    var street = document.forms["myForm"]["street"].value;
	var noOfBedrooms = document.forms["myForm"]["noOfBedrooms"].value;
    var monthlyFee = document.forms["myForm"]["monthlyFee"].value;
    var errorCount = 0;
    if (street == "") {
		document.getElementById('street_error').innerHTML = '*Street must be filled out!'
		errorCount++;
	}
	if (noOfBedrooms == "") {
		document.getElementById('noOfBedrooms_error').innerHTML = '*Number of bedrooms must be filled out!'
		errorCount++;
	}
    if (monthlyFee == "") {
		document.getElementById('monthlyFee_error').innerHTML = '*Monthly fee must be filled out!'
		errorCount++;
	}
    if (errorCount > 0){
		return false;
	}
	else{
		return true;
	}

}