
# Movie Library

A web application that allows users to manage a collection of movies. Also one of my first project in school that make me really proud the most so feel free to use or contribute to it :3
## Description
- It is built using Flask, a Python web framework, and utilizes Flask-Login for user authentication. 
- The application supports operations such as adding and deleting movies from a user's collection. 
- Using OMDbAPI to fetch data so you would need to collect your own API key in order to work.
- Project comes with a password reset feature for users that forget their password. You require to modify the application's SMTP configuration.

## Register and Login
![Register](https://github.com/user-attachments/assets/bab3496d-e321-49cc-8f92-7720feedf079)

## Add and Remove
![Add and remove](https://github.com/user-attachments/assets/7b1c1596-2ef8-415f-b4e3-1679460237bb)

## Search
![Search](https://github.com/user-attachments/assets/18b59ea5-c1ff-48cf-b283-f3df01189f97)

## Setup, Installation and Run Locally

Clone the project

```bash
  git clone https://github.com/ShermanTreeDev/Movie-Library.git
```

Go to the project directory

```bash
  cd Movie-Library
```

Create virtual environment

```bash
  python3 -m venv env
```

Run virtual environment

```bash
    source env/bin/activate
    env\Scripts\activate (Microsoft Windows cmd)
    env\Scripts\Activate.ps1 or env/Scritps/activate (Powershell)
```

Install my-project with npm

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  flask run
```

## Database Migration
For any detail, follow this structure https://github.com/miguelgrinberg/flask-migrate

Next you will need to put your own API and email variable. Good luck :3
