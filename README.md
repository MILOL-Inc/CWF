# Coral Web Framework (CWF)

## Introduction
Coral Web Framework (CWF) is a versatile and powerful web framework designed for developing both server and client applications. Utilizing the robustness of Python and Tornado, along with the responsiveness of Bootstrap, CWF offers a comprehensive toolkit for building modern web applications.

## Key Features

### Versatile Application Development
* User Interface Apps: Create dynamic and responsive user interfaces with ease.
* Terminal Routines: Develop command-line applications for backend processes.

### Robust Backend Administration
* GUI and Terminal Support: Manage your application through a graphical user interface or via the command line.
* Python and Tornado Framework: Leverage the power of Python and the efficiency of Tornado for server-side logic.

### Seamless Integration
* HTML and Bootstrap: Design compelling web pages with Bootstrap's responsive features.
* GridJS and ChartJS Integration: Embed interactive tables and charts into your applications.
  
### Extensive Database Support
* Multiple Database APIs: Connect with a variety of databases including SQLite, PyDBLite, Rockdb, MongoDB, and Redis.

### Security
* Cryptographic Password Security: Ensure user data safety with built-in cryptographic functionalities.

### Advanced APIs
* Python smtplib API: Simplify Email handling in Python.
* JSON Logs API: Efficient logging mechanism using JSON for better data structure and retrieval.

## Getting Started
* git clone https://github.com/MILOL-Inc/CWF.git
* cd CWF/container
* vi public/__path__.py (Add your absolute path to the container directory.)
* $ cwf --init (Create initial database.)
* $ cwf --apps (Run manage application.)
* Visit http://locahost:8090
* Credentials: ad@cwf.local (Get password from public/_pass_.py file. )

## Documentation
```
$ cwf -v | Show version number.
$ cwf -h | Shows Help Menu.
$ cwf --init | Initialize database settings.
$ cwf --listapps | List all apps.
$ cwf --listroutines | List all routine apps.
$ cwf --apps | Runs enabled apps.
$ cwf --routines | Runs all enabled routine apps.
$ cwf --runapp 'myapp_name' | Run app in foreground mode.
$ cwf --runroutine 'myapp_name' | Run routine app in foreground mode.
$ cwf --createapp 'myapp_name' | Creates app.
$ cwf --createapp 'myapp_name' [PORT] [1|0] [project_id] | Creates app with values. status = 0|1
$ cwf --deleteapp 'myapp_name' | Deletes app.
$ cwf --updateapp 'myapp_id [PORT] [STATUS] [project_id]' | Update app. status = 0|1
$ cwf --createroutine 'myapp_name' | Creates routine app.
$ cwf --createroutine 'myapp_name' [PORT] [1|0] [project_id] | Creates routine app with values. status = 0|1
$ cwf --deleteroutine 'myapp_name' | Deletes routine app.
$ cwf --updateroutine 'myapp_id [PORT] [STATUS] [project_id]' | Update routine app. status = 0|1
```

## License
Repository released under MIT License.
