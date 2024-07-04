<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "medical_app_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $login_username = $_POST['login-username'];
    $login_password = $_POST['login-password'];

    $sql = "SELECT * FROM users WHERE username='$login_username' OR email='$login_username'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if (password_verify($login_password, $row['password'])) {
            echo "Login successful";
        } else {
            echo "Invalid password";
        }
    } else {
        echo "No user found with that username or email";
    }
}

$conn->close();
?>
