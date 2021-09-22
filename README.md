![flask](https://img.shields.io/badge/Flask-v2.0.1-blue.svg?&logo=flask&color=success)
![python](https://img.shields.io/badge/python-v3.9-blue.svg?&logo=python&logoColor=yellow)
![GitHub repo size](https://img.shields.io/github/repo-size/twibster/IEEE-ZSB?color=red&logo=github)
![Lines of code](https://img.shields.io/tokei/lines/github/twibster/IEEE-ZSB?color=blueviolet)

# IEEE-ZSB

IEEE-ZSB is a **web platform** designed to manage 
task creation, submission and excuses for the team members.\
It also provides the team with the ability to organize meetings and announce news.\
The platform is equipped with a notification system and e-mail services with wide variety of options for the users.

## Online version
Visit **[IEEE-ZSB](https://twibster.pythonanywhere.com)** to see an online running version of the platform

[//]: <> (## Features)
[//]: <> (* User registration and login )
[//]: <> (* Task creation, modification and deletion)
[//]: <> (* User excuses and submissions for tasks)
[//]: <> (* Organizing meetings with location)
[//]: <> (* Announcing News for the team members)
[//]: <> (* Notification system with full user control over the settings)
[//]: <> (* Account deletion and modification)

## Installation

Use the package manager **[pip](https://pip.pypa.io/en/stable/)** to install the required packages to run the application.

```bash
git clone https://github.com/twibster/IEEE-ZSB.git
cd IEEE-ZSB
pip install -r requirements.txt
```
<details>
  <summary>Directory structure</summary>
  
  ```
    IEEE-ZSB/
    ├── Procfile
    ├── README.md
    ├── requirements.txt
    ├── reset.py
    ├── run.py
    ├── wsgi.py
    └── website/
        ├── __init__.py
        ├── email_config.py
        ├── forms.py
        ├── functions.py
        ├── models.py
        ├── routes.py
        ├── static/
        │   ├── img/
        │   │   ├── favicon.png
        │   │   └── logo2.png
        │   ├── main.css
        │   ├── profile_pics/
        │   │   └── default.jpg
        │   └── scripts/
        │       ├── force_modal.js
        │       ├── force_modal_review.js
        │       ├── map.js
        │       ├── navbar.js
        │       ├── new_meetup.js
        │       ├── popovers.js
        │       ├── register.js
        │       └── tooltips.js
        └── templates/
            ├── about.html
            ├── account.html
            ├── announcements.html
            ├── department.html
            ├── email_body.html
            ├── home.html
            ├── layout.html
            ├── login.html
            ├── macros.html
            ├── meet-ups.html
            ├── meetup.html
            ├── notifications.html
            ├── profile.html
            ├── register.html
            ├── reset_password.html
            ├── reset_request.html
            ├── submit.html
            ├── submits.html
            └── task.html
  ```
  
</details>

## Setup
There are a few environment variables needed for the application to work:

| Syntax | Description | Defualt | Importance |
| ----------- | ----------- | ---------- | ---------- |
| *DATABASE_URL* | Url configuration for the database | sqlite:///site.db | High |
| *SECRET_KEY* | A long random string | A random 16 character long string is generated | High |
| *GOOGLE_API* | Essential for the maps to work properly | None | Medium |
| *ADMIN_USERNAME* | The username of the admin page | admin | Medium |
| *ADMIN_PASSWORD* | The passowrd of the admin page | admin | Medium |
| *MAIL_SERVER* | The IMAP of the e-mail service | imap.gmail.com | Low |
| *MAIL_PORT* | The port of the e-mail service | 465 | Low |
| *MAIL_USE_TLS* | TLS option of the e-mail service | False | Low |
| *MAIL_USE_SSL* | SSL option of the e-mail service | True | Low |
| *MAIL_USERNAME* | The email address to send emails from | None | Low |
| *MAIL_PASSWORD* | The password for the email address | None | Low |

## Usage
```bash
reset.py    # for the first time only
python run.py
```
Navigate to your browser and enter **[localhost:5000](localhost:5000)** in the address bar

[//]: <> ( ## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.)
