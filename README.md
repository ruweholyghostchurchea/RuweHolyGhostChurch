
# RuweHolyGhostChurch Management System

A comprehensive church management system for Ruwe Holy Ghost Church EA, designed to streamline church operations and member management. Uses PostgreSQL database.

## About Ruwe Holy Ghost Church

The Ruwe Holy Ghost Church traces its origin back to 1906/07 and was founded by Alfayo Odongo Mango and Lawi Obonyo Ongwek in Musanda LUO near the border of former Western and Nyanza Provinces in the early 1930s. The current main headquarters is at Ruwe, Siaya County but there's another divide headquartered at Kisumu.

## Features

### 🏛️ Church Structure Management
- **Diocese Management**: Organize church hierarchy at the diocese level
- **Pastorate Management**: Manage pastorate subdivisions
- **Church Management**: Individual church branch administration

### 👥 Member Management
- **Comprehensive Member Profiles**: Store detailed member information including:
  - Personal details (name, gender, marital status, education level)
  - Contact information (phone, email, location)
  - Baptismal information and church membership history
  - Job/occupation and income details
  - Emergency contacts (up to 2 contacts per member)
  - Profile photo management (upload or URL)
  - Custom fields for flexible data storage
- **Document Management**: Attach important documents like:
  - Baptism certificates
  - Annual tithe cards
  - ID documents
  - Medical records
  - Membership certificates
- **Church Hierarchy Assignment**: Link members to home and town churches
- **Member Groups**: Categorize members as Youth, Adult, Elder, or Clergy

### 🚪 Visitor Management
- Track church visitors and their information
- Monitor visitor engagement and follow-up

### 📊 Attendance Tracking
- Record service attendance for members
- Generate attendance reports and analytics
- Track attendance patterns and trends

### 💰 Financial Management
- Manage church finances including:
  - Tithes and offerings
  - Donations and pledges
  - Financial reporting and analytics

### 📱 Bulk SMS System
- Send bulk messages to members
- Communication management for church announcements
- Member group-based messaging

### 🛠️ Equipment Management
- Track church equipment and assets
- Maintenance schedules and records
- Equipment allocation and usage

### 📈 Reports & Analytics
- Generate comprehensive reports on:
  - Member statistics
  - Attendance patterns
  - Financial summaries
  - Growth analytics

### ⚙️ Church Settings
- Configurable church-specific settings
- System preferences and customization

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript with Bootstrap
- **File Storage**: Local file system with media handling
- **Authentication**: Django's built-in authentication system

## Installation & Setup

### Prerequisites
- Python 3.12+
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

3. **Database setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver 0.0.0.0:5000
   ```

6. **Access the application**:
   - Web interface: `http://localhost:5000`
   - Admin panel: `http://localhost:5000/admin`

## Project Structure

```
ruweholyghostchurch/
├── attendance/          # Attendance tracking module
├── bulk_sms/           # SMS communication system
├── church_settings/    # Church configuration settings
├── church_structure/   # Diocese, Pastorate, Church management
├── dashboard/          # Main dashboard and analytics
├── equipment/          # Equipment and asset management
├── finance/            # Financial management
├── members/            # Member management system
├── reports/            # Reporting and analytics
├── visitors/           # Visitor management
├── templates/          # HTML templates
├── static/             # CSS, JavaScript, images
├── media/              # Uploaded files (photos, documents)
└── ruweholyghostchurch/ # Main project settings
```

## Key Models

### Member Model
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

## API Endpoints

The system provides REST API endpoints for:
- Member CRUD operations
- Attendance management
- Financial transactions
- Visitor tracking
- Equipment management

## Security Features

- CSRF protection enabled
- Secure file upload handling
- User authentication and authorization
- SQL injection prevention through Django ORM

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

## Deployment

The application is configured for deployment on Replit with:
- WhiteNoise for static file serving
- Gunicorn as WSGI server
- Environment-based configuration
- CORS headers for API access

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
