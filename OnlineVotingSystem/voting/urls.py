from django.urls import path
from voting import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('vote/', views.vote_view, name='vote'),
    path('results/', views.results_view, name='results'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/add/', views.add_candidate, name='add_candidate'),
    path('candidates/edit/<int:candidate_id>/', views.edit_candidate, name='edit_candidate'),
    path('candidates/delete/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    path('voters/', views.voter_list, name='voter_list'),
    path('voters/add/', views.voter_add, name='voter_add'),
    path('voters/update/<int:user_id>/', views.voter_update, name='voter_update'),
    path('voters/delete/<int:user_id>/', views.voter_delete, name='voter_delete'),
    path('register_admin2/', views.register_admin2, name='register_admin2'),

]
