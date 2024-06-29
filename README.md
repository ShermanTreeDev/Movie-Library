
# Movie Library

A web application that allows users to manage a collection of movies. Also one of my first project in school that make me really proud the most so feel free to use or contribute to it :3
## Description
- It is built using Flask, a Python web framework, and utilizes Flask-Login for user authentication. 
- The application supports operations such as adding and deleting movies from a user's collection. 
- Using OMDbAPI to fetch data so you would need to collect your own API key in order to work.
- Project comes with a password reset feature for users that forget their password. You require to modify the application's SMTP configuration.

## Register and Login
![Register and Login](https://github.com/CallMeTree/Movie-Library/assets/101957534/116338ee-f2b7-4e1c-a585-7dcfcb824062)

## Add and Remove
![Add and Remove](https://github.com/CallMeTree/Movie-Library/assets/101957534/cc0dfcf0-df1a-4044-9489-369bda7068a3)


## Search
![Search](https://github.com/CallMeTree/Movie-Library/assets/101957534/1cf27aa9-8c8e-4192-a8dd-de861055ebf1)

    
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

Install my-project with npm

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  flask run
```

Next you will need to put your own API and email variable. Good luck :3