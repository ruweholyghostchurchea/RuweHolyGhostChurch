# Overview

The RuweHolyGhostChurch Management System is a comprehensive Django-based church administration platform designed for Ruwe Holy Ghost Church EA. The system manages the complete church ecosystem including hierarchical church structure (Diocese > Pastorate > Church), member profiles, visitor tracking, attendance monitoring, financial management, and bulk communication capabilities.

The application serves as a centralized hub for church administrators to efficiently manage all aspects of church operations, from member registration and role assignments to service attendance tracking and financial reporting.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
- **Django 5.2.4**: Core web framework providing MVC architecture, ORM, and admin interface
- **Django REST Framework**: API endpoints for AJAX functionality and potential mobile app integration
- **Django Simple JWT**: Token-based authentication for API security

## Database Design
- **Django ORM**: Object-relational mapping for database interactions
- **Hierarchical Structure**: Three-tier church organization (Diocese → Pastorate → Church)
- **Member Relationship Mapping**: Complex family and church role relationships
- **JSON Fields**: Flexible storage for member roles, custom fields, and dynamic data

## Authentication & Authorization
- **Django Auth System**: Built-in user authentication with custom UserProfile extension
- **Role-Based Access**: Member roles including Youth, Adult, Elder with clergy sub-roles
- **Session Management**: Configurable session expiry with "remember me" functionality
- **CSRF Protection**: Enhanced security for form submissions

## Frontend Architecture
- **Server-Side Rendering**: Django templates with Jinja2-style syntax
- **Responsive Design**: Mobile-first CSS with dark theme UI
- **AJAX Integration**: Dynamic form interactions and cascading dropdowns
- **Rich Text Editing**: Custom JavaScript-based rich text editor for descriptions

## Data Models Structure
- **Church Structure**: Diocese, Pastorate, Church with leadership assignments
- **Member Management**: Comprehensive member profiles with family relationships
- **Service Management**: Attendance tracking linked to services and members
- **Financial Management**: Offerings, expenses with categorization
- **Communication**: SMS templates and campaign management

## File Storage Strategy
- **URL-Based Media**: Profile pictures and documents stored as URLs rather than local files
- **Static Files**: CSS/JS served through Django's static file system
- **WhiteNoise**: Static file serving in production environments

## Security Measures
- **CSRF Tokens**: Protection against cross-site request forgery
- **Input Validation**: Django forms with comprehensive field validation
- **SQL Injection Prevention**: Django ORM parameterized queries
- **Session Security**: HTTP-only cookies with secure settings

# External Dependencies

## Core Framework Dependencies
- **Django 5.2.4**: Main web framework
- **djangorestframework 3.15.2**: API development
- **djangorestframework-simplejwt 5.5.0**: JWT authentication
- **django-jazzmin 3.0.1**: Enhanced admin interface

## Database & Storage
- **PyMySQL 1.1.1**: MySQL database connector (configurable for other databases)
- **Pillow 11.3.0**: Image processing capabilities
- **whitenoise 6.9.0**: Static file serving

## UI & Content Management
- **django-ckeditor-5 0.2.17**: Rich text editing capabilities
- **FontAwesome 6.5.1**: Icon library (CDN)
- **Custom CSS Framework**: Dark theme responsive design

## Production & Deployment
- **gunicorn 23.0.0**: WSGI HTTP server for production
- **python-dotenv 1.1.0**: Environment variable management
- **django-cors-headers 4.7.0**: Cross-origin resource sharing

## Communication Services
- **Bulk SMS Integration**: Prepared for SMS service provider integration
- **Email Backend**: Django's built-in email system for notifications

## Development Tools
- **Django Debug Toolbar**: Development debugging (implied)
- **Django Extensions**: Enhanced management commands (implied)

The system is architected for scalability with clear separation of concerns, modular app structure, and extensible design patterns that allow for easy feature additions and customizations.