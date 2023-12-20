// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Reference to the form element
    var form = document.getElementById('accountForm');
    // Event listener for form submission
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission
        // Your custom logic for handling the form submission goes here
        // For example, you can log the form data to the console
        console.log('Form submitted!');
        console.log('ID Tài Khoản:', document.getElementById('idTaiKhoan').value);
        console.log('Tên Đăng Nhập:', document.getElementById('tenDangNhap').value);
        console.log('Mật Khẩu:', document.getElementById('matKhau').value);
        console.log('Admin: Xác nhận', document.getElementById('admin').checked);
    });
});
