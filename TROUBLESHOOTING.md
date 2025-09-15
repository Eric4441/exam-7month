# Troubleshooting Guide

## Static Files Not Loading (CSS/JS Issues)

If you're getting errors with CSS not loading, follow these steps:

### 1. Check Static Files Configuration

Ensure your `settings.py` has:
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

### 2. In PyCharm or Other IDEs

1. **Clear Browser Cache**: Ctrl+F5 or Ctrl+Shift+R
2. **Restart Django Server**: Stop and restart `python manage.py runserver`
3. **Check Console**: Open browser developer tools (F12) and check for 404 errors

### 3. Manual Static Files Collection

Run these commands:
```bash
python manage.py collectstatic --noinput
python manage.py runserver
```

### 4. Alternative: Use CDN Only

If static files still don't work, the page will still function with Bootstrap and Font Awesome from CDN.

### 5. Check URLs

- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/
- Posts: http://127.0.0.1:8000/posts/
- Demo data: http://127.0.0.1:8000/install/

### 6. Create Demo Data

Visit: http://127.0.0.1:8000/install/
This will create demo user and posts for testing.

Demo login:
- Username: demo
- Password: demo123

### 7. Common PyCharm Issues

1. **Port conflicts**: Try different port: `python manage.py runserver 8001`
2. **Virtual environment**: Make sure PyCharm is using the correct Python interpreter
3. **Project root**: Ensure PyCharm is opened in the correct project directory
