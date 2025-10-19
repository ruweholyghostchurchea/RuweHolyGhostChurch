# Overview

The RuweHolyGhostChurch Management System is a comprehensive Django-based church administration platform designed for Ruwe Holy Ghost Church EA. The system manages the complete church ecosystem including hierarchical church structure (Diocese > Pastorate > Church), member profiles, visitor tracking, attendance monitoring, financial management, and bulk communication capabilities.

The application serves as a centralized hub for church administrators to efficiently manage all aspects of church operations, from member registration and role assignments to service attendance tracking and financial reporting.

**Architecture (Updated October 2025)**: The system now uses a multi-subdomain architecture with three distinct portals:
- **Admin CMS** (cms.ruweholyghostchurch.org): Church administration and management
- **Members Portal** (members.ruweholyghostchurch.org): Member self-service portal (in development)
- **Public Website** (ruweholyghostchurch.org): Public-facing church information (in development)

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
- **Django Auth System**: Built-in user authentication with OneToOne relationship to Members model
- **Auto-Sync Signals**: Automatic User account creation when Members are registered, and vice versa
- **Role-Based Access**: Member roles including Youth, Adult, Elder with clergy sub-roles
- **Session Management**: Configurable session expiry with "remember me" functionality
- **CSRF Protection**: Enhanced security for form submissions
- **Subdomain Routing**: Middleware-based subdomain detection for multi-portal access

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
- **ALLOWED_HOSTS**: Wildcard only in DEBUG mode; production uses explicit domain list
- **Subdomain Security**: Separate URL configurations and session handling per subdomain

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

# Recent Changes (October 2025)

## Multi-Subdomain Architecture Implementation
- **Subdomain Middleware**: Created custom middleware to detect and route requests based on subdomain
- **URL Configurations**: Separate URL routing for cms, members, and public subdomains
- **New Django Apps**: 
  - `members_portal`: Foundation for member self-service features (templates to be built)
  - `public_site`: Foundation for public website (templates to be built)

## User-Member Integration
- **OneToOne Relationship**: Linked Django's built-in User model with the Members model
- **Signal-Based Auto-Sync**: 
  - Creating a superuser automatically creates a Member profile
  - Registering a Member automatically creates a User account for portal access
  - Prevents infinite loops and DoesNotExist exceptions using hasattr() guards
- **Migration**: Applied migration to add user field to Members model

## Security Enhancements
- **Environment-Based ALLOWED_HOSTS**: Wildcard only enabled in DEBUG mode
- **Session Configuration**: Updated for cross-subdomain session management
- **Production Ready**: Settings configured for production deployment with proper security headers

## Development Environment Routing (Latest Update)
- **Homepage Routing**: Development environment now defaults to public site (public_urls.py)
- **Login Flow**: Login redirects to Members Portal dashboard after successful authentication
- **Cross-Portal Access**: 
  - Public site includes Members Portal at /members/ path
  - Public site includes Admin Dashboard at /dashboard/ path  
  - Staff/admin users see Admin CMS link in Members Portal sidebar
- **Member Profile Requirement**: Members Portal requires a linked Member profile (user.member_profile)
  - Superuser needs a Member profile created to access Members Portal
  - Use Admin CMS to create Member profile and link to user account