from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = 'vote'

urlpatterns = [
    path('', views.index, name='index'),
    path('bio', views.bio, name='bio'),
    path('confirmation/<str:registration_number>/', views.confirmation, name='confirmation'),
    path('success', views.success, name='success'),
    path('success_vote', views.success_vote, name='success_vote'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('voter_list', views.voter_list, name='voter_list'),
    path('create_voter', views.create_voter, name='create_voter'),
    path('create_election', views.create_election, name='create_election'),
    path('election_list', views.election_list, name='election_list'),
    path('candidate_list', views.candidate_list, name='candidate_list'),
    path('create_candidate', views.create_candidate, name='create_candidate'),
    path('cast_vote/<str:election_id>/', views.cast_vote, name='cast_vote'),
    path('cast_vote_auth', views.cast_vote_auth, name='cast_vote_auth'),
    path('update_county/<str:county_code>/', views.update_county, name='update_county'),
    path('delete_county/<str:county_code>/', views.delete_county, name='delete_county'),
    path('update_ward/<str:ward_code>/', views.update_ward, name='update_ward'),
    path('delete_ward/<str:ward_code>/', views.delete_ward, name='delete_ward'),
    path('update_constituency/<str:constituency_code>/', views.update_constituency, name='update_constituency'),
    path('delete_constituency/<str:constituency_code>/', views.delete_constituency, name='delete_constituency'),
    path('check_details_auth', views.check_details_auth, name='check_details_auth'),
    path('update_details_auth', views.update_details_auth, name='update_details_auth'),
    path('voter_details/<str:registration_number>/', views.voter_details, name='voter_details'),
    path('update_details/<str:registration_number>/', views.update_details, name='update_details'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('user_account', views.user_account, name='user_account'),
    path('admin_account', views.admin_account, name='admin_account'),
    path('log_out', views.log_out, name='log_out'),
    path('admin_log_out', views.admin_log_out, name='admin_log_out'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('activation_failed', views.activation_failed, name='activation_failed')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
