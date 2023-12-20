document.getElementById('householdForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        idHo: document.getElementById('idHo').value,
        chuHo: document.getElementById('chuHo').value,
        idTaiKhoan: document.getElementById('idTaiKhoan').value,
        soPhong: document.getElementById('soPhong').value,
        loaiPhong: document.getElementById('loaiPhong').value
    };
    console.log(formData); // Replace with an API call to submit the form data
    fetch('/api/NK/add/apply', { method: 'POST', body: JSON.stringify(formData) })
});