# PythonAnywhere Deployment Checklist

## 1. Create virtual environment
```
mkvirtualenv --python=python3.9 django-exam
```

## 2. Install dependencies
```
pip install -r /home/<username>/path/to/project/requirements.txt
```

## 3. Configure environment variables
Set these in the PythonAnywhere WSGI file or in the web app configuration:
- `DEBUG=0`
- `ALLOWED_HOSTS=yourusername.pythonanywhere.com`

## 4. Update Django settings
- Confirm `STATIC_ROOT` and `MEDIA_ROOT` are set.
- Confirm `ALLOWED_HOSTS` and `DEBUG` are driven by env vars.

## 5. Run migrations
```
python manage.py migrate
```

## 6. Collect static files
```
python manage.py collectstatic
```

## 7. Configure static and media paths in PythonAnywhere
- Static: `/home/<username>/path/to/project/staticfiles` mapped to `/static/`
- Media: `/home/<username>/path/to/project/media` mapped to `/media/`

## 8. WSGI configuration
In the WSGI file, ensure the project path is on `sys.path` and set the correct settings module:
```
import os
import sys

path = '/home/<username>/path/to/project'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
```

## 9. Test
- Reload the web app.
- Verify upload and approved pages.
- Upload `sample_products.xlsx`.
