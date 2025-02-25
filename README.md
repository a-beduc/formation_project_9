# LITRevu Django Website - Project 9

Ninth project for the online course of Python application development on OpenClassroom.

<p align="center">
    <img alt="Logo of the chess application" style="width:70%; height:auto;" src="mystatic/images/168805567091_LITrevu banner.png" title="Logo of LITRevu" />
</p>

## Description

This is a Django-based web application created for a fictitious company called LITRevu. The application functions as a social network where users can request and post book reviews.

## Features

A non-logged-in visitor can:
* Sign up (create an account)
* Log in to an existing account

A logged-in user can:
* View their feed, which displays the latest posts and reviews from the users they follow, in reverse chronological order.
* Create new posts (tickets) to request reviews of a book or an article.
* Create new reviews in response to existing posts.
* Create both a post and its review in a single step.
* View, edit, and delete their own posts and reviews.
* Follow other users by entering their username.
* View the users they follow, and follow anyone they wish.
* Unfollow or block a user.

## Installation & Launch

Ensure you have the following installed on your system:

- [Python 3.x](https://www.python.org/downloads/)

### Steps to Install

1. Clone the project or download the files to your local machine:

    ```bash
    git clone https://github.com/a-beduc/formation_project_9
    ```
2. Open a terminal and navigate to the project directory.
3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
   
        ```bash
        cd venv/Scripts
        activate
        cd ../..
        ```
    - On macOS/Linux:
   
        ```bash
        source venv/bin/activate
        ```
5. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```
6. (Optional) If you want a new Database, 
   - Delete the current data
     - Delete the db.sqlite3 in the root directory
     - Delete the files found in /media

   - Apply migrations
     - Make sure you are in the project's root directory

         ```bash
         python manage.py migrate
         ```
   
   - Create an admin user to access the Admin panel.
       ```bash
       python manage.py createsuperuser
     
       Username: <Your choice>
       Emailaddress: example@gmail.com
       Password: ******
       Password(again): ******
       ```

7. Generate a SECRET_KEY:
   * Create a .env file at the root of the project by copying the content .env.example 
   * Go to https://djecrety.ir/ to generate a Django SECRET_KEY 
   * Paste the generated key as a string in the .env
   * It should look like : SECRET_KEY='your_unique_generated_secret_key'


8. Run the server:

    ```bash
    python manage.py runserver
    ``` 
8. Access the application:

    ```bash
    http://127.0.0.1:8000
    ```

### Site Administration

Access the admin panel:
    ```bash
    http://127.0.0.1:8000/admin
   
    default admin credentials:
    username: admin
    password: admin
    ```

### Test Users
    ```bash
    username: alex     | password: bateau1234
    username: mat      | password: bateau1234
    username: mike     | password: bateau1234
    ```
