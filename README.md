
# RuweHolyGhostChurch Management System

A comprehensive church management system for Ruwe Holy Ghost Church EA, designed to streamline church operations and member management.

## About Ruwe Holy Ghost Church

The Ruwe Holy Ghost Church traces its origin back to 1906/07 and was founded by Alfayo Odongo Mango and Lawi Obonyo Ongwek in Musanda LUO near the border of former Western and Nyanza Provinces in the early 1930s. The current main headquarters is at Ruwe, Siaya County but there's another divide headquartered at Kisumu.

**Important Note**: Our church observes Saturday as the Sabbath day, following biblical tradition.

## Features

### Core Modules
- **Dashboard**: Overview of church statistics, recent activities, and upcoming events
- **Members Management**: Complete member database with personal information and church involvement
- **Visitors Management**: Track and follow up with church visitors
- **Attendance Management**: Record and analyze service attendance patterns
- **Finance Management**: Track offerings, tithes, and church financial records
- **Bulk SMS**: Send mass communications to members and visitors
- **Equipment Management**: Inventory and maintenance of church equipment
- **Reports**: Generate comprehensive reports for church administration
- **Church Settings**: Configure church information, service times, and system preferences

### Key Features
- **Saturday Sabbath Focus**: All service types and scheduling reflect Saturday Sabbath observance
- **Professional Dark Theme**: Clean, modern interface with professional dark color scheme
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Statistics**: Live dashboard with member counts, attendance, and financial data
- **Activity Tracking**: Monitor recent church activities and member engagement

## Technology Stack

- **Backend**: Django 5.2.4 (Python web framework)
- **Database**: SQLite (default, easily configurable to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Custom responsive design with FontAwesome icons
- **Styling**: Professional dark theme with red accent colors

## Church Structure Management

The system includes a comprehensive hierarchical church structure management module:

### Hierarchy Levels
1. **Headquarters** - Located at Ruwe Sublocation, Siaya County (led by Archbishop)
2. **Diocese** - Regional divisions headed by Bishops (12+ across Kenya, Uganda, Tanzania)
3. **Pastorate** - Groups of 2+ churches headed by Pastors (75+ total)
4. **Church** - Individual church units headed by Church Teachers (200+ total)

### Features
- **Cascading Dropdowns**: Dynamic selection of Diocese → Pastorate → Church
- **Multi-Country Support**: Kenya (main), Uganda, and Tanzania
- **Administrative Controls**: Add new dioceses, pastorates, and churches
- **Comprehensive Records**: Contact information for all leadership levels
- **Real-time Statistics**: Live counts and hierarchical overview

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ruweholyghostchurch
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver 0.0.0.0:5000
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`
   - Use the admin interface at `http://localhost:5000/admin`

## Project Structure

```
ruweholyghostchurch/
├── attendance/          # Attendance management module
├── bulk_sms/           # SMS communication module
├── church_settings/    # Church configuration module
├── dashboard/          # Main dashboard module
├── equipment/          # Equipment inventory module
├── finance/           # Financial management module
├── members/           # Member management module
├── reports/           # Reporting module
├── visitors/          # Visitor management module
├── templates/         # HTML templates
├── static/           # CSS, JavaScript, and images
└── ruweholyghostchurch/ # Main Django project settings
```

## Service Types

The system supports various service types tailored for Saturday Sabbath observance:
- Saturday Morning Sabbath
- Saturday Evening Service
- Wednesday Service
- Prayer Meeting
- Bible Study
- Youth Service
- Special Events

## Customization

### Church Information
Update church details in the Church Settings module:
- Church name and contact information
- Pastor details
- Service times (configured for Saturday Sabbath)
- Social media links

### Branding
- Logo and banner images can be uploaded through Church Settings
- Color scheme uses professional dark theme with red accents
- FontAwesome icons throughout the interface

## Database Models

Key models include:
- **Member**: Complete member profiles with contact and spiritual information
- **Visitor**: Visitor tracking and follow-up management
- **Service**: Service scheduling and management
- **Attendance**: Service attendance records
- **Offering**: Financial contribution tracking
- **ChurchInfo**: Church configuration and settings

## Security Features

- Django's built-in security features
- CSRF protection
- SQL injection prevention
- Secure password validation
- Admin interface protection

## Future Enhancements

- Email integration for automated communications
- Advanced reporting with charts and graphs
- Mobile app development
- Integration with external SMS providers
- Multi-location church support
- Advanced member engagement tracking

## Support

For technical support or feature requests, please contact the church administration or create an issue in the project repository.

## License

This project is licensed under the terms specified in the LICENSE file.
