# Building an Online Delivery Parcel Management System Web Application with Flask and MySQL

_By Vaibhav Gupta_

---

## Introduction

The objective of this project is to develop a delivery parcel management system that tracks and manages
parcels from reception to delivery using dummy data. The system will enable users to add, update, track,
and report on parcel status and provide real-time updates on long-running tasks, such as bulk parcel
processing

---

## Project Details

- **Project Name:** Delivery Parcel Management System
- **Purpose:** Develop a fully functional Delivery Parcel Management System
- **Developed By:** Vaibhav Gupta (Full Stack Developer)

---

## Setting Up the Project

1. Creating a Virtual Environment
   Navigate into the "Project" directory and create a virtual environment for the project. Run the following commands:

```bash
$ cd FreshBasket
$ python3 -m venv venv
$  venv/Scripts/activate.bat
```

This will create a new virtual environment and activate it.

3. Installing Dependencies

With the virtual environment activated, let’s install the required dependencies. Run the following command:

```bash
$ pip install -r requirements.txt
```

This will install all the necessary packages specified in the "requirements.txt" file.

4. Configuring the Database

The "Delivery Parcel Management System" project uses MySQL as the database. Before running the application, you need to set up a MySQL database and configure the project to use it.

a. **Creating a MySQL Database**

Open your preferred MySQL client and create a new database for the project. You can use the following SQL command:

```sql
CREATE DATABASE parcel_management;
```

a. **Creating a Admin User**

After setting up the database and tables it is suggested to add a Admin User to the user table. You can use the following SQL command:

```sql
use DATABASE parcel_management;
INSERT INTO user('username', 'password') VALUES('sender_name', 'receiver_name');
```

c. **Configuring the Database Connection**

In the project directory, open the "config.py" file. Update the values of the following variables with your MySQL database credentials:

```sql
    SQLALCHEMY_DATABASE_URI = 'localhost'
 SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
 SECRET_KEY = 'your_secret_key'
 SESSION_TYPE = 'filesystem'
```

Save the changes.

5. Running the Application

To start the Delivery Parcel Management System web application, run the following command:

```bash
$ python app.py
```

---

This will launch the application, and you can access it by opening your web browser and entering the URL `http://localhost:5000`.
