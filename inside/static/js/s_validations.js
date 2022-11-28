//F12 Restrict
document.onkeypress = function (event) {
    event = (event || window.event);
    if (event.keyCode == 123) {
        return false;
    }
}
document.onmousedown = function (event) {
    event = (event || window.event);
    if (event.keyCode == 123) {
        return false;
    }
}
document.onkeydown = function (event) {
    event = (event || window.event);
    if (event.keyCode == 123) {
        return false;
    }
}
//F12 Restrict

//For number like "123.53" (Accepts 0-9 .)
function AcceptDecimal(txtvalue) {
    var e = event || evt; // for trans-browser compatibility
    var charCode = e.which || e.keyCode;
    if (!(document.getElementById(txtvalue.id).value)) {
        if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
        return true;
    }
    else {
        var val = document.getElementById(txtvalue.id).value;
        if (charCode == 46 || (charCode > 31 && (charCode > 47 && charCode < 58))) {
            var points = 0;
            points = val.indexOf(".", points);
            if (points >= 1 && charCode == 46) {
                return false;
            }
            if (val.indexOf(".") != -1) {
                var lastdigits = val.substring(val.indexOf(".") + 1, val.length);
                if (lastdigits.length > 1) {
                    alert("Only Two decimal places allowed");
                    return false;
                }
            }
            return true;
        }
        else {
            alert("Only Numerics allowed");
            return false;
        }
    }
}


//For number like "123.5, 45" (Accepts 0-9 .)
function AcceptDecimalForQuantity(txtvalue) {

    var e = event || evt; // for trans-browser compatibility
    var charCode = e.which || e.keyCode;
    if (!(document.getElementById(txtvalue.id).value)) {
        if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
        return true;
    }
    else {
        var val = document.getElementById(txtvalue.id).value;

        if (charCode == 46 || (charCode > 31 && (charCode > 47 && charCode < 58))) {
            var points = 0;
            points = val.indexOf(".", points);
            if (points >= 1 && charCode == 46) {
                return false;
            }
            if (val.indexOf(".") != -1) {

                var lastdigits = val.substring(val.indexOf(".") + 1, val.length);
                if (lastdigits.length == 0) {
                    if (charCode != 53) {
                        alert("Enter Quantity like Ex : 12 , 10.5 ");
                        return false;
                    }
                }
                if (lastdigits.length > 0) {
                    alert("Only one decimal place allowed");
                    return false;
                }
            }
            return true;
        }
        else {
            alert("Only Numerics allowed");
            return false;
        }
    }
}

//For only numbers like "12352" (Accepts 0-9)
function AcceptNumerics(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode

    if (charCode >= 48 && charCode <= 57) {
        return true;
    }
    alert('Please enter Numerics only!');
    return false;
}


//For only Alphabets like "12352" (Accepts A-Z  a-z  space)
function AcceptAlphabets(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode

    if ((charCode >= 65 && charCode <= 90) || (charCode >= 97 && charCode <= 122) || charCode == 32) {
        return true;
    }
    alert('Please enter Alphabets only!');
    return false;
}


//For Alphabets and Numbers like  "k varma 13kumar" (Accepts A-Z a-z  / 0-9 space)
function AcceptAlphaNumeric(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode


    if ((charCode >= 65 && charCode <= 90) || (charCode >= 97 && charCode <= 122) || (charCode >= 47 && charCode <= 57) || charCode == 32) {
        return true;
    }
    alert('Please enter Alphabets & Numbers only!');
    return false;
}


//For Providing "Are you sure you want to Proceed"
function ClickRegister() {

    var flag = Page_ClientValidate('Register');
    if (flag)
    {
        var confirmmessage = "Are you sure you want to Proceed?";
        if (confirm(confirmmessage))
        {
        return true;
        }
        else
        {
        return false;
        }
    }
    else
     {
        //var lbl = document.getElementById("<%=lblfileUploadStatus.ClientID%>");
        //Text="Please Upload File"
     }
}


//For Showing URL of selected file, OnMouseHover of Browse button
function DisplayUploadControlURL(control) {
    control.title = control.value;
}













function ValidMobileNum() {
    var regmobNo = /^(\d)(?!\1+$)\d*$/;
    var mobno = document.getElementById('<%=txtmobile1.ClientID %>').value;
    if (!regmobNo.test(mobno)) {
        alert('Please enter valid Mobile Number');

        document.getElementById('<%=txtmobile1.ClientID %>').value = "";
        return false;
    }
}





function AcceptDigitsTons(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode

    if ((charCode >= 48 && charCode <= 57) || charCode == 190 || charCode == 46) {
        return true;
    }
    alert('Please enter Numerics only!');
    return false;
}


function AcceptDigits_Dot(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode

    if (charCode >= 48 && charCode <= 57 || charCode == 46) {
        return true;
    }
    alert('Please enter Numerics only!');
    return false;
}


function AcceptDigitsDecimals(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode

    if (charCode >= 48 && charCode <= 57 || charCode == 46) {
        return true;
    }
    alert('Please enter Numerics only!');
    return false;
}

function AllowSlashAlphaNumeric(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode

    if ((charCode >= 65 && charCode <= 90) || (charCode >= 97 && charCode <= 122) || (charCode >= 47 && charCode <= 57) || charCode == 45) {
        return true;
    }
    alert('Please enter Alphabets & Numbers only!');
    return false;
}




//function IsNumeric(evt)
//{
// var c = (evt.which) ? evt.which : event.keyCode
// if ((c >= '0'  && c <= '9') || c == ',' )
// {
//    return true;
//  }
//  alert('Please enter Numerics and (,) only!');
// return false;
//}


function AcceptDate(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode

    if (charCode >= 47 && charCode <= 57) {
        return true;
    }
    alert('Please enter Date only!');
    return false;
}

function numericValidationForQty(txtvalue) {
    var e = event || evt; // for trans-browser compatibility
    var charCode = e.which || e.keyCode;
    // if(document.getElementById('<%=txtQty.ClientID%>').value=="0")
    if (document.getElementById('<%=txtQty.ClientID%>').value == "0") {
        return false;
    }




    if (!(document.getElementById(txtvalue.id).value)) {
        if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
        return true;
    }
    else {
        var val = document.getElementById(txtvalue.id).value;
        if (charCode == 46 || (charCode > 31 && (charCode > 47 && charCode < 58))) {
            var points = 0;
            points = val.indexOf(".", points);
            if (points >= 1 && charCode == 46) {
                return false;
            }
            if (points >= 1) {
                var lastdigits = val.substring(val.indexOf(".") + 1, val.length);
                if (lastdigits.length >= 2) {
                    alert("Two Decimal places only allowed");
                    return false;
                }
            }
            return true;
        }
        else {
            alert("Only Numarics allowed");
            return false;
        }
    }
}



//function PreventAllKeys(e) {


//    var evt = e || window.event;
//    if (evt) {
//        var keyCode = evt.charCode || evt.keyCode;
//        if (keyCode === 8 || keyCode !=  {
//            if (evt.preventDefault) {
//                evt.preventDefault();

//            } else {
//                evt.returnValue = false;
//            }
//        }
//    }
//}
//     //Below code will disable mouse drag to select
var unFocus = function () {
    if (document.selection) {
        document.selection.empty()
    } else {
        window.getSelection().removeAllRanges()
    }

}