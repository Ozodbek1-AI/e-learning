from django.urls import path

from apps.courses.views import CourseCreateAPIView, InstructorCreateAPIView, CategoryCreateAPIView, CourseListAPIView, \
    CourseDetailPutPatchDeleteAPIView, CourseDetailAPIView

app_name = 'courses'

urlpatterns = [
    #post
    path('',CourseCreateAPIView.as_view(),name='create-course'),
    path('create-cat/',CategoryCreateAPIView.as_view(),name='create-cat'),
    path('create-teach/',InstructorCreateAPIView.as_view(),name='create-teach'),

    #get
    path('list/',CourseListAPIView.as_view(),name='list-detail-course'),

    #detail
    path('update-detail/<int:pk>/', CourseDetailPutPatchDeleteAPIView.as_view(), name='update-detail'),
    path('detail/<int:pk>/', CourseDetailAPIView.as_view(), name='detail'),

]