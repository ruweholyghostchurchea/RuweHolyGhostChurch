
from django.db import models
from church_structure.models import Diocese, Pastorate, Church
import json
import random
import string

class Member(models.Model):
    USER_GROUP_CHOICES = [
        ('Youth', 'Youth'),
        ('Adult', 'Adult'),
        ('Elder', 'Elder'),
    ]
    
    MEMBER_ROLES = [
        ('regular_member', 'Regular Member'),
        ('singer', 'Singer'),
        ('drum_percussionist', 'Drum Percussionist'),
        ('shaker_percussionist', 'Shaker Percussionist'),
        ('synod_representative', 'Synod Representative'),
        ('clergy', 'Clergy'),
    ]
    
    CHURCH_CLERGY_ROLES = [
        ('church_teacher_wife', "Teacher's Wife"),
        ('church_teacher_husband', "Teacher's Husband"),
        ('church_teacher', 'Teacher'),
        ('pastorate_woman_leader', 'Woman Leader'),
        ('pastorate_woman_leader_husband', "Woman Leader's Husband"),
        ('pastorate_division_wife', "Division's Wife"),
        ('pastorate_division_husband', "Division's Husband"),
        ('pastorate_division', 'Division'),
        ('pastorate_lay_reader_wife', "Lay Reader's Wife"),
        ('pastorate_lay_reader', 'Lay Reader'),
        ('pastorate_pastor_wife', "Pastor's Wife"),
        ('pastorate_pastor', 'Pastor'),
        ('diocese_bishop_wife', "Bishop's Wife"),
        ('diocese_bishop', 'Bishop'),
        ('dean_archbishop_wife', "Archbishop's Wife"),
        ('dean_archbishop', 'Archbishop'),
    ]
    
    SPECIAL_CLERGY_ROLES = [
        ('dean_king', 'King'),
        ('dean_king_wife', "King's Wife"),
        ('dean_archdeacon', 'Archdeacon'),
        ('dean_archdeacon_wife', "Archdeacon's Wife"),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
    ]
    
    # Removed LOCATION_CHOICES - now using text field with autocomplete
    
    EDUCATION_LEVEL_CHOICES = [
        ('primary', 'Primary Education'),
        ('secondary', 'Secondary Education'),
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('other', 'Other'),
    ]
    
    MEMBERSHIP_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Transferred', 'Transferred'),
        ('Left/Quit', 'Left/Quit'),
        ('Dead', 'Dead'),
    ]
    
    PWD_TYPE_CHOICES = [
        ('prefer_not_to_say', 'Prefer not to say'),
        ('blind_low_vision', 'Blind or low vision'),
        ('cognitive_autism', 'Cognitive or Autism'),
        ('cripple_mobility', 'Cripple or Mobility problem'),
        ('chronic_invisible', 'Chronic/Invisible Disability'),
        ('deaf_hearing', 'Deaf or Hearing difficulty'),
        ('mute_speaking', 'Mute or Speaking difficulty'),
        ('mental_health', 'Mental Health Condition'),
        ('other', 'Other (Please specify if you are comfortable)'),
    ]
    
    JOB_CATEGORIES = [
        ('agriculture_agribusiness', 'Agriculture & Agribusiness'),
        ('healthcare_medical', 'Healthcare & Medical'),
        ('education_training', 'Education & Training'),
        ('finance_banking_insurance', 'Finance, Banking & Insurance'),
        ('ict', 'Information & Communication Technology (ICT)'),
        ('creative_media_digital', 'Creative, Media & Digital Content'),
        ('sales_retail_customer_service', 'Sales, Retail & Customer Service'),
        ('hospitality_tourism_events', 'Hospitality, Tourism & Events'),
        ('construction_infrastructure', 'Construction & Infrastructure'),
        ('manufacturing_production', 'Manufacturing & Production'),
        ('transportation_logistics', 'Transportation & Logistics'),
        ('trades_skilled_labour', 'Trades & Skilled Labour (Jua Kali & formal)'),
        ('legal_compliance_governance', 'Legal, Compliance & Governance'),
        ('public_sector_civil_service_ngos', 'Public Sector, Civil Service & NGOs'),
        ('real_estate_property', 'Real Estate & Property'),
        ('energy_utilities_environment', 'Energy, Utilities & Environment'),
        ('agriculture_value_chain_agritech', 'Agriculture Value-Chain & Agritech'),
        ('automotive_mechanical', 'Automotive & Mechanical'),
        ('personal_services_beauty', 'Personal Services & Beauty'),
        ('security_protective_services', 'Security & Protective Services'),
        ('gig_economy_freelance_remote', 'Gig Economy, Freelance & Remote Work'),
        ('science_research_higher_education', 'Science, Research & Higher Education'),
        ('entrepreneurship_small_business', 'Entrepreneurship & Small Business'),
        ('creative_entrepreneurship_arts', 'Creative Entrepreneurship & Arts'),
        ('sports_recreation_fitness', 'Sports, Recreation & Fitness'),
    ]
    
    JOB_CHOICES = [
        # Agriculture & Agribusiness
        ('smallholder_farmer', 'Smallholder farmer (maize, vegetables, tea, coffee, horticulture)'),
        ('agronomist_extension_officer', 'Agronomist / extension officer'),
        ('farm_manager', 'Farm manager'),
        ('livestock_farmer', 'Livestock farmer (dairy, poultry, goats)'),
        ('agribusiness_entrepreneur', 'Agribusiness entrepreneur (value-added products)'),
        ('agro_inputs_salesperson', 'Agro-inputs salesperson (seeds, fertilisers)'),
        ('agricultural_technician_vet_assistant', 'Agricultural technician / vet assistant'),
        ('produce_trader_market_agent', 'Produce trader / market agent'),
        ('food_processing_operator', 'Food processing operator'),
        ('irrigation_technician', 'Irrigation technician'),
        
        # Healthcare & Medical
        ('nurse_registered', 'Nurse (registered nurse)'),
        ('clinical_officer_medical_officer', 'Clinical officer / medical officer'),
        ('community_health_volunteer_chw', 'Community health volunteer / CHW'),
        ('pharmacist_pharmaceutical_technologist', 'Pharmacist / pharmaceutical technologist'),
        ('lab_technician_radiographer', 'Lab technician / radiographer'),
        ('physiotherapist_occupational_therapist', 'Physiotherapist / occupational therapist'),
        ('medical_records_officer_health_administrator', 'Medical records officer / health administrator'),
        ('health_educator_public_health_officer', 'Health educator / public health officer'),
        ('dental_therapist_dental_assistant', 'Dental therapist / dental assistant'),
        ('xray_imaging_technician', 'X-ray / imaging technician'),
        ('nutritionist_dietitian', 'Nutritionist / dietitian'),
        ('psychologist_mental_performance_coach', 'Psychologist / mental performance coach'),
        ('orthopaedic_technologist', 'Orthopaedic technologist (Prosthetist / Orthotist)'),
        
        # Education & Training
        ('primary_school_teacher', 'Primary school teacher'),
        ('secondary_school_teacher', 'Secondary school teacher'),
        ('university_lecturer_tutor', 'University lecturer / tutor'),
        ('early_childhood_educator', 'Early childhood educator (ECDE teacher)'),
        ('pe_teacher_sports_coordinator', 'PE teacher / school sports coordinator'),
        ('private_tutor', 'Private tutor (exam prep — KCPE/KCSE/CBC)'),
        ('curriculum_developer_instructional_designer', 'Curriculum developer / instructional designer'),
        ('training_coordinator_corporate_trainer', 'Training coordinator / corporate trainer'),
        ('librarian_learning_resources_officer', 'Librarian / learning resources officer'),
        ('education_administrator_headteacher', 'Education administrator / headteacher'),
        
        # Finance, Banking & Insurance
        ('bank_teller_customer_service_rep', 'Bank teller / customer service rep'),
        ('accountant_bookkeeper', 'Accountant / bookkeeper'),
        ('credit_analyst_loan_officer', 'Credit analyst / loan officer'),
        ('financial_analyst_investment_officer', 'Financial analyst / investment officer'),
        ('microfinance_officer', 'Microfinance officer'),
        ('insurance_agent_underwriter', 'Insurance agent / underwriter'),
        ('tax_consultant_compliance_officer', 'Tax consultant / compliance officer'),
        ('treasury_cash_management_officer', 'Treasury / cash management officer'),
        ('auditor', 'Auditor'),
        
        # Information & Communication Technology (ICT)
        ('software_developer', 'Software developer (web / mobile)'),
        ('data_analyst_business_intelligence', 'Data analyst / business intelligence analyst'),
        ('network_engineer_system_administrator', 'Network engineer / system administrator'),
        ('it_support_helpdesk_technician', 'IT support / helpdesk technician'),
        ('ux_ui_designer_product_designer', 'UX/UI designer / product designer'),
        ('devops_engineer_cloud_engineer', 'DevOps engineer / cloud engineer'),
        ('cybersecurity_analyst_soc_analyst', 'Cybersecurity analyst / SOC analyst'),
        ('qa_tester_automation_tester', 'QA tester / automation tester'),
        ('ai_ml_engineer', 'AI/ML engineer (entry to advanced)'),
        
        # Creative, Media & Digital Content
        ('graphic_designer', 'Graphic designer'),
        ('content_writer_copywriter_blogger', 'Content writer / copywriter / blogger'),
        ('social_media_manager_digital_marketer', 'Social media manager / digital marketer'),
        ('videographer_video_editor', 'Videographer / video editor'),
        ('photographer', 'Photographer'),
        ('animator_motion_graphics_artist', 'Animator / motion graphics artist'),
        ('radio_presenter_podcaster', 'Radio presenter / podcaster'),
        ('journalist_news_reporter', 'Journalist / news reporter'),
        ('pr_communications_officer', 'PR / communications officer'),
        
        # Sales, Retail & Customer Service
        ('retail_shop_attendant_cashier', 'Retail shop attendant / cashier'),
        ('sales_marketing_representative', 'Sales and marketing representative / field sales agent'),
        ('store_manager_merchandiser', 'Store manager / merchandiser'),
        ('ecommerce_operator', 'E-commerce operator (online seller)'),
        ('customer_service_agent_call_centre', 'Customer service agent / call centre rep'),
        ('market_vendor_hawker', 'Market vendor / hawker'),
        ('wholesale_trader_distributor', 'Wholesale trader / distributor'),
        ('buying_clerk_procurement_assistant', 'Buying clerk / procurement assistant'),
        
        # Hospitality, Tourism & Events
        ('hotel_receptionist_front_desk', 'Hotel receptionist / front desk'),
        ('housekeeper_cleaner', 'Housekeeper / cleaner'),
        ('chef_cook_sous_chef', 'Chef / cook / sous-chef'),
        ('restaurant_waiter_barista', 'Restaurant waiter / barista'),
        ('tour_guide_travel_agent', 'Tour guide / travel agent'),
        ('event_planner_coordinator_manager', 'Event planner / coordinator / manager'),
        ('bartender_mixologist', 'Bartender / mixologist'),
        ('lodge_manager_operations_manager', 'Lodge manager / operations manager'),
        
        # Construction & Infrastructure
        ('civil_engineer_site_engineer', 'Civil engineer / site engineer'),
        ('quantity_surveyor', 'Quantity surveyor'),
        ('architect_drafter', 'Architect / drafter'),
        ('project_manager_construction', 'Project manager (construction)'),
        ('mason_bricklayer', 'Mason / bricklayer'),
        ('carpenter_joiner', 'Carpenter / joiner'),
        ('plumber_pipefitter', 'Plumber / pipefitter'),
        ('electrician_wiring_technician', 'Electrician / wiring technician'),
        ('heavy_equipment_operator', 'Heavy equipment operator (excavator, bulldozer)'),
        
        # Manufacturing & Production
        ('factory_machine_operator', 'Factory machine operator'),
        ('production_supervisor_line_manager', 'Production supervisor / line manager'),
        ('quality_control_qa_inspector', 'Quality control / QA inspector'),
        ('textile_garment_worker_tailor', 'Textile / garment worker / tailor'),
        ('food_processing_technician', 'Food processing technician'),
        ('packaging_operator', 'Packaging operator'),
        ('maintenance_technician_millwright', 'Maintenance technician / millwright'),
        ('plant_manager_production_planner', 'Plant manager / production planner'),
        
        # Transportation & Logistics
        ('matatu_bus_driver', 'Matatu / bus driver'),
        ('boda_boda_rider', 'Boda-boda rider'),
        ('ride_hailing_driver', 'Ride-hailing driver (e.g., Uber, Bolt)'),
        ('truck_driver_long_haul', 'Truck driver / long-haul driver'),
        ('logistics_coordinator_freight_forwarder', 'Logistics coordinator / freight forwarder'),
        ('warehouse_supervisor_storekeeper', 'Warehouse supervisor / storekeeper'),
        ('courier_delivery_rider', 'Courier / delivery rider'),
        ('fleet_manager', 'Fleet manager'),
        ('customs_clearing_agent', 'Customs clearing agent'),
        
        # Trades & Skilled Labour (Jua Kali & formal)
        ('metal_fabricator_welder', 'Metal fabricator / welder'),
        ('motorcycle_automotive_mechanic', 'Motorcycle / automotive mechanic'),
        ('electrician_domestic_industrial', 'Electrician (domestic & industrial)'),
        ('plumber_tiler_painter', 'Plumber / tiler / painter'),
        ('tailor_seamstress', 'Tailor / seamstress'),
        ('carpenter_furniture_maker', 'Carpenter / furniture maker'),
        ('stone_mason_bricklayer', 'Stone mason / bricklayer'),
        ('glass_glazing_technician', 'Glass & glazing technician'),
        
        # Legal, Compliance & Governance
        ('lawyer_advocate', 'Lawyer / advocate'),
        ('paralegal_legal_assistant', 'Paralegal / legal assistant'),
        ('compliance_officer_aml_analyst', 'Compliance officer / AML analyst'),
        ('court_clerk_magistrate_support', 'Court clerk / magistrate support'),
        ('policy_analyst_legislative_assistant', 'Policy analyst / legislative assistant'),
        ('notary_conveyancing_clerk', 'Notary / conveyancing clerk'),
        
        # Public Sector, Civil Service & NGOs
        ('government_administrative_officer', 'Government administrative officer'),
        ('county_government_officer', 'County government officer (health, planning, finance)'),
        ('social_worker_community_development', 'Social worker / community development officer'),
        ('program_officer_project_manager_ngo', 'Program officer / project manager (NGO)'),
        ('monitoring_evaluation_officer', 'Monitoring & evaluation (M&E) officer'),
        ('research_officer_policy_researcher', 'Research officer / policy researcher'),
        ('public_relations_communications_specialist', 'Public relations / communications specialist'),
        ('recruitment_officer_talent_scout', 'Recruitment officer / talent scout'),
        
        # Real Estate & Property
        ('real_estate_agent_broker', 'Real estate agent / broker'),
        ('property_manager_estate_manager', 'Property manager / estate manager'),
        ('valuer_surveyor', 'Valuer / surveyor'),
        ('facilities_manager', 'Facilities manager'),
        ('construction_estimator', 'Construction estimator'),
        ('land_adjudication_registrar_assistant', 'Land adjudication / LAND registrar assistant'),
        
        # Energy, Utilities & Environment
        ('renewable_energy_technician', 'Renewable energy technician (solar)'),
        ('electrical_engineer_power_systems', 'Electrical engineer (power systems)'),
        ('water_sanitation_engineer_technician', 'Water & sanitation engineer / technician'),
        ('environmental_conservation_officer', 'Environmental conservation officer'),
        ('waste_management_supervisor', 'Waste management supervisor'),
        ('gis_remote_sensing_specialist', 'GIS / remote sensing specialist'),
        
        # Agriculture Value-Chain & Agritech
        ('food_processing_entrepreneur', 'Food processing entrepreneur'),
        ('cold_chain_logistics_operator', 'Cold-chain logistics operator'),
        ('agro_export_coordinator', 'Agro-export coordinator'),
        ('agricultural_drone_precision_farming', 'Agricultural drone / precision farming technician'),
        ('farm_to_market_aggregator', 'Farm-to-market aggregator / supply chain manager'),
        
        # Automotive & Mechanical
        ('auto_electrician', 'Auto electrician'),
        ('vehicle_mechanic_diagnostics', 'Vehicle mechanic / diagnostics specialist'),
        ('panel_beater_spray_painter', 'Panel beater / spray painter'),
        ('tyre_technician_alignment_specialist', 'Tyre technician / alignment specialist'),
        ('auto_parts_salesperson', 'Auto parts salesperson'),
        
        # Personal Services & Beauty
        ('barber_hairstylist', 'Barber / hairstylist'),
        ('beautician_cosmetologist', 'Beautician / cosmetologist'),
        ('massage_therapist', 'Massage therapist'),
        ('fitness_instructor_personal_trainer', 'Fitness instructor / personal trainer'),
        ('house_cleaner_domestic_worker', 'House cleaner / domestic worker'),
        ('childcare_provider_nanny', 'Childcare provider / nanny'),
        
        # Security & Protective Services
        ('security_guard_corporate_security', 'Security guard / corporate security officer'),
        ('private_investigator', 'Private investigator'),
        ('firefighter_emergency_responder', 'Firefighter / emergency responder (roles in private sector too)'),
        ('loss_prevention_officer', 'Loss prevention officer (retail)'),
        
        # Gig Economy, Freelance & Remote Work
        ('freelance_developer_designer', 'Freelance developer / designer'),
        ('virtual_assistant_remote_support', 'Virtual assistant / remote customer support'),
        ('online_english_tutor', 'Online English tutor / classroom teacher'),
        ('transcriptionist_translator', 'Transcriptionist / translator'),
        ('micro_task_worker', 'Micro-task worker (task platforms)'),
        
        # Science, Research & Higher Education
        ('laboratory_researcher_scientist', 'Laboratory researcher / scientist'),
        ('research_assistant', 'Research assistant (universities, institutes)'),
        ('clinical_trial_coordinator', 'Clinical trial coordinator'),
        ('data_scientist_statistician', 'Data scientist / statistician'),
        ('environmental_scientist_ecologist', 'Environmental scientist / ecologist'),
        
        # Entrepreneurship & Small Business
        ('kiosk_retail_owner', 'Kiosk / retail owner'),
        ('salon_barber_shop_owner', 'Salon / barber shop owner'),
        ('food_vendor_street_food_stall', 'Food vendor / street food stall owner'),
        ('courier_startup_founder', 'Courier startup founder'),
        ('tech_startup_founder', 'Tech startup founder (apps, SaaS, agri-tech)'),
        
        # Creative Entrepreneurship & Arts
        ('fashion_designer_tailor_entrepreneur', 'Fashion designer / tailor entrepreneur'),
        ('musician_audio_producer', 'Musician / audio producer'),
        ('craft_maker_artisan', 'Craft maker / artisan (baskets, carvings)'),
        ('film_documentary_maker_producer', 'Film & documentary maker / producer'),
        
        # Sports, Recreation & Fitness
        ('sports_administrator_club_manager', 'Sports administrator / club manager / team manager'),
        ('referee_umpire_match_official', 'Referee / umpire / match official'),
        ('sports_coach', 'Sports coach'),
        ('sports_football', 'Sports football'),
        ('sports_athletics', 'Sports athletics'),
        ('sports_rugby', 'Sports rugby'),
        ('sports_basketball', 'Sports basketball'),
        ('sports_boxing_taekwondo', 'Sports boxing / taekwondo'),
        ('fitness_instructor_gym_trainer', 'Fitness instructor / gym trainer / group class instructor (yoga, aerobics, spin)'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    identifier = models.CharField(max_length=20, unique=True, blank=True, help_text="Auto-generated unique identifier")
    user_group = models.CharField(max_length=20, choices=USER_GROUP_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='single')
    location = models.CharField(max_length=200, help_text="Location (city, country)")
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, default='other')
    
    # Member Roles (Multi-select via JSON field)
    member_roles = models.JSONField(default=list, help_text="List of member roles")
    church_clergy_roles = models.JSONField(default=list, blank=True, help_text="Church/Dean clergy roles (only if clergy role is selected)")
    special_clergy_roles = models.JSONField(default=list, blank=True, help_text="Special clergy roles (only if clergy role is selected)")
    
    phone_number = models.CharField(max_length=20, unique=True)
    email_address = models.EmailField(blank=True, unique=True)
    
    # Job/Occupation Information
    job_occupations = models.JSONField(default=list, help_text="List of selected job/occupation roles")
    income_details = models.TextField(blank=True, help_text="Additional income and occupation details")
    
    # Baptismal Information
    baptismal_first_name = models.CharField(max_length=100)
    baptismal_last_name = models.CharField(max_length=100)
    date_baptized = models.DateField()
    date_joined_religion = models.DateField()
    date_joined_app = models.DateField(auto_now_add=True)
    
    # Home Church Structure (Required)
    user_home_diocese = models.ForeignKey(Diocese, on_delete=models.CASCADE, related_name='home_members')
    user_home_pastorate = models.ForeignKey(Pastorate, on_delete=models.CASCADE, related_name='home_members')
    user_home_church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name='home_members')
    
    # Town Church Structure (Optional - for work/education/treatment)
    user_town_diocese = models.ForeignKey(Diocese, on_delete=models.SET_NULL, null=True, blank=True, related_name='town_members')
    user_town_pastorate = models.ForeignKey(Pastorate, on_delete=models.SET_NULL, null=True, blank=True, related_name='town_members')
    user_town_church = models.ForeignKey(Church, on_delete=models.SET_NULL, null=True, blank=True, related_name='town_members')
    
    # Emergency Contacts
    emergency_contact_1_name = models.CharField(max_length=100, blank=True)
    emergency_contact_1_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_1_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_1_email = models.EmailField(blank=True)
    
    emergency_contact_2_name = models.CharField(max_length=100, blank=True)
    emergency_contact_2_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_2_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_2_email = models.EmailField(blank=True)
    
    # Family Details (Optional - searchable relationships)
    father = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_father')
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_mother')
    guardian = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_guardian')
    brother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='siblings_as_brother')
    sister = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='siblings_as_sister')
    uncle = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='nephews_nieces_as_uncle')
    aunt = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='nephews_nieces_as_aunt')
    friend = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='friends')
    
    # Membership Status
    membership_status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS_CHOICES, default='Active')
    
    # Person with Disability (PWD)
    is_pwd = models.BooleanField(default=False, verbose_name="Person with Disability")
    pwd_type = models.CharField(max_length=50, choices=PWD_TYPE_CHOICES, blank=True, verbose_name="Type of Disability")
    pwd_other_description = models.TextField(blank=True, verbose_name="Other Disability Description")
    
    # Staff Status
    is_staff = models.BooleanField(default=False, verbose_name="Staff Member")
    
    # Hand Ordination Status
    is_ordained = models.BooleanField(default=False, verbose_name="Ordained Member")
    
    # Profile Photo
    profile_photo = models.URLField(blank=True, null=True, help_text='Member photo URL')
    profile_photo_url = models.URLField(blank=True, help_text="Alternative to uploading a photo")
    
    # Custom Fields (JSON field for flexible custom data)
    custom_fields = models.JSONField(default=dict, blank=True, help_text="Store custom member data as key-value pairs")
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
    
    def generate_identifier(self):
        """Generate a unique identifier for the member"""
        while True:
            # Generate random 4-character segments
            segment1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            segment2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            segment3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            identifier = f"RUWE-{segment1}-{segment2}-{segment3}"
            
            # Check if this identifier already exists
            if not Member.objects.filter(identifier=identifier).exists():
                return identifier

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.generate_identifier()
        
        # Ensure regular_member role is always present
        if 'regular_member' not in self.member_roles:
            self.member_roles.append('regular_member')
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def baptismal_full_name(self):
        return f"{self.baptismal_first_name} {self.baptismal_last_name}"
    
    @property
    def home_church_hierarchy(self):
        return f"{self.user_home_diocese.name} > {self.user_home_pastorate.name} > {self.user_home_church.name}"
    
    @property
    def town_church_hierarchy(self):
        if self.user_town_church:
            return f"{self.user_town_diocese.name} > {self.user_town_pastorate.name} > {self.user_town_church.name}"
        return "Not assigned"
    
    @property
    def display_photo(self):
        """Return the profile photo URL or uploaded photo URL"""
        if self.profile_photo:
            return self.profile_photo.url
        elif self.profile_photo_url:
            return self.profile_photo_url
        return None
    
    def get_custom_field(self, key, default=None):
        """Get a custom field value by key"""
        return self.custom_fields.get(key, default)
    
    def set_custom_field(self, key, value):
        """Set a custom field value"""
        self.custom_fields[key] = value
    
    def has_role(self, role):
        """Check if member has a specific role"""
        return role in self.member_roles
    
    def add_role(self, role):
        """Add a role to the member"""
        if role not in self.member_roles:
            self.member_roles.append(role)
    
    def remove_role(self, role):
        """Remove a role from the member"""
        if role in self.member_roles:
            self.member_roles.remove(role)
    
    def has_clergy_role(self, clergy_role):
        """Check if member has a specific clergy role"""
        return clergy_role in self.church_clergy_roles or clergy_role in self.special_clergy_roles
    
    def add_church_clergy_role(self, role):
        """Add a church clergy role to the member"""
        if role not in self.church_clergy_roles:
            self.church_clergy_roles.append(role)
    
    def add_special_clergy_role(self, role):
        """Add a special clergy role to the member"""
        if role not in self.special_clergy_roles:
            self.special_clergy_roles.append(role)
    
    @property
    def is_clergy(self):
        """Return True if member has clergy role"""
        return 'clergy' in self.member_roles
    
    @property
    def display_roles(self):
        """Return a comma-separated list of member roles for display"""
        role_labels = []
        for role_code in self.member_roles:
            for code, label in self.MEMBER_ROLES:
                if code == role_code:
                    role_labels.append(label)
                    break
        return ', '.join(role_labels) if role_labels else 'Regular Member'
    
    @property
    def display_clergy_roles(self):
        """Return a comma-separated list of clergy roles for display"""
        clergy_labels = []
        
        # Church clergy roles
        for role_code in self.church_clergy_roles:
            for code, label in self.CHURCH_CLERGY_ROLES:
                if code == role_code:
                    clergy_labels.append(label)
                    break
        
        # Special clergy roles
        for role_code in self.special_clergy_roles:
            for code, label in self.SPECIAL_CLERGY_ROLES:
                if code == role_code:
                    clergy_labels.append(label)
                    break
        
        return ', '.join(clergy_labels) if clergy_labels else None
    
    @property
    def is_active(self):
        """Return True if member status is Active"""
        return self.membership_status == 'Active'
    
    @property
    def is_archived(self):
        """Return True if member should be archived"""
        return self.membership_status in ['Left/Quit', 'Dead']
    
    @property
    def display_jobs(self):
        """Return a comma-separated list of job/occupation roles for display"""
        job_labels = []
        for job_code in self.job_occupations:
            for code, label in self.JOB_CHOICES:
                if code == job_code:
                    job_labels.append(label)
                    break
        return ', '.join(job_labels) if job_labels else 'Not specified'


class MemberDocument(models.Model):
    DOCUMENT_TYPES = [
        ('baptism_certificate', 'Baptism Certificate'),
        ('annual_tithe_card', 'Annual Tithe Card'),
        ('id_document', 'ID Document'),
        ('medical_record', 'Medical Record'),
        ('membership_certificate', 'Membership Certificate'),
        ('other', 'Other'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document_file = models.FileField(upload_to='member_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=100, blank=True)  # Could be linked to User model later
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Member Document'
        verbose_name_plural = 'Member Documents'
    
    def __str__(self):
        return f"{self.member.full_name} - {self.title}"
