-- Create the users table to store user credentials
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL
);

-- Create the prescriptions table to store user prescriptions
CREATE TABLE prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(50) NOT NULL,
    name VARCHAR(100),
    text TEXT,
    FOREIGN KEY (user) REFERENCES users(username)
);
