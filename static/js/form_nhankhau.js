document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        cccd: document.getElementById('cccd').value,
        hoTen: document.getElementById('hoTen').value,
        ngaySinh: document.getElementById('ngaySinh').value,
        quanHe: document.getElementById('quanHe').value,
        tinhTrangCuTru: document.getElementById('tinhTrangCuTru').value,
    };
    console.log(formData); // Replace with an API call to submit the form data
    // Example: fetch('your-api-endpoint', { method: 'POST', body: JSON.stringify(formData) })
});
