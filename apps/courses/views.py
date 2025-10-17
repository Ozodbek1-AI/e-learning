from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from apps.courses.models import Course, Category, Instructor, Lesson
from apps.courses.serializer import CourseModelSerializer, CategoryModelSerializer, InstructorSerializer, \
    CourseListSerializer, CourseDetailSerializer


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
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Category ID bo‘yicha filter (majburiy emas, lekin ishlaydi)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('instructor', openapi.IN_QUERY, description="Instructor ID bo‘yicha filter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('level', openapi.IN_QUERY, description="Level (beginner, intermediate, advanced)", type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimal narx", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Maksimal narx", type=openapi.TYPE_NUMBER),
            openapi.Parameter('is_featured', openapi.IN_QUERY, description="True/False — featured kurslar uchun", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Title bo‘yicha qidirish", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Masalan: price yoki -price", type=openapi.TYPE_STRING),
        ],
        responses={200: CourseListSerializer(many=True)}
    )
    def get(self, request):
        courses = Course.objects.all()

        category = request.query_params.get('category')
        instructor = request.query_params.get('instructor')
        level = request.query_params.get('level')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        is_featured = request.query_params.get('is_featured')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')

        # 🧩 Filterlar
        if category:
            courses = courses.filter(category__id=category)

        if instructor:
            courses = courses.filter(instructor__id=instructor)

        if level:
            courses = courses.filter(level=level)

        if min_price:
            courses = courses.filter(price__gte=min_price)

        if max_price:
            courses = courses.filter(price__lte=max_price)

        if is_featured is not None:
            if is_featured.lower() == 'true':
                courses = courses.filter(is_featured=True)
            elif is_featured.lower() == 'false':
                courses = courses.filter(is_featured=False)

        if search:
            courses = courses.filter(title__icontains=search)

        if ordering:
            courses = courses.order_by(ordering)

        if not courses.exists():
            return Response({"message": "Hech qanday kurs topilmadi"}, status=404)

        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)



class CourseDetailAPIView(APIView):

    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        serializer = CourseDetailSerializer(course)
        return Response(serializer.data)


class CourseDetailPutPatchDeleteAPIView(APIView):
    serializer_class = CourseDetailSerializer
    model = Course

    @swagger_auto_schema(
        request_body=CourseDetailSerializer,
        responses={200: CourseDetailSerializer}
    )
    def put(self,request,pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"errors":"Course not found"},status=404)

        serializer = CourseDetailSerializer(instance=course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product updated", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        request_body=CourseDetailSerializer,
        responses={200: CourseDetailSerializer}
    )
    def patch(self,request,pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'error':'Product not found'},status=404)

        serializer = CourseDetailSerializer(instance=course, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product updated", "data": serializer.data},
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=404)

        course.delete()
        return Response({'message': 'Course deleted successfully'})