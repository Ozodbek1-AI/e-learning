from django.urls import path

from apps.courses.views import CourseCreateAPIView, InstructorCreateAPIView, CategoryCreateAPIView

app_name = 'courses'

urlpatterns = [
    path('',CourseCreateAPIView.as_view(),name='create-course'),
    path('create-cat/',CategoryCreateAPIView.as_view(),name='create-cat'),
    path('create-teach/',InstructorCreateAPIView.as_view(),name='create-teach'),
]