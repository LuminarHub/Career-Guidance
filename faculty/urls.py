from django.urls import path
from .views import *

urlpatterns = [
    path('fac_home/',Fac_HomeView.as_view(),name='fac_home'),
    path('videos/',videos_view, name='videos'),
    path('videos-all/',all_videos_view, name='all_videos'),
    path('videos-all-admin/',all_videos_admin_view, name='all_videoss'),
    path('videos/<int:video_id>/',video_detail_view, name='video_detail'),
    path('videos/add/',add_video_view, name='add_video'),
    path('videos/<int:video_id>/update/',update_video_view, name='update_video'),
    path('videos/<int:video_id>/delete/',delete_video_view, name='delete_video'),
    path('student/projects/', student_projects, name='student_projects'),
    path('admin/projects/list/', admin_view_projects, name='admin_projects'),
    path('student/projects/add/', add_project, name='add_project'),
    path('student/projects/edit/<int:project_id>/', edit_project, name='edit_project'),
    path('student/projects/delete/<int:project_id>/', delete_project, name='delete_project'),
    path('faculty/projects/', faculty_view_projects, name='faculty_view_projects'),
    path('faculty/projects/student/<int:student_id>/', faculty_view_student_projects, name='faculty_view_student_projects'),
]
