from django.db.models import Q, Sum, Avg
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.generics import CreateAPIView, get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Course, Category, Instructor, Lesson
from apps.courses.serializer import CourseModelSerializer, CategoryModelSerializer, InstructorSerializer, \
    CourseListSerializer


class InstructorCreateAPIView(CreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer



class CourseListAPIView(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        serializer = CourseListSerializer(course)
        return Response(serializer.data)

