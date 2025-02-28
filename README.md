# ComSciCurriculumProject

## This repository creates for senior project Integrated Agile Process and Devops_01418472-65.

This project is about checking the criteria of students to confirm graduation. The check will include 
1. academic transcripts
2. academic debt payment forms 
3. graduation applications
4. activity sheets (optional).

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
3. `pip install -r requirement.txt`
4. `cp .env.example backend/.env`
5. `python backend/manage.py makemigrations`
6. `python backend/manage.py migrate`

### run server
1. `python backend/manage.py runserver`

### deactivate backend program
1. `docker compose down`
2. `deactivate` in terminal using virtual environment