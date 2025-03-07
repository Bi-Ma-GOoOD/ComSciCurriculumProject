# ComSciCurriculumProject

## This repository creates for senior project Integrated Agile Process and Devops_01418472-65.

This project is about checking the criteria of students to confirm graduation. The check will include 
1. academic transcripts
2. academic debt payment forms 
3. graduation applications
4. activity sheets (optional).

# How to activate frontend
To activate frontend run the following command
> suggest using git bash
1. `cd frontend/`
2. `npm install`
3. `npm run dev`

# How to activate backend

To activate backend run the following command 
> suggest using git bash

### run server database using docker
1. `docker-compose up -d`
> suggest using seperate terminal

### inspect direct to the database
1. `docker exec -it cs_curriculum bin/bash`
2. `mysql -uroot -p1234`
3. `use cs_curriculum`
4. now you can access directly to the database

### access database via phpmyadmin
1. Go to `http://127.0.0.1:8080/`
    - username : root
    - password : 1234

### setup environment
1. `python -m venv .venv`
2. __activate virtual environment__ -> `source .venv/Scripts/activate`
3. `cd ./backend`
4. `pip install -r requirement.txt`
5. `cp .env.example backend/.env`
6. `python backend/manage.py makemigrations`
7. `python backend/manage.py migrate`

### run server
1. `python backend/manage.py runserver`

### deactivate backend program
1. `docker compose down`
2. `deactivate` in terminal using virtual environment

### email for sending OTP code
1. `EMAIL_HOST_USER = 'xxxxxxxxxx@gmail.com'` change the email
2. `EMAIL_HOST_PASSWORD = 'xxxxxxxxxxxxxxxx'` change the app password (get the app password from google account)

### how to do unit testing
1. `cd backend`
2. `pytest -sv`

> `-s` flag is to show console printing </br>
> `-v` flag is to show detail
