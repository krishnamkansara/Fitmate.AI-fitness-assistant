<?php
// Establish database connection
$con = new mysqli("localhost", "root", "", "database");

// Check if the connection was successful
if ($con->connect_error) {
    die("Connection failed: " . $con->connect_error);
}

// Check if the form data is set
if (isset($_POST['email']) && isset($_POST['password'])) {
    // Sanitize and escape form inputs
    $email = mysqli_real_escape_string($con, $_POST['email']);
    $password = mysqli_real_escape_string($con, $_POST['password']);

    // Prepare SQL statement
    $sql = "SELECT * FROM signup WHERE email=? AND password=?";
    $result = mysqli_prepare($con, $sql);

    // Check if the statement was prepared successfully
    if ($result === false) {
        die("Error: " . mysqli_error($con));
    }

    // Bind parameters
    mysqli_stmt_bind_param($result, "ss", $email, $password);

    // Execute the statement
    $check = mysqli_stmt_execute($result);

    // Check if the statement was executed successfully
    if ($check) {
        // Check if a row was returned
        mysqli_stmt_store_result($result);
        if (mysqli_stmt_num_rows($result) > 0) {
            echo "Login successful";
            // Redirect to a logged-in page or perform other actions
        } else {
            echo "Invalid email or password";
        }
    } else {
        die("Error: " . mysqli_error($con));
    }
} else {
    echo "Error: Required form fields not set.";
}

// Close the database connection
mysqli_close($con);
?>
