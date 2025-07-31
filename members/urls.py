
from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_member, name='add_member'),
    path('detail/<int:member_id>/', views.member_detail, name='member_detail'),
    
    # API endpoints for cascading dropdowns
    path('api/pastorates/<int:diocese_id>/', views.get_pastorates_by_diocese, name='get_pastorates_by_diocese'),
    path('api/churches/<int:pastorate_id>/', views.get_churches_by_pastorate, name='get_churches_by_pastorate'),
]
