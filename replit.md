# Overview

The RuweHolyGhostChurch Management System is a comprehensive Django-based church administration platform designed for Ruwe Holy Ghost Church EA. Its purpose is to manage the complete church ecosystem, including a hierarchical church structure (Diocese > Pastorate > Church), member profiles, visitor tracking, attendance monitoring, financial management, and bulk communication. The system aims to centralize church operations for efficient administration.

The project is ambitious, aiming to provide a multi-subdomain architecture with distinct portals: an Admin CMS for church management, a Members Portal for self-service, and a Public Website for general information, thereby covering all facets of church interaction and administration.

# User Preferences

Preferred communication style: Simple, everyday language.

# 🔴 CRITICAL: Python Version Management

## Python Version: 3.12 (LOCKED)

This project **MUST** use Python 3.12. Any other version will cause package import failures, especially with `psycopg2-binary` and `Pillow`.

### Version Lock Configuration
- **Module**: `python-3.12` (in `.replit` file)
- **Lock File**: `.python-version` contains `3.12`
- **System Python**: Uses Nix Python 3.12 from `/nix/store/.../python3-3.12.x/`

### Installing Packages (CRITICAL - Follow Exactly)
```bash
# ✅ ALWAYS use this method:
python3 -m pip install -r requirements.txt

# ❌ NEVER use these:
pip install -r requirements.txt        # Wrong - may use wrong Python
pip3 install -r requirements.txt       # Wrong - may use wrong Python
```

### Common Errors & Quick Fixes

**Error**: "ModuleNotFoundError: No module named 'psycopg2._psycopg'"
```bash
python3 -m pip install psycopg2-binary==2.9.10 --force-reinstall --no-cache-dir
```

**Error**: "Cannot use ImageField because Pillow is not installed"
```bash
python3 -m pip install Pillow==11.3.0 --force-reinstall --no-cache-dir
```

**Error**: "Couldn't import Django"
```bash
python3 -m pip install -r requirements.txt --force-reinstall
```

### Verification Commands
```bash
# Check Python version (should be 3.12.x)
python3 --version

# Verify correct Python path
which python3  # Should show /nix/store/.../python3-3.12.x/bin/python3

# Test critical packages
python3 -c "import psycopg2; print('✅ psycopg2 OK')"
python3 -c "from PIL import Image; print('✅ Pillow OK')"
python3 -c "import django; print('✅ Django OK')"
```

### Why This Matters
- C extensions in `psycopg2-binary` and `Pillow` are compiled for specific Python versions
- Python 3.12 vs 3.11 have different internal APIs (`_psycopg`, `_imaging`)
- Mixing versions causes `ModuleNotFoundError` even when packages are "installed"

### Documentation Files
- **`PYTHON_VERSION_GUIDE.md`**: Comprehensive troubleshooting guide
- **`requirements.txt`**: All package dependencies with comments
- **`.python-version`**: Version lock file (contains `3.12`)

**Last Updated**: November 22, 2025

# System Architecture

## Core Framework
The system is built on **Django 5.2.4**, leveraging its MVC architecture, ORM, and admin interface. **Django REST Framework** provides API capabilities, secured with **Django Simple JWT** for token-based authentication.

## Database Design
Utilizes **Django ORM** for database interactions. Key design principles include a three-tier hierarchical church organization (Diocese → Pastorate → Church), complex member relationship mapping, and the use of **JSON Fields** for flexible storage of dynamic data.

## Authentication & Authorization
Employs Django's built-in authentication system with a **OneToOne relationship** to the Members model, featuring **auto-sync signals** for user account creation. **Role-Based Access Control** (RBAC) is implemented, with configurable session management and **CSRF protection**. Subdomain routing middleware enables multi-portal access control.

## Frontend Architecture
The frontend uses **Server-Side Rendering** with Django templates and a **responsive, mobile-first design** including a dark theme. **AJAX integration** provides dynamic interactions, and a custom JavaScript-based rich text editor is used for content.

## Data Models Structure
Key data models include:
- **Church Structure**: Diocese, Pastorate, Church with leadership.
- **Member Management**: Comprehensive profiles and family relationships.
- **Service Management**: Attendance tracking.
- **Financial Management**: Offerings and expenses.
- **Email System**: Campaigns, templates, and logs.
- **Communication**: SMS templates.
- **Visitors Management**: Tracks visitors, visits, follow-ups, and conversion to members. Includes automated welcome and thank-you emails.
- **Attendance/Register System**: Manages attendance sessions, records, absence streaks, and sends automated absence alerts.

## File Storage Strategy
Profile pictures and documents are stored as URLs. **Static files** (CSS/JS) are served via Django's static file system, with **WhiteNoise** handling static file serving in production.

## Security Measures
Includes **CSRF tokens**, **input validation** via Django forms, **SQL injection prevention** through Django ORM, secure **session management** with HTTP-only cookies, and explicit **ALLOWED_HOSTS** configuration for production. Staff-only features are protected with `@staff_required` decorators.

## Multi-Subdomain Architecture
The system supports three distinct subdomains: `cms.ruweholyghostchurch.org` (Admin CMS), `members.ruweholyghostchurch.org` (Members Portal), and `ruweholyghostchurch.org` (Public Website), each with separate URL configurations and session handling.

# External Dependencies

## Core Framework Dependencies
- **Django 5.2.4**: Web framework.
- **djangorestframework 3.15.2**: API development.
- **djangorestframework-simplejwt 5.5.0**: JWT authentication.
- **django-jazzmin 3.0.1**: Enhanced admin interface.

## Database & Storage
- **PyMySQL 1.1.1**: MySQL connector.
- **Pillow 11.3.0**: Image processing.
- **whitenoise 6.9.0**: Static file serving.

## UI & Content Management
- **django-ckeditor-5 0.2.17**: Rich text editing.
- **FontAwesome 6.5.1**: Icon library (CDN).
- **Custom CSS Framework**: Dark theme responsive design.

## Production & Deployment
- **gunicorn 23.0.0**: WSGI HTTP server.
- **python-dotenv 1.1.0**: Environment variable management.
- **django-cors-headers 4.7.0**: Cross-origin resource sharing.

## Communication Services
- **Email System**: Utilizes Django's built-in SMTP for campaign management, automated emails (welcome, absence alerts, visitor follow-ups), and professional HTML templates.
- **Bulk SMS Integration**: Prepared for third-party SMS service integration.