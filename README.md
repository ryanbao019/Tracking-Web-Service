# Tracking-Web-Service
This is a web application for SecureSoftware course Final Project

Log Oct 18, 2024 - Group Meeting at Hub Center room 482
Site Map for Web application,
1.About Page
1.1Introduction
1.2Contact
1.3Home Service
1.3.1Map
1.3.2Show the Map Information
2.Sign Up
2.1User Name
2.2Password
2.3Email
2.4Home Location
3.Login
3.1Report Personal COVID Information
3.1.1Location in the past three days after diagnosis
3.1.2Check Self Affect Chance History
3.1.3Provide the past three days' location
3.2Allow to Locate
3.2.1Create the safest travel route back home or to the nearest hotel




# AspNetCore.Diagnostics.HealthChecks

This is an online web application developed using the Django framework. It is built with Python and MySQL. Follow the steps below to configure and run the app on your system.

Prerequisites
Python
Django
MySQL
mysqlclient Python package
Setup Instructions
1. Build and Configure the Database
Install MySQL and the mysqlclient Python package.
Create a MySQL database for the app.
2. Install Dependencies
Install Python and Django on your system.
Install any required Django extensions.
3. Prepare for Migrations
Remove the default migration files with the following commands:

rm loginapp/migrations/0*.py

rm service/migrations/0*.py

4. Update Database Configuration
Update the DATABASES section in the settings.py file with your MySQL database details to link the app to your database.

5. Create Fresh Migrations
Run the following commands to create fresh migrations:

python3 manage.py makemigrations loginapp

python3 manage.py makemigrations service

6. Apply Migrations in Order
Apply the migrations in the specified order:

python3 manage.py migrate contenttypes

python3 manage.py migrate auth

python3 manage.py migrate admin

python3 manage.py migrate sessions

python3 manage.py migrate loginapp

python3 manage.py migrate service


7. Run the Server
Start the server using the following command:

python3 manage.py runserver_plus --cert-file certificate.crt --key-file private.key

## Success
Once the steps are complete, the web app should be successfully configured and running on your system. Enjoy exploring the Web-Map Searching App!

## License
This project is licensed under [Your License]. Replace with the applicable license details.
