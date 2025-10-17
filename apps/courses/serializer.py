from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Avg
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
            'id','user','bio','profile_image','expertise','total_students','rating','is_verified','created_at'
        ]
        read_only_fields = ['id','created_at','id']

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
    level = serializers.ChoiceField(choices=['beginner', 'intermediate', 'advanced'])
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_id = CategoryModelSerializer(source='category', read_only=True)
    teach = InstructorSerializer(source='instructor', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id','title', 'description', 'instructor', 'teach',
            'category', 'category_id', 'price',
            'discount_percentage', 'level', 'duration_hours',
            'requirements', 'what_you_learn', 'language',
            'thumbnail', 'slug', 'created_at'
        ]
        read_only_fields = ['id','slug', 'created_at','teach','category_id']

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

    @staticmethod
    def validate_title(title):
        if len(title.strip()) < 1:
            raise serializers.ValidationError("Name can not be empty.")
        return title

    @staticmethod
    def validate_description(value):
        if len(value) < 50:
            raise serializers.ValidationError("Description must be at least 50 characters long")
        return value

    @staticmethod
    def validate_price(price):
        if price < 0:
            raise serializers.ValidationError("Price can not be empty.")
        return price

    @staticmethod
    def validate_discount_percentage(price):
        if price < 0 or price > 100:
            raise  serializers.ValidationError("Discount percentage must be between 0-100")
        return price

    @staticmethod
    def validate_duration_hours(hours):
        if hours is None or hours <= 0:
            raise serializers.ValidationError("Hour must be greater than 0.")
        return hours

    def validate(self, attrs):
        instructor = attrs.get('instructor')

        if not instructor:
            raise serializers.ValidationError({"instructor": "Instructor must be entered."})

        if not getattr(instructor, 'is_active', True):
            raise serializers.ValidationError({"instructor": "Instructor is not active."})

        return attrs

    def validate_category(self,category):

        if not category:
            raise serializers.ValidationError({"category": "category must be entered."})

        if not getattr(category, 'is_active',True):
            raise serializers.ValidationError({"category": "category is not active."})

        return category

    @staticmethod
    def validate_language(language):
        if len(language) < 0:
            raise serializers.ValidationError("Name can not be empty.")
        return language

class CategoryNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('parent', 'is_active')



class InstructorNestedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Instructor
        fields = '__all__'



class CourseListSerializer(serializers.ModelSerializer):
    category = CategoryNestedSerializer(read_only=True)
    instructor = InstructorNestedSerializer(read_only=True)
    final_price = serializers.SerializerMethodField(read_only=True)
    # total_lessons = serializers.SerializerMethodField(read_only=True)
    # total_duration = serializers.SerializerMethodField(read_only=True)
    # students_count = serializers.SerializerMethodField(read_only=True)
    # average_rating = serializers.SerializerMethodField(read_only=True)
    # reviews_count = serializers.SerializerMethodField(read_only=True)
    category_id = CategoryModelSerializer(source='category', read_only=True)
    teach = InstructorSerializer(source='instructor', read_only=True)

    class Meta:
        model = Course
        exclude = ['id', 'updated_at', 'is_featured']
        read_only_fields = ['id', 'slug', 'created_at']

    @staticmethod
    def get_final_price(value):
        return value.price * (Decimal(1) - Decimal(value.discount_percentage) / Decimal(100))

    # def get_total_lessons(self,value):
    #     pass
    #
    # def get_total_duration(self,value):
    #     pass
    #
    # @staticmethod
    # def get_students_count(value):
    #     return value.enrollments.count()
    #
    # @staticmethod
    # def get_average_rating(value):
    #     return value.reviews.aggregate(avg=Avg('rating'))
    #
    # @staticmethod
    # def get_reviews_count(value):
    #     return value.reviews.count()


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



class CourseDetailSerializer(serializers.ModelSerializer):
    category_id = CategoryModelSerializer(source='category', read_only=True)
    teach = InstructorSerializer(source='instructor', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['slug', 'created_at']


    def update(self, instance, validated_data):
        title = validated_data.get('title', instance.title)
        if title != instance.title:
            slug = slugify(title)
            counter = 1
            while Course.objects.filter(slug=slug).exists():
                slug = f"{slugify(title)}-{counter}"
                counter += 1
            validated_data['slug'] = slug
        return super().update(instance, validated_data)