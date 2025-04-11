import os
import subprocess
import sys
import argparse
import platform

def create_and_use_virtual_environment():
    """Create a virtual environment and return its Python path for use."""
    venv_path = os.path.join(os.getcwd(), 'venv')
    try:
        # Create the virtual environment
        subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
        print("Virtual environment 'venv' created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create virtual environment 'venv': {e}")
        sys.exit(1)

    # Determine the Python path and activation command based on the OS
    if platform.system() == "Windows":
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
        activate_cmd = f"venv\\Scripts\\activate.bat"
    else:  # macOS or Linux
        python_path = os.path.join(venv_path, 'bin', 'python')
        activate_cmd = f"source venv/bin/activate"

    # Install Django in the virtual environment
    try:
        subprocess.run([python_path, '-m', 'pip', 'install', 'django>=3.0'], check=True)
        print("Django installed successfully in the virtual environment!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Django in the virtual environment: {e}")
        sys.exit(1)

    # Print copy-paste-ready activation command
    print("\nPlease activate the virtual environment before running the server:")
    print(f"Copy and paste this command in your terminal and press Enter:")
    print(f"  {activate_cmd}")
    print(f"After activation, run: python manage.py runserver")
    print(f"Virtual environment created at: {venv_path}")
    return python_path

def create_project_and_app(project_name, app_name, python_path):
    """Create a Django project and app using the virtual environment's Python."""
    # Step 1: Create the Django project
    try:
        subprocess.run([python_path, '-m', 'django', 'startproject', project_name], check=True, cwd=os.getcwd())
        print(f"Project '{project_name}' created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create project '{project_name}': {e}")
        sys.exit(1)

    # Step 2: Change to project directory
    project_dir = os.path.join(os.getcwd(), project_name)
    os.chdir(project_dir)

    # Step 3: Create the Django app
    try:
        subprocess.run([python_path, 'manage.py', 'startapp', app_name], check=True)
        print(f"App '{app_name}' created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create app '{app_name}': {e}")
        sys.exit(1)

    # Step 4: Create urls.py in the app
    app_urls_path = os.path.join(app_name, 'urls.py')
    urls_content = f"""from django.urls import path
from . import views

app_name = '{app_name}'
urlpatterns = [
    path('', views.home, name='home'),
]
"""

    try:
        with open(app_urls_path, 'w', encoding='utf-8') as f:
            f.write(urls_content)
        print(f"'urls.py' created in '{app_name}' successfully!")
    except Exception as e:
        print(f"Failed to create 'urls.py': {e}")
        sys.exit(1)

    # Step 5: Update project settings.py to include the app
    settings_path = os.path.join(project_name, 'settings.py')
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings_content = f.readlines()

        for i, line in enumerate(settings_content):
            if 'INSTALLED_APPS' in line:
                for j in range(i, len(settings_content)):
                    if ']' in settings_content[j]:
                        settings_content.insert(j, f"    '{app_name}',\n")
                        break
                break

        with open(settings_path, 'w', encoding='utf-8') as f:
            f.writelines(settings_content)
        print(f"App '{app_name}' added to INSTALLED_APPS!")
    except Exception as e:
        print(f"Failed to update settings.py: {e}")
        sys.exit(1)

    # Step 6: Update project urls.py to include app urls
    project_urls_path = os.path.join(project_name, 'urls.py')
    try:
        with open(project_urls_path, 'r', encoding='utf-8') as f:
            urls_content = f.readlines()

        # Ensure 'include' is imported
        import_line = "from django.urls import path, include\n"
        if not any(line.strip() == import_line.strip() for line in urls_content):
            for i, line in enumerate(urls_content):
                if line.strip().startswith("from django.urls import"):
                    urls_content[i] = import_line
                    break
            else:
                urls_content.insert(0, import_line)

        # Add the path if not present
        path_line = f"    path('', include('{app_name}.urls')),\n"
        if not any(path_line.strip() in line.strip() for line in urls_content):
            for i, line in enumerate(urls_content):
                if line.strip() == "urlpatterns = [":
                    urls_content.insert(i + 1, path_line)
                    break

        with open(project_urls_path, 'w', encoding='utf-8') as f:
            f.writelines(urls_content)
        print(f"Project 'urls.py' updated to include '{app_name}.urls'!")
    except Exception as e:
        print(f"Failed to update project urls.py: {e}")
        sys.exit(1)

    # Step 7: Create a basic home view in app/views.py
    views_path = os.path.join(app_name, 'views.py')
    views_content = f"""from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to {app_name}!")
"""

    try:
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(views_content)
        print(f"Basic view created in '{app_name}/views.py'!")
    except Exception as e:
        print(f"Failed to update views.py: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Django Hey: Create a Django project and app with a virtual environment.')
    parser.add_argument('subcommand', help='Subcommand: django')
    parser.add_argument('action', help='Action: create')
    parser.add_argument('project_name', help='Name of the project')
    parser.add_argument('app_name', help='Name of the app')

    args = parser.parse_args()

    if args.subcommand != 'django' or args.action != 'create':
        print("Usage: hey django create <project_name> <app_name>")
        sys.exit(1)

    # Create and use the virtual environment
    python_path = create_and_use_virtual_environment()
    # Create project and app using the venv's Python
    create_project_and_app(args.project_name, args.app_name, python_path)

if __name__ == '__main__':
    main()