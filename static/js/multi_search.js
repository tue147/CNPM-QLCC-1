  var  tableHead = document.getElementById("dataTable").getElementsByTagName('thead')[0];
  var list_name = tableHead.querySelectorAll('th');
  var finale = "";
  number_column = list_name.length;
  for (let i = 0; i < number_column; i++) {
    finale += `<th> <input id="Filter${i}" placeholder="Filter"> </th>`;
  }
  tableHead.innerHTML += `<tr>${finale} </tr>`;
  for (let i = 0; i < list_name.length; i++) {
    document.getElementById(`Filter${i}`).addEventListener("keyup", function () {
      FilterRemaster();
    });
  }
  function FilterRemaster() {
    var table = document.getElementById("dataTable");
    var tr = table.getElementsByTagName("tr");
    var input = new Array(number_column);
    for (let i = 0; i < number_column; i++) {
      input[i] = document.getElementById(`Filter${i}`).value.toUpperCase();
    }
    var TextValue;
    for (let i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName('td');
      var flag = true;
      for (let j = 0; j < number_column; j++) {
        if (td[j]) {
          if (td[j].querySelector('input')) {
            TextValue = td[j].querySelector('input').value;
          }
          else {
            TextValue = td[j].textContent || td[j].innerText;
          }
          if (TextValue.toUpperCase().indexOf(input[j]) == -1) {
            flag = false;
            break;
          }
        }
      }
      if (flag) {
        tr[i].style.display = "";
      }
      else {
        tr[i].style.display = "none";
      }
    }
  }