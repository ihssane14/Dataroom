# Dataroom
DataRoom Enterprise
Project Description

DataRoom Enterprise is an educational web security project that demonstrates real-world vulnerabilities in a simulated enterprise web application.

The project focuses on two critical OWASP Top 10 vulnerabilities:

Directory Traversal

Command Injection

These vulnerabilities are intentionally implemented for learning and demonstration purposes.

Features

Enterprise-style admin dashboard

Document management system

System administration module

Security logs and audit interface

Automated vulnerability demonstrations

Demonstrated Vulnerabilities
Directory Traversal

Allows unauthorized access to sensitive files such as configuration and API key files.

Command Injection

Executes operating system commands due to improper input validation.

Technologies Used

Backend: Python, Flask

Frontend: HTML (Jinja2), CSS

Environment: Localhost, Windows

Project Structure
DATAROOM/
│
├── app.py
├── requirements.txt
├── config/
│   ├── api_keys.txt
│   └── database.conf
├── documents/
│   ├── handbook.txt
│   └── report.txt
├── logs/
│   ├── application.log
│   └── security.log
└── templates/
    ├── audit.html
    ├── dashboard.html
    ├── documents.html
    ├── login.html
    ├── logs.html
    ├── system_admin.html
    └── users.html

Disclaimer

 This project is developed strictly for educational purposes.
The vulnerabilities are intentional and must not be used in production environments.
