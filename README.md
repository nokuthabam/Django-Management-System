# Django-Management-System
## Project Description
A dynamic web application that should allow students to view course and subject material, instructors to view their specific subject material, set assignments and grades for students registered for their subject, and admin users to manage, students, instructors, courses and subjects.

## Documentation
The project Documentation can be found in the [Wiki](https://github.com/nokuthabam/Django-Management-System/wiki)!

## Project Structure

The project is organized into the following directories:

- `student_management/`: Contains Django project settings and configurations.
- `management_app/`: The Django app for the management system.
- `static/`: Houses static files such as CSS, JavaScript, and images.

## Application Installation
To run this project on your local system, follow these steps:

1. Clone the repository from GitHub:
   ```bash
   git clone https://github.com/nokuthabam/Django-Management-System.git

2. Install project dependencies:
   - pip install -r requirements.txt

3. Installing Django and creating virtual environment:
   - mkvirtualenv my_django
   - workon my_django
   -  pip install django


3. Navigate to the project directory:
   - cd Django-Management-System

3. Apply database migrations:
   - python manage.py migrate

4. Create a superuser to manage the Django admin panel:
   - python manage.py createsuperuser

5. Start the development server:
   - python manage.py runserver

6. Access the website at http://127.0.0.1:8000/


## Usage
    - Visit http://127.0.0.1:8000/ to access the login page
   - Click register as an admin user in order to be able to manage the database tables.
   - Once logged i as the admin, you can navigate through the website's various pages.

## Continuous Integration: CircleCI Badge
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/nokuthabam/Django-Management-System/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/nokuthabam/Django-Management-System/tree/main)

## Code Coverage: CodeCov Badge

## Project Author
Nokuthaba Moyo

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for more information.