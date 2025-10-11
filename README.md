
# RuweHolyGhostChurch Management System

A comprehensive church management system for Ruwe Holy Ghost Church EA, designed to streamline church operations and member management. Features a multi-subdomain architecture with separate interfaces for admins, members, and the public.

## About Ruwe Holy Ghost Church

The Ruwe Holy Ghost Church traces its origin back to 1906/07 and was founded by Alfayo Odongo Mango and Lawi Obonyo Ongwek in Musanda LUO near the border of former Western and Nyanza Provinces in the early 1930s. The current main headquarters is at Ruwe, Siaya County but there's another divide headquartered at Kisumu.

## System Architecture

The system is built with a **multi-subdomain architecture** to provide distinct experiences for different user types:

### 🌐 Subdomain Structure

1. **Admin CMS** (`cms.ruweholyghostchurch.org`)
   - Full church management system for administrators and staff
   - Complete access to all features and data
   - Member management, finances, reports, etc.

2. **Members Portal** (`members.ruweholyghostchurch.org`)
   - Member-facing portal (login required)
   - Members can view their own information, attendance, contributions
   - Password reset functionality for account activation

3. **Public Website** (`ruweholyghostchurch.org`)
   - Public-facing website (no authentication required)
   - Church information, events, contact forms
   - Accessible to anyone

### 🔐 Authentication & User Management

The system implements a **dual authentication system** linking Django's built-in User model with the Members model:

#### User-Member Relationship
- **OneToOne Link**: Each Member can optionally have a linked User account for authentication
- **Auto-Sync**: When a superuser is created, a basic Member profile is automatically generated
- **Member Registration**: When admins register a member, a User account is auto-created with an unusable password
- **Account Activation**: Members use the "Forgot Password" flow to set their password and activate their account

#### How It Works

1. **Admin Creates Superuser**:
   ```bash
   python manage.py createsuperuser
   ```
   → Automatically creates a Member profile linked to this User
   → Admin appears in Members list

2. **Admin Registers Member**:
   - Admin fills member registration form
   → System creates Member record
   → System auto-creates linked User account
   → User password is set as unusable
   → Member receives email/SMS to reset password

3. **Member Account Activation**:
   - Member goes to `members.ruweholyghostchurch.org`
   - Clicks "Forgot Password"
   - Receives password reset email
   - Sets new password
   - Can now login to Members Portal

## Features

### 🏛️ Church Structure Management (CMS Only)
- **Diocese Management**: Organize church hierarchy at the diocese level
- **Pastorate Management**: Manage pastorate subdivisions
- **Church Management**: Individual church branch administration

### 👥 Member Management (CMS Only)
- **Comprehensive Member Profiles**: Store detailed member information including:
  - Personal details (name, gender, marital status, education level)
  - Contact information (phone, email, location)
  - Baptismal information and church membership history
  - Job/occupation and income details
  - Emergency contacts (up to 2 contacts per member)
  - Profile photo management (upload or URL)
  - Custom fields for flexible data storage
  - **User Account Link**: Optional link to Django User for login access
- **Document Management**: Attach important documents like:
  - Baptism certificates
  - Annual tithe cards
  - ID documents
  - Medical records
  - Membership certificates
- **Church Hierarchy Assignment**: Link members to home and town churches
- **Member Groups**: Categorize members as Youth, Adult, Elder, or Clergy

### 🚪 Visitor Management (CMS Only)
- Track church visitors and their information
- Monitor visitor engagement and follow-up

### 📊 Attendance Tracking
- **CMS**: Admins can record and manage all attendance
- **Members Portal**: Members can view their own attendance history

### 💰 Financial Management
- **CMS**: Full financial management and reporting
- **Members Portal**: Members can view their own giving/contribution history

### 📱 Bulk SMS System (CMS Only)
- Send bulk messages to members
- Communication management for church announcements
- Member group-based messaging

### 🛠️ Equipment Management (CMS Only)
- Track church equipment and assets
- Maintenance schedules and records
- Equipment allocation and usage

### 📈 Reports & Analytics (CMS Only)
- Generate comprehensive reports on:
  - Member statistics
  - Attendance patterns
  - Financial summaries
  - Growth analytics

### ⚙️ Church Settings (CMS Only)
- Configurable church-specific settings
- System preferences and customization

### 🌍 Public Website (Coming Soon)
- Church information and history
- Service times and locations
- Events calendar
- Contact form
- News and announcements

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: PostgreSQL (Neon/Replit PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript with Bootstrap
- **File Storage**: Local file system with media handling
- **Authentication**: Django's built-in authentication system
- **Architecture**: Multi-subdomain with middleware-based routing

## Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database
- pip package manager

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ruweholyghostchurch
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional):
   ```bash
   export DATABASE_URL="postgresql://user:password@host:port/dbname"
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```
   Note: This automatically creates a Member profile for the superuser

6. **Run the development server**:
   ```bash
   python manage.py runserver 0.0.0.0:5000
   ```

7. **Access the application**:
   - Development (defaults to CMS): `http://localhost:5000`
   - Admin panel: `http://localhost:5000/admin`

### Production Deployment (cPanel)

1. **Configure DNS**:
   - Create subdomain: `cms.ruweholyghostchurch.org`
   - Create subdomain: `members.ruweholyghostchurch.org`
   - Main domain: `ruweholyghostchurch.org`
   - All should point to the same Django application

2. **Update settings.py**:
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS` with your domains
   - Configure email settings for password reset

3. **Run migrations**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

4. **Create superuser and start**:
   ```bash
   python manage.py createsuperuser
   gunicorn --bind=0.0.0.0:5000 ruweholyghostchurch.wsgi:application
   ```

## Project Structure

```
ruweholyghostchurch/
├── attendance/              # Attendance tracking module
├── authentication/          # User authentication (shared)
├── bulk_sms/               # SMS communication system
├── church_settings/        # Church configuration settings
├── church_structure/       # Diocese, Pastorate, Church management
├── dashboard/              # Main dashboard and analytics (CMS)
├── equipment/              # Equipment and asset management
├── finance/                # Financial management
├── members/                # Member management system (CMS)
│   ├── models.py          # Member model with User link
│   ├── signals.py         # Auto-sync User and Member
│   └── views.py           # Member CRUD operations
├── members_portal/         # Members-facing portal
│   ├── views.py           # Member dashboard, profile, etc.
│   └── urls.py            # Members portal routes
├── public_site/            # Public website
│   ├── views.py           # Public pages
│   └── urls.py            # Public routes
├── reports/                # Reporting and analytics
├── ruwe_administration/    # Church administration
├── visitors/               # Visitor management
├── templates/              # HTML templates
├── static/                 # CSS, JavaScript, images
├── media/                  # Uploaded files (photos, documents)
└── ruweholyghostchurch/    # Main project settings
    ├── settings.py        # Django settings with subdomain config
    ├── middleware.py      # Subdomain detection middleware
    ├── urls.py            # Default URL config
    ├── cms_urls.py        # CMS routes (cms.*)
    ├── members_urls.py    # Members portal routes (members.*)
    └── public_urls.py     # Public website routes (www.*)
```

## Key Models

### Member Model
- **User Link**: `OneToOneField` to Django User (optional, null=True)
- **Personal Information**: Name, gender, date of birth, marital status
- **Contact Details**: Phone, email, location, education level
- **Church Information**: Home and town church assignments
- **Baptismal Data**: Baptismal names and dates
- **Emergency Contacts**: Up to 2 emergency contacts
- **Profile Management**: Photo upload or URL
- **Custom Fields**: JSON field for flexible data storage

### Church Structure
- **Diocese**: Top-level church organization
- **Pastorate**: Mid-level church subdivision
- **Church**: Individual church branches

### Document Management
- **MemberDocument**: File attachments for members
- **Document Types**: Baptism certificates, tithe cards, etc.
- **File Storage**: Organized by member and document type

## Subdomain Routing

The system uses a custom middleware (`SubdomainMiddleware`) to detect the subdomain and route to the appropriate URL configuration:

```python
# Development (localhost/Replit) → defaults to CMS
# cms.ruweholyghostchurch.org → cms_urls.py (Admin CMS)
# members.ruweholyghostchurch.org → members_urls.py (Members Portal)
# ruweholyghostchurch.org (or www) → public_urls.py (Public Website)
```

### Session Management
- Sessions are shared across subdomains (`.ruweholyghostchurch.org`)
- Cookie name: `ruwehg_sessionid`
- Members can login on members portal, admins on CMS

## Signal Workflows

### 1. Superuser Creation → Member Profile
```python
# When superuser is created via createsuperuser command:
User created (is_superuser=True)
  → Signal: create_member_for_superuser
  → Member profile auto-created with basic info
  → Linked via user field
  → Appears in Members list with is_staff=True
```

### 2. Member Registration → User Account
```python
# When admin registers a member:
Member created via CMS form
  → Signal: create_user_for_member
  → User account auto-created
  → Password set as unusable
  → is_active=True (can reset password)
  → Email sent with password reset instructions
```

### 3. Member Account Activation
```python
# Member activates account:
Member clicks "Forgot Password" on members portal
  → Receives password reset email
  → Sets new password
  → Can login to members.ruweholyghostchurch.org
  → Views personal dashboard, attendance, contributions
```

## Security Features

- **CSRF Protection**: Enabled for all POST requests
- **Secure File Upload**: Validated file types and sizes
- **User Authentication**: Django's built-in auth system
- **SQL Injection Prevention**: Django ORM
- **Password Security**: Django's password hashing (PBKDF2)
- **Session Security**: Secure cookies in production
- **Subdomain Isolation**: Separate URL configs per subdomain

## API Endpoints

The system provides REST API endpoints for:
- Member CRUD operations
- Attendance management
- Financial transactions
- Visitor tracking
- Equipment management

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations [app_name]
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

### Testing Subdomain Routing (Local)
```bash
# Add to /etc/hosts (Linux/Mac) or C:\Windows\System32\drivers\etc\hosts (Windows):
127.0.0.1 cms.localhost
127.0.0.1 members.localhost
127.0.0.1 www.localhost

# Then access:
# http://cms.localhost:5000 → CMS
# http://members.localhost:5000 → Members Portal
# http://www.localhost:5000 → Public Website
```

## Deployment

The application is configured for deployment with:
- **WhiteNoise**: Static file serving
- **Gunicorn**: Production WSGI server
- **Environment-based Config**: Database URL, secrets via env vars
- **CORS Headers**: API access configuration
- **Subdomain Support**: Middleware-based routing

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
EMAIL_HOST_USER=smtp-email@example.com
EMAIL_HOST_PASSWORD=smtp-password
ALLOWED_HOSTS=.ruweholyghostchurch.org
```

## Member Portal Features (Planned)

- View personal profile information
- Update profile details (limited fields)
- View attendance history
- View giving/contribution history
- View church announcements
- Download personal documents
- Family member connections
- Event registration

## Public Website Features (Planned)

- Homepage with church mission/vision
- About us and church history
- Service times and locations
- Leadership structure (clergy)
- Events calendar
- Contact form
- News/blog section
- Sermon archive

## Troubleshooting

### Members Not Appearing in List
- Ensure User and Member are properly linked
- Check signals are loaded (members/apps.py has ready() method)
- Verify migrations are applied: `python manage.py migrate`

### Member Cannot Login
- Ensure Member has email address
- Check User account was created (Django Admin → Users)
- Verify password reset email was sent
- Check email configuration in settings.py

### Subdomain Not Working
- Verify DNS configuration (cPanel)
- Check ALLOWED_HOSTS includes subdomain
- Verify middleware is in MIDDLEWARE list
- Check CSRF_TRUSTED_ORIGINS includes subdomain

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For technical support or feature requests, please contact the church administration.
- **Email**: [lawifirst@gmail.com]
- **WhatsApp/Phone**: [https://wa.me/254708581688]
- **Documentation**: See project wiki
- **Issues**: Use GitHub Issues for bug reports

## License

This project is proprietary software developed for Ruwe Holy Ghost Church. All rights reserved.

---

**Built with ❤️ for Ruwe Holy Ghost Church**

---

**Ruwe Holy Ghost Church Management System** - *Empowering church administration through modern technology*

---

## Recent Updates (October 2025)

### Architecture Restructuring
- ✅ Implemented multi-subdomain architecture
- ✅ Linked Django User and Member models
- ✅ Created auto-sync signals for User-Member relationship
- ✅ Built Members Portal foundation
- ✅ Built Public Website foundation
- ✅ Configured subdomain routing middleware

### User & Member Integration
- ✅ Added OneToOne User field to Member model
- ✅ Auto-create Member when superuser is created
- ✅ Auto-create User when Member is registered
- ✅ Password reset flow for member account activation

### Next Steps
- 🚧 Complete Members Portal dashboard and features
- 🚧 Build out Public Website pages and content
- 🚧 Create member-facing templates
- 🚧 Implement member profile editing
- 🚧 Add member attendance and giving views
