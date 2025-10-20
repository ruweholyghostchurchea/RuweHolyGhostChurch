from django.urls import path
from . import views

app_name = 'email_system'

urlpatterns = [
    path('', views.index, name='index'),
    path('compose/', views.compose, name='compose'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('campaigns/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/<int:campaign_id>/send/', views.send_campaign, name='send_campaign'),
    path('logs/', views.email_logs, name='logs'),
    path('preview-recipients/', views.preview_recipients, name='preview_recipients'),
]
