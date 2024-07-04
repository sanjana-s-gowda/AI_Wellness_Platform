<?php
$servername = "localhost"; // Change if your database server is different
$username = "root"; // Replace with your MySQL username
$password = ""; // Replace with your MySQL password
$dbname = "medical_al_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'];
    $age = $_POST['age'];
    $height = $_POST['height'];
    $country = $_POST['country'];
    $health_goals = $_POST['health-goals'];
    $weight = $_POST['weight'];
    $ailments = $_POST['ailments'];
    $preference = $_POST['preference'];

    $sql = "INSERT INTO users (name, age, height, country, health_goals, weight, ailments, preference)
            VALUES ('$name', $age, $height, '$country', '$health_goals', $weight, '$ailments', '$preference')";

    if ($conn->query($sql) === TRUE) {
        echo "New record created successfully";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

$conn->close();
?>
