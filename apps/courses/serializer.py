from django.contrib.auth.models import User
from django.utils.text import slugify
from rest_framework import serializers

from apps.courses.models import Course, Instructor, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = Instructor
        fields = [
            'user','bio','profile_image','expertise','total_students','rating','is_verified','created_at'
        ]
        read_only_fields = [ 'created_at','id']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        instructor = Instructor.objects.create(user=user, **validated_data)
        return instructor


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['slug']


class CourseModelSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_detail = CategoryModelSerializer(source='category', read_only=True)
    teach = InstructorSerializer(source='instructor', read_only=True)

    class Meta:
        model = Course
        fields = [
            'title', 'description', 'instructor', 'teach',
            'category', 'category_detail', 'price',
            'discount_percentage', 'level', 'duration_hours',
            'requirements', 'what_you_learn', 'language',
            'thumbnail', 'slug', 'created_at'
        ]
        read_only_fields = ['slug', 'created_at']

    def create(self, validated_data):
        title = validated_data.get('title')
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        while Course.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        validated_data['slug'] = slug
        return super().create(validated_data)



