from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from apps.courses.models import Course, Category, Instructor
from apps.courses.serializer import CourseModelSerializer, CategoryModelSerializer, InstructorSerializer


class InstructorCreateAPIView(CreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
