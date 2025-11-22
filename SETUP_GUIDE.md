# Ruwe Holy Ghost Church Management System - Setup Guide

## 🚀 Quick Start (For New Developers)

### Step 1: Verify Python Version
```bash
python3 --version
# Expected output: Python 3.12.x
```

If not 3.12, **STOP** and check `.replit` module configuration.

### Step 2: Install Dependencies
```bash
# Use this exact command (do NOT use pip or pip3 alone):
python3 -m pip install -r requirements.txt
```

### Step 3: Set Up Database
```bash
# The PostgreSQL database is already configured via environment variables
# Run migrations to create tables:
python3 manage.py migrate
```

### Step 4: Create Admin User (Optional)
```bash
python3 manage.py createsuperuser
```

### Step 5: Run Development Server
```bash
python3 manage.py runserver 0.0.0.0:5000
```

Visit: `http://localhost:5000` or your Replit preview URL

---

## 📦 Package Installation Details

### Critical Dependencies

1. **Django 5.2.4** - Main web framework
2. **psycopg2-binary 2.9.10** - PostgreSQL database adapter (MUST match Python version)
3. **Pillow 11.3.0** - Image processing (MUST match Python version)
4. **gunicorn 23.0.0** - Production WSGI server

### If Packages Fail to Import

Common issue: Packages installed for wrong Python version

**Solution**:
```bash
# Reinstall the problematic package for Python 3.12:
python3 -m pip install <package-name> --force-reinstall --no-cache-dir

# Example for psycopg2:
python3 -m pip install psycopg2-binary==2.9.10 --force-reinstall --no-cache-dir
```

---

## 🗄️ Database Configuration

### Database Type: PostgreSQL

The project uses PostgreSQL (via Replit's managed database service).

### Environment Variables (Auto-configured)
- `DATABASE_URL` - Full PostgreSQL connection string
- `PGHOST` - Database host
- `PGPORT` - Database port (usually 5432)
- `PGUSER` - Database username
- `PGPASSWORD` - Database password
- `PGDATABASE` - Database name

### Database Settings Location
File: `ruweholyghostchurch/settings.py` (lines 180-200)

The settings automatically detect `DATABASE_URL` and configure accordingly.

---

## 🏗️ Project Structure

```
ruweholyghostchurch/
├── attendance/          # Attendance tracking system
├── authentication/      # User authentication & login
├── bulk_sms/           # SMS campaign management
├── church_settings/    # Church configuration
├── church_structure/   # Diocese/Pastorate/Church hierarchy
├── dashboard/          # Admin dashboard
├── email_system/       # Email campaigns & templates
├── equipment/          # Equipment management
├── finance/            # Financial tracking
├── members/            # Member profiles & management
├── members_portal/     # Member self-service portal
├── public_site/        # Public-facing website
├── reports/            # Reporting system
├── ruwe_administration/ # Administrative functions
├── visitors/           # Visitor tracking & follow-up
├── ruweholyghostchurch/ # Main Django project settings
├── static/             # Static files (CSS, JS, images)
├── staticfiles/        # Collected static files for production
├── templates/          # HTML templates
└── media/              # User-uploaded files
```

---

## 🔧 Common Commands

### Database Management
```bash
# Create new migrations after model changes
python3 manage.py makemigrations

# Apply migrations to database
python3 manage.py migrate

# Create database cache table (for caching)
python3 manage.py createcachetable
```

### Static Files
```bash
# Collect static files for production
python3 manage.py collectstatic --noinput
```

### User Management
```bash
# Create superuser (admin)
python3 manage.py createsuperuser

# Change user password
python3 manage.py changepassword <username>
```

### Development Server
```bash
# Run development server (default port 5000)
python3 manage.py runserver 0.0.0.0:5000

# Run with different port
python3 manage.py runserver 0.0.0.0:8000
```

---

## 🌐 Multi-Subdomain Architecture

The system supports three distinct portals:

1. **Admin CMS**: `cms.ruweholyghostchurch.org`
   - Full administrative control
   - Staff/admin access only
   - URL routing: `ruweholyghostchurch/cms_urls.py`

2. **Members Portal**: `members.ruweholyghostchurch.org`
   - Member self-service
   - Authenticated members only
   - URL routing: `ruweholyghostchurch/members_urls.py`

3. **Public Website**: `ruweholyghostchurch.org` or `www.ruweholyghostchurch.org`
   - Public-facing website
   - No authentication required
   - URL routing: `ruweholyghostchurch/public_urls.py`

**Subdomain Middleware**: `ruweholyghostchurch/middleware.py` handles routing

---

## 🔒 Security Configuration

### Settings Configured
- ✅ CSRF protection enabled
- ✅ Secure cookies in production
- ✅ HTTPS redirect in production
- ✅ HSTS enabled in production
- ✅ XSS filter enabled
- ✅ ALLOWED_HOSTS configured
- ✅ Staff-only decorators on admin views

### Environment-Based Security
- **DEBUG=True** in development (Replit)
- **DEBUG=False** in production (requires HTTPS)

---

## 📝 Environment Variables

### Required for Production
- `EMAIL_HOST_USER` - Email address for sending emails
- `EMAIL_HOST_PASSWORD` - Email account password
- `DATABASE_URL` - PostgreSQL connection string (auto-set in Replit)

### Optional
- `DATABASE_NAME` - Custom database name
- `DATABASE_USER` - Custom database user
- `DATABASE_PASSWORD` - Custom database password
- `DATABASE_HOST` - Custom database host
- `DATABASE_PORT` - Custom database port

---

## 🚨 Troubleshooting

### Server Won't Start
1. Check Python version: `python3 --version` (must be 3.12.x)
2. Check logs for import errors
3. Verify database is accessible
4. Run migrations: `python3 manage.py migrate`

### Import Errors
1. Reinstall package: `python3 -m pip install <package> --force-reinstall`
2. Verify Python version matches
3. Check `requirements.txt` has correct package

### Database Errors
1. Verify `DATABASE_URL` environment variable exists
2. Check PostgreSQL service is running
3. Run migrations: `python3 manage.py migrate`

### Static Files Not Loading
1. Collect static files: `python3 manage.py collectstatic`
2. Check `STATIC_ROOT` and `STATIC_URL` in settings
3. Verify WhiteNoise is in `MIDDLEWARE`

---

## 📚 Additional Documentation

- **`PYTHON_VERSION_GUIDE.md`** - Comprehensive Python version troubleshooting
- **`replit.md`** - Project overview and architecture
- **`requirements.txt`** - Package dependencies with comments
- **`.python-version`** - Python version lock file

---

## 🎯 Next Steps After Setup

1. ✅ Verify server runs: `python3 manage.py runserver 0.0.0.0:5000`
2. ✅ Create admin user: `python3 manage.py createsuperuser`
3. ✅ Access admin panel: `/admin/`
4. ✅ Configure church settings
5. ✅ Set up church hierarchy (Diocese → Pastorate → Church)
6. ✅ Add initial members
7. ✅ Test email configuration
8. ✅ Review security settings for production

---

**Last Updated**: November 22, 2025  
**Python Version**: 3.12  
**Django Version**: 5.2.4  
**Database**: PostgreSQL
