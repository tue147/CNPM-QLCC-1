document.getElementById('paymentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        stt: document.getElementById('stt').value,
        idDichVu: document.getElementById('idDichVu').value,
        idHo: document.getElementById('idHo').value,
        soLuong: document.getElementById('soLuong').value,
        giaTien: document.getElementById('giaTien').value,
        daThu: document.getElementById('daThu').value,
        ngayThu: document.getElementById('ngayThu').value
    };
    console.log(formData); // Replace with an API call to submit the form data
    fetch('/api/TC/add/apply', { method: 'POST', body: JSON.stringify(formData) })
});