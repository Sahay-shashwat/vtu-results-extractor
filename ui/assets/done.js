function createTable()
{
    let table = document.getElementById('skipped');
    len = localStorage.getItem("len");
    toastr["success"]("", `${len} USN's were successful!`);
    data = localStorage.getItem("skipped").split(",");
    for (var i = 0; i < data.length; i++)
    {
        let tr = document.createElement('tr');

        let td = document.createElement('td');
        td.textContent = data[i];
        tr.appendChild(td);
        table.appendChild(tr);
    }
}

function back()
{
    window.location.replace('index.html');
}