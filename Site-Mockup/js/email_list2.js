const $ = selector => document.querySelector(selector);

document.addEventListener("DOMContentLoaded", () => {
    
    $("#join_list2").addEventListener("click", () => {
        // get values user entered in textboxes
        const email3 = $("#email_3");
        const email4 = $("#email_4");
        const firstName2 = $("#first_name2");
        const lastName2 = $("#last_name2");
        const userName2 = $("#user_name2");
    
        // create a Boolean variable to keep track of invalid entries
        let isValid = true;

        // check user entries - add text to error message if invalid
        if (email3.value == "") {
            email3.nextElementSibling.textContent = "This field is required.";
            isValid = false; 
        } else {
            email3.nextElementSibling.textContent = "";
        }
    
        if (email4.value == "") { 
            email4.nextElementSibling.textContent = "This field is required.";
            isValid = false; 
        } else {
            email4.nextElementSibling.textContent = "";
        }
    
        if (email3.value != email4.value) { 
            email4.nextElementSibling.textContent = "Email addresses must match.";
            isValid = false; 
        }
    
        if (firstName2.value == "") {
            firstName2.nextElementSibling.textContent = "First name is required.";
            isValid = false;
        } else {
            firstName2.nextElementSibling.textContent = "";
        }

        if (lastName2.value == "") {
            lastName2.nextElementSibling.textContent = "Last name is required.";
            isValid = false;
        } else {
            lastName2.nextElementSibling.textContent = "";
        }

        if (userName2.value == "") {
            userName2.nextElementSibling.textContent = "User name is required.";
            isValid = false;
        } else {
            userName2.nextElementSibling.textContent = "";
        }
    
        // submit the form if all entries are valid
        if (isValid) {
            alert("You have Registered on the site!");
        }
    });

    $("#clear_form2").addEventListener("click", () => {
        $("#email_3").value = "";
        $("#email_4").value = "";
        $("#first_name2").value = "";
        $("#last_name2").value = "";
        $("#user_name2").value = "";
        $("#email_3").focus();

    });
    
    $("#email_3").focus();
});