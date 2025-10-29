from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_member, name='add_member'),
    path('detail/<str:username>/', views.member_detail, name='member_detail'),
    path('edit/<str:username>/', views.edit_member, name='edit_member'),

    # API endpoints for member search and cascading dropdowns
    path('api/search/', views.search_members_api, name='search_members_api'),
    path('api/pastorates/<int:diocese_id>/', views.get_pastorates_by_diocese, name='get_pastorates_by_diocese'),
    path('api/churches/<int:pastorate_id>/', views.get_churches_by_pastorate, name='get_churches_by_pastorate'),
]