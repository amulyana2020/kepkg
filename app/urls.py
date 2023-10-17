from django.contrib import admin
from django.urls import path, include
from .views import Profile, homepage, dashboard, register, profile, profile_update, submission_list, submission_update, submission_create, submission_delete, submission_detail, review, success, reviewer, my_submission_list, reviewer_submission_list, revision, decision

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
    path('submission/', submission_list, name='submission_list'),
    path('my_submission/', my_submission_list, name='my_submission_list'),
    path('reviewer_submission/', reviewer_submission_list, name='reviewer_submission_list'),
    path('submission/new/', submission_create, name='submission_create'),
    path('submission/<slug:slug>/', submission_detail, name='submission_detail'),
    path('submission/<slug:slug>/update/', submission_update, name='submission_update'),
    path('submission/<slug:slug>/delete/', submission_delete, name='submission_delete'),
    path('success',success, name="success"),
    path('review/<slug:slug>',review,name="review"),
    path('reviewer/<slug:slug>',reviewer,name="reviewer"),
    path('revision/<slug:slug>',revision,name="revision"),
    path('decision/<slug:slug>',decision,name="decision"),
]