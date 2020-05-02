# MyRailway

---
Title: "Railway Management System"
Author: "Vraj Mistry & Ekansh Verma"
Date: "22 October 2016"
---

## Project Structure
        . refers to Project Directory i.e. current working directory
    
        1. ./railway/views.py : Contains important methods which return HttpResponse object
    
        2. ./Project/urls.py : Map url to methods in views
    
        3. ./static : Css and Images
    
        4. ./templates : HTML pages
    
        5. ./Project/settings.py: Store database details, template path, static path.

## Create database, create and populate tables
1) Open ubuntu command prompt
2) Start mysql as `mysql -u <your_user> -p`
3) Create database `manage_rail` as `create database manage_rail;`
4) Select database as `use manage_rail;`
5) Use `commands.sql` file in the main repository to create and populate tables. Run `source <path>/MyRailway/commands.sql`

## How to start server?
Go to the Project_1 directory and run ``python manage.py runserver``

## Go to home page
After starting the server go to the ``https://127.0.0.1:8001/home`` i.e. homepage of the website.

## Facilities provided to the end user

  In order to do something you must have an account. So you can **signup** if you don't have one and you are good to go.
  Now you have an account so after successful **login** you can
  
  1. know about trains: **User** need to provide **train number** as **input**. If train number is valid then train information will be displayed to the user such as **seats availability**, whether **food** is available or not, on **which day** of the week it runs, **train route**, **arrival time** and **departure time** and much more.
  
  2. find trains between stations: Provide two **station codes** and you will get to know all trains passes through both the specified stations. Both station codes must be different.
  
  3. book a ticket: Booking a ticket is very simple. You just need to fill a form correctly. You will have to provide **train number**, **first name**, **last name**, select **gender** from drop down menu, **age**, select **class(sleeper, 1 AC, 2 AC, 3 AC)** from drop down menu and **phone number**.
          
## Other facilities
  1. HTML pages are linked for better user experience.
      
