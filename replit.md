# Overview

The RuweHolyGhostChurch Management System is a comprehensive Django-based church administration platform designed for Ruwe Holy Ghost Church EA. Its purpose is to manage the complete church ecosystem, including a hierarchical church structure (Diocese > Pastorate > Church), member profiles, visitor tracking, attendance monitoring, financial management, and bulk communication. The system aims to centralize church operations for efficient administration.

The project is ambitious, aiming to provide a multi-subdomain architecture with distinct portals: an Admin CMS for church management, a Members Portal for self-service, and a Public Website for general information, thereby covering all facets of church interaction and administration.

# User Preferences

Preferred communication style: Simple, everyday language.

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