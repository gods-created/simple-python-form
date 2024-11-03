const button = $("#button");
const fname = $("#fname");
const lname = $("#lname");
const email = $("#email");
const api_link = "http://0.0.0.0:8001/form";

function validation() {
    if (fname.val().trim().length > 0 && lname.val().trim().length > 0 && validator.isEmail(email.val())) {
        button.prop("disabled", false);
    } else {
        button.prop("disabled", true);
    }
}

async function send_form(e) {
    e.preventDefault();
    let fname_value = fname.val();
    let lname_value = lname.val();
    let email_value = email.val();
    
    const form = {
        fname: fname_value,
        lname: lname_value,
        email: email_value
    }
    
    try {
        const request = await axios.post(api_link, form);
        const { status, description } = request.data;
        alert(description)
    } catch (error) {
        alert(error.message);
    }
    
    return;
}

$(document).ready(() => {
    fname.on("input", validation);
    lname.on("input", validation);
    email.on("input", validation);
    
    button.on("click", async (e) => { await send_form(e) })
});
