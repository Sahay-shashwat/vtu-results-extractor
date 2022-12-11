/*
* Main JS file
* Core JS functions for UI
* @author: Rijuth Menon
* @copyright: https://rijuthmenon.me
*/

// For Toastr
toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": true,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "900",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1500",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

function extract()
{
    var resultLink = document.getElementById('link').value;
    var usn = document.getElementById('usn').value;

    if (!/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/.test(resultLink))
    {
        toastr["error"]("", "Please enter a valid link!");
    }
    else if (!/^\w+(,\w+)*$/.test(usn))
    {
        toastr["error"]("", "Please enter valid USN's!");
    }
    else
    {
        eel.extract(usn, resultLink)(function (ret)
        {
            console.log(ret);
            if (ret.status)
            {
                toastr["success"]("", `${ret.len} USN's extracted!`);
            }
            else
            {
                toastr["error"]("", "Error occured while extracting!");
            }
        });
    }

}

function generate()
{
    var usn = document.getElementById('usn').value;
    if (!/^\w+(,\w+)*$/.test(usn))
    {
        toastr["error"]("", "Please enter valid USN's!");
    }
    else
    {
        eel.main(usn, resultLink)(function (ret)
        {
            alert(ret);
        });
    }
}