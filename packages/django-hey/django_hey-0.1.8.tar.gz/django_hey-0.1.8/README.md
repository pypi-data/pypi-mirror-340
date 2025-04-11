
# Django Hey

**Django Hey** is a lightweight, command-line utility that simplifies the process of initializing Django projects and applications. With a single command, it automates the creation of a Django project, an accompanying app, URL configurations, and a starter view—streamlining your workflow and letting you dive into development faster. Built for developers of all levels, `django-hey` ensures consistency and efficiency in setting up Django environments.

## Key Features

- Rapid Project Setup: Generate a fully structured Django project in seconds.
- App Creation: Automatically create an app within your project.
- URL Configuration: Pre-configure `urls.py` for both project and app with a default route.
- Settings Integration: Seamlessly add your app to the project's `INSTALLED_APPS`.
- Starter View: Include a basic view with a welcome message to get you started.
- Verbose Feedback: Receive clear success messages for each step.

## Installation

To use `django-hey`, ensure you have Python 3.6+ installed. Install the package globally via pip:

```bash
pip install django-hey
```

### Prerequisites

**Django:** The tool requires Django 3.0 or higher. Install it if not already present:

```bash
pip install django>=3.0
```

## Usage

Run the following command to create a new Django project and app:

```bash
hey django create <project_name> <app_name>
```

### Example

```bash
hey django create blogproject blogapp
```

### What It Does

- Creates a Django project named `blogproject` in your current directory.
- Adds an app named `blogapp` inside `blogproject`.
- Generates `blogapp/urls.py` with a default route ('') linked to a home view.
- Updates `blogproject/settings.py` to include `blogapp` in `INSTALLED_APPS`.
- Modifies `blogproject/urls.py` to integrate `blogapp.urls`.
- Creates a home view in `blogapp/views.py` that returns `"Welcome to blogapp!"`.

### Command Output

```
Project 'blogproject' created successfully!
App 'blogapp' created successfully!
'urls.py' created in 'blogapp' successfully!
App 'blogapp' added to INSTALLED_APPS!
Project 'urls.py' updated to include 'blogapp.urls'!
Basic view created in 'blogapp/views.py'!
```

## Running Your Project

Navigate to the project directory and launch the development server:

```bash
cd blogproject
python manage.py runserver
```

Open your browser to http://127.0.0.1:8000/ to see "Welcome to blogapp!".

## Requirements

- **Python**: Version 3.6 or later
- **Django**: Version 3.0 or later (installed separately)

## Troubleshooting

- **"django-admin: command not found"**: Install Django with `pip install django` and ensure it's available in your PATH.
- **Permission Issues**: Run your terminal with elevated privileges or use a virtual environment.
- **Command Not Recognized**: Confirm installation with `pip show django-hey` and check your PATH.

## Contributing

Contributions are welcome! To contribute:

- Fork the repository on GitHub.
- Submit pull requests with improvements or bug fixes.
- Report issues or suggest features via the issue tracker.

## License

django-hey is released under the MIT License. See the LICENSE file for full details.

## Author

Developed by **Sabari Nathan**  
📧 Email: sabareee000@gmail.com  
💻 GitHub: [github.com/sabari7497](https://github.com/sabari7497)

For questions, feedback, or support, feel free to reach out!
