<?php
$servername = "localhost";
$username = "root";  // Update this with your database username
$password = "";  // Update this with your database password
$dbname = "mental_health_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $age = $_POST['age'];
    $gender = $_POST['gender'];
    $location = $_POST['location'];
    $occupation = $_POST['occupation'];
    $medical_history = $_POST['medical_history'];
    $sleep_duration = $_POST['sleep_duration'];
    $stress_level = $_POST['stress_level'];
    $mood = $_POST['mood'];
    $activity = $_POST['activity'];
    $social_interaction = $_POST['social_interaction'];
    $hobbies = $_POST['hobbies'];

    // Prepare and bind
    $stmt = $conn->prepare("INSERT INTO tracker (age, gender, location, occupation, medical_history, sleep_duration, stress_level, mood, activity, social_interaction, hobbies) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("issssiiisss", $age, $gender, $location, $occupation, $medical_history, $sleep_duration, $stress_level, $mood, $activity, $social_interaction, $hobbies);

    // Execute the statement
    if ($stmt->execute()) {
        echo "New record created successfully";
    } else {
        echo "Error: " . $stmt->error;
    }

    // Close statement and connection
    $stmt->close();
    $conn->close();
}
?>
