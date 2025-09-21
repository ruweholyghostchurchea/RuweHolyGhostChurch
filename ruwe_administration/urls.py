from django.urls import path
from . import views

app_name = 'ruwe_administration'

urlpatterns = [
    # Main index page
    path('', views.administration_index, name='index'),
    
    # =========================
    # CHURCH LEVEL URLS (5)
    # =========================
    
    # Church Main Office
    path('church/main/<int:church_id>/', views.church_main_office_detail, name='church_main_detail'),
    path('church/main/<int:church_id>/add/', views.church_main_office_add, name='church_main_add'),
    path('church/main/<int:pk>/edit/', views.church_main_office_edit, name='church_main_edit'),
    
    # Church Youth Office
    path('church/youth/<int:church_id>/', views.church_youth_office_detail, name='church_youth_detail'),
    path('church/youth/<int:church_id>/add/', views.church_youth_office_add, name='church_youth_add'),
    path('church/youth/<int:pk>/edit/', views.church_youth_office_edit, name='church_youth_edit'),
    
    # Church Development Office
    path('church/development/<int:church_id>/', views.church_development_office_detail, name='church_development_detail'),
    path('church/development/<int:church_id>/add/', views.church_development_office_add, name='church_development_add'),
    path('church/development/<int:pk>/edit/', views.church_development_office_edit, name='church_development_edit'),
    
    # Church Travel Office
    path('church/travel/<int:church_id>/', views.church_travel_office_detail, name='church_travel_detail'),
    path('church/travel/<int:church_id>/add/', views.church_travel_office_add, name='church_travel_add'),
    path('church/travel/<int:pk>/edit/', views.church_travel_office_edit, name='church_travel_edit'),
    
    # Church Disciplinary Office
    path('church/disciplinary/<int:church_id>/', views.church_disciplinary_office_detail, name='church_disciplinary_detail'),
    path('church/disciplinary/<int:church_id>/add/', views.church_disciplinary_office_add, name='church_disciplinary_add'),
    path('church/disciplinary/<int:pk>/edit/', views.church_disciplinary_office_edit, name='church_disciplinary_edit'),
    
    # =========================
    # PASTORATE LEVEL URLS (3)
    # =========================
    
    # Pastorate Main Office
    path('pastorate/main/<int:pastorate_id>/', views.pastorate_main_office_detail, name='pastorate_main_detail'),
    path('pastorate/main/<int:pastorate_id>/add/', views.pastorate_main_office_add, name='pastorate_main_add'),
    path('pastorate/main/<int:pk>/edit/', views.pastorate_main_office_edit, name='pastorate_main_edit'),
    
    # Pastorate Youth Office
    path('pastorate/youth/<int:pastorate_id>/', views.pastorate_youth_office_detail, name='pastorate_youth_detail'),
    path('pastorate/youth/<int:pastorate_id>/add/', views.pastorate_youth_office_add, name='pastorate_youth_add'),
    path('pastorate/youth/<int:pk>/edit/', views.pastorate_youth_office_edit, name='pastorate_youth_edit'),
    
    # Pastorate Teachers Office
    path('pastorate/teachers/<int:pastorate_id>/', views.pastorate_teachers_office_detail, name='pastorate_teachers_detail'),
    path('pastorate/teachers/<int:pastorate_id>/add/', views.pastorate_teachers_office_add, name='pastorate_teachers_add'),
    path('pastorate/teachers/<int:pk>/edit/', views.pastorate_teachers_office_edit, name='pastorate_teachers_edit'),
    
    # =========================
    # DIOCESE LEVEL URLS (3)
    # =========================
    
    # Diocese Main Office
    path('diocese/main/<int:diocese_id>/', views.diocese_main_office_detail, name='diocese_main_detail'),
    path('diocese/main/<int:diocese_id>/add/', views.diocese_main_office_add, name='diocese_main_add'),
    path('diocese/main/<int:pk>/edit/', views.diocese_main_office_edit, name='diocese_main_edit'),
    
    # Diocese Youth Office
    path('diocese/youth/<int:diocese_id>/', views.diocese_youth_office_detail, name='diocese_youth_detail'),
    path('diocese/youth/<int:diocese_id>/add/', views.diocese_youth_office_add, name='diocese_youth_add'),
    path('diocese/youth/<int:pk>/edit/', views.diocese_youth_office_edit, name='diocese_youth_edit'),
    
    # Diocese Teachers Office
    path('diocese/teachers/<int:diocese_id>/', views.diocese_teachers_office_detail, name='diocese_teachers_detail'),
    path('diocese/teachers/<int:diocese_id>/add/', views.diocese_teachers_office_add, name='diocese_teachers_add'),
    path('diocese/teachers/<int:pk>/edit/', views.diocese_teachers_office_edit, name='diocese_teachers_edit'),
    
    # ====================================
    # DEAN/HEADQUARTERS LEVEL URLS (25)
    # ====================================
    
    # Dean Management Office
    path('dean/management/', views.dean_management_office_detail, name='dean_management_detail'),
    path('dean/management/add/', views.dean_management_office_add, name='dean_management_add'),
    path('dean/management/<int:pk>/edit/', views.dean_management_office_edit, name='dean_management_edit'),
    
    # Dean Organizing Secretary Office
    path('dean/organizing-secretary/', views.dean_organizing_secretary_office_detail, name='dean_organizing_secretary_detail'),
    path('dean/organizing-secretary/add/', views.dean_organizing_secretary_office_add, name='dean_organizing_secretary_add'),
    path('dean/organizing-secretary/<int:pk>/edit/', views.dean_organizing_secretary_office_edit, name='dean_organizing_secretary_edit'),
    
    # Dean Youth Office
    path('dean/youth/', views.dean_youth_office_detail, name='dean_youth_detail'),
    path('dean/youth/add/', views.dean_youth_office_add, name='dean_youth_add'),
    path('dean/youth/<int:pk>/edit/', views.dean_youth_office_edit, name='dean_youth_edit'),
    
    # Dean King's Office
    path('dean/kings/', views.dean_kings_office_detail, name='dean_kings_detail'),
    path('dean/kings/add/', views.dean_kings_office_add, name='dean_kings_add'),
    path('dean/kings/<int:pk>/edit/', views.dean_kings_office_edit, name='dean_kings_edit'),
    
    # Dean Archbishop's Office
    path('dean/archbishops/', views.dean_archbishops_office_detail, name='dean_archbishops_detail'),
    path('dean/archbishops/add/', views.dean_archbishops_office_add, name='dean_archbishops_add'),
    path('dean/archbishops/<int:pk>/edit/', views.dean_archbishops_office_edit, name='dean_archbishops_edit'),
    
    # Dean Bishops Office
    path('dean/bishops/', views.dean_bishops_office_detail, name='dean_bishops_detail'),
    path('dean/bishops/add/', views.dean_bishops_office_add, name='dean_bishops_add'),
    path('dean/bishops/<int:pk>/edit/', views.dean_bishops_office_edit, name='dean_bishops_edit'),
    
    # Dean Pastors Office
    path('dean/pastors/', views.dean_pastors_office_detail, name='dean_pastors_detail'),
    path('dean/pastors/add/', views.dean_pastors_office_add, name='dean_pastors_add'),
    path('dean/pastors/<int:pk>/edit/', views.dean_pastors_office_edit, name='dean_pastors_edit'),
    
    # Dean Lay Readers Office
    path('dean/lay-readers/', views.dean_lay_readers_office_detail, name='dean_lay_readers_detail'),
    path('dean/lay-readers/add/', views.dean_lay_readers_office_add, name='dean_lay_readers_add'),
    path('dean/lay-readers/<int:pk>/edit/', views.dean_lay_readers_office_edit, name='dean_lay_readers_edit'),
    
    # Dean Divisions Office
    path('dean/divisions/', views.dean_divisions_office_detail, name='dean_divisions_detail'),
    path('dean/divisions/add/', views.dean_divisions_office_add, name='dean_divisions_add'),
    path('dean/divisions/<int:pk>/edit/', views.dean_divisions_office_edit, name='dean_divisions_edit'),
    
    # Dean Teachers Office
    path('dean/teachers/', views.dean_teachers_office_detail, name='dean_teachers_detail'),
    path('dean/teachers/add/', views.dean_teachers_office_add, name='dean_teachers_add'),
    path('dean/teachers/<int:pk>/edit/', views.dean_teachers_office_edit, name='dean_teachers_edit'),
    
    # Dean Women Leaders Office
    path('dean/women-leaders/', views.dean_women_leaders_office_detail, name='dean_women_leaders_detail'),
    path('dean/women-leaders/add/', views.dean_women_leaders_office_add, name='dean_women_leaders_add'),
    path('dean/women-leaders/<int:pk>/edit/', views.dean_women_leaders_office_edit, name='dean_women_leaders_edit'),
    
    # Dean Elders Office
    path('dean/elders/', views.dean_elders_office_detail, name='dean_elders_detail'),
    path('dean/elders/add/', views.dean_elders_office_add, name='dean_elders_add'),
    path('dean/elders/<int:pk>/edit/', views.dean_elders_office_edit, name='dean_elders_edit'),
    
    # Dean Soso Office
    path('dean/soso/', views.dean_soso_office_detail, name='dean_soso_detail'),
    path('dean/soso/add/', views.dean_soso_office_add, name='dean_soso_add'),
    path('dean/soso/<int:pk>/edit/', views.dean_soso_office_edit, name='dean_soso_edit'),
    
    # Dean Courses Office
    path('dean/courses/', views.dean_courses_office_detail, name='dean_courses_detail'),
    path('dean/courses/add/', views.dean_courses_office_add, name='dean_courses_add'),
    path('dean/courses/<int:pk>/edit/', views.dean_courses_office_edit, name='dean_courses_edit'),
    
    # Dean Ecclesiastical Vestment Office
    path('dean/ecclesiastical-vestment/', views.dean_ecclesiastical_vestment_office_detail, name='dean_ecclesiastical_vestment_detail'),
    path('dean/ecclesiastical-vestment/add/', views.dean_ecclesiastical_vestment_office_add, name='dean_ecclesiastical_vestment_add'),
    path('dean/ecclesiastical-vestment/<int:pk>/edit/', views.dean_ecclesiastical_vestment_office_edit, name='dean_ecclesiastical_vestment_edit'),
    
    # Dean Ecclesiastical Cross Office
    path('dean/ecclesiastical-cross/', views.dean_ecclesiastical_cross_office_detail, name='dean_ecclesiastical_cross_detail'),
    path('dean/ecclesiastical-cross/add/', views.dean_ecclesiastical_cross_office_add, name='dean_ecclesiastical_cross_add'),
    path('dean/ecclesiastical-cross/<int:pk>/edit/', views.dean_ecclesiastical_cross_office_edit, name='dean_ecclesiastical_cross_edit'),
    
    # Dean Chaplaincy Office
    path('dean/chaplaincy/', views.dean_chaplaincy_office_detail, name='dean_chaplaincy_detail'),
    path('dean/chaplaincy/add/', views.dean_chaplaincy_office_add, name='dean_chaplaincy_add'),
    path('dean/chaplaincy/<int:pk>/edit/', views.dean_chaplaincy_office_edit, name='dean_chaplaincy_edit'),
    
    # Dean Churches Data and Records Office
    path('dean/churches-data-records/', views.dean_churches_data_records_office_detail, name='dean_churches_data_records_detail'),
    path('dean/churches-data-records/add/', views.dean_churches_data_records_office_add, name='dean_churches_data_records_add'),
    path('dean/churches-data-records/<int:pk>/edit/', views.dean_churches_data_records_office_edit, name='dean_churches_data_records_edit'),
    
    # Dean Education and Gender Equality Office
    path('dean/education-gender-equality/', views.dean_education_gender_equality_office_detail, name='dean_education_gender_equality_detail'),
    path('dean/education-gender-equality/add/', views.dean_education_gender_equality_office_add, name='dean_education_gender_equality_add'),
    path('dean/education-gender-equality/<int:pk>/edit/', views.dean_education_gender_equality_office_edit, name='dean_education_gender_equality_edit'),
    
    # Dean Development Office
    path('dean/development/', views.dean_development_office_detail, name='dean_development_detail'),
    path('dean/development/add/', views.dean_development_office_add, name='dean_development_add'),
    path('dean/development/<int:pk>/edit/', views.dean_development_office_edit, name='dean_development_edit'),
    
    # Dean Disciplinary Committee Office
    path('dean/disciplinary-committee/', views.dean_disciplinary_committee_office_detail, name='dean_disciplinary_committee_detail'),
    path('dean/disciplinary-committee/add/', views.dean_disciplinary_committee_office_add, name='dean_disciplinary_committee_add'),
    path('dean/disciplinary-committee/<int:pk>/edit/', views.dean_disciplinary_committee_office_edit, name='dean_disciplinary_committee_edit'),
    
    # Dean Arbitration Committee Office
    path('dean/arbitration-committee/', views.dean_arbitration_committee_office_detail, name='dean_arbitration_committee_detail'),
    path('dean/arbitration-committee/add/', views.dean_arbitration_committee_office_add, name='dean_arbitration_committee_add'),
    path('dean/arbitration-committee/<int:pk>/edit/', views.dean_arbitration_committee_office_edit, name='dean_arbitration_committee_edit'),
    
    # Dean Health and Counselling Office
    path('dean/health-counselling/', views.dean_health_counselling_office_detail, name='dean_health_counselling_detail'),
    path('dean/health-counselling/add/', views.dean_health_counselling_office_add, name='dean_health_counselling_add'),
    path('dean/health-counselling/<int:pk>/edit/', views.dean_health_counselling_office_edit, name='dean_health_counselling_edit'),
    
    # Dean Churches Protocol Office
    path('dean/churches-protocol/', views.dean_churches_protocol_office_detail, name='dean_churches_protocol_detail'),
    path('dean/churches-protocol/add/', views.dean_churches_protocol_office_add, name='dean_churches_protocol_add'),
    path('dean/churches-protocol/<int:pk>/edit/', views.dean_churches_protocol_office_edit, name='dean_churches_protocol_edit'),
    
    # Dean Media and Publicity Office
    path('dean/media-publicity/', views.dean_media_publicity_office_detail, name='dean_media_publicity_detail'),
    path('dean/media-publicity/add/', views.dean_media_publicity_office_add, name='dean_media_publicity_add'),
    path('dean/media-publicity/<int:pk>/edit/', views.dean_media_publicity_office_edit, name='dean_media_publicity_edit'),
]