# MyRailway

---
Title: "Railway Management System"
Author: "Vraj Mistry & Ekansh Verma"
Date: "26 June 2020"
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
3) Create database `raildb` as `create database raildb;`
4) Select database as `use raildb;`
5) Use `commandlist.sql` file in the main repository to create and populate tables. Run `source <path>/MyRailway/commandlist.sql`

## How to start server?
Go to the TestSite directory and run ``python manage.py runserver``

## Go to home page
After starting the server go to the ``https://127.0.0.1:8000`` i.e. homepage of the website.

