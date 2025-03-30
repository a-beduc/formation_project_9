<p align="center">
    <img alt="Logo of the chess application" style="width:70%; height:auto;" src="src/mystatic/images/168805567091_LITrevu banner.png" title="Logo of LITRevu" />
</p>

# LITRevu Django Website - Project 9

Ninth project for the online course of Python application development on 
OpenClassroom.

## Description

This is a Django-based web application created for a fictitious company called 
LITRevu. The application functions as a locally hosted Website where users can 
request and post book reviews. Developed with **Django Framework**, it 
proposes an inscription system, a feed where users you can see what users you
follow posts.

## Features

A non-logged-in visitor can:
* Sign up (create an account)
* Log in to an existing account

A logged-in user can:
* View their feed, which displays the latest posts and reviews from the users 
they follow, in reverse chronological order.
* Create new posts (tickets) to request reviews of a book or an article.
* Create new reviews in response to existing posts.
* Create both a post and its review in a single step.
* View, edit, and delete their own posts and reviews.
* Follow other users by entering their username.
* View the users they follow, and follow anyone they wish.
* Unfollow or block a user.

## Installation & Launch

Ensure you have the following installed on your system:

- [Python 3.7+](https://www.python.org/downloads/)
  - Tested with Python 3.12 should work on Python 3.7+.
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

### Steps to Install

1. Open a terminal and navigate to your desired directory. 
2. Clone the project or download the files to your local machine:

    ```bash
    git clone https://github.com/a-beduc/formation_project_10
    ```
3. Create a virtual environment:

    ```bash
    pipenv shell
    ```

   - ***(Optional)** You can verify if the virtual environment is correctly created with the 
following command which should give you the path of the current virtual 
environment:*
    ```bash
    pipenv --venv
    ```

   - ***(Optional)** You can stop your virtual environment with:*
    ```bash
    exit
    ```
   
    - ***(Optional)** and reactivate it with:*
   ```bash
    pipenv shell
    ```

4. Install dependencies:
    ```bash
    pipenv install
    ```

   - ***(Optional)** For development tools (linters), you can also install dev dependencies:*
    ```bash
    pipenv install --dev
    ```
5. ***(Optional)** If you want a new and clean Database*
   - *Delete the current data*
     - *Delete the db.sqlite3 in the src/ directory*

   - *Apply migrations*
     - *Make sure you are in the project's src/ directory*

         ```bash
         python manage.py migrate
         ```
   - Create an admin user to access the Admin panel. 
   *You can follow the process to create a new superuser with this 
   [w3school tutorial](https://www.w3schools.com/django/django_admin_create_user.php)*

6. Generate a SECRET_KEY:
   * Create a .env file at the root of the project (not in /src) by copying the content .env.example 
   * Go to https://djecrety.ir/ to generate a Django SECRET_KEY 
   * Paste the generated key as a string in the .env
   * It should look like : SECRET_KEY='your_unique_generated_secret_key'

7. Navigate to the src directory and start the server:

    ```bash
    python manage.py runserver
    ``` 
8. Access the application:
    
    With a web browser:
    ```
    http://127.0.0.1:8000
    ```

### Site Administration

Access the admin panel: http://127.0.0.1:8000/admin
    
   ```
   default admin credentials:
   username: admin
   password: 53CR37!4dm1n
   ```

### Test Users
   ```
   username: user_one     | password: 53CR37!U53R
   username: user_two     | password: 53CR37!U53R
   username: user_thr     | password: 53CR37!U53R
   ```
