from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.FloatField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')

    def __str__(self):
        return self.name
    from rest_framework import serializers
from .models import Company, Vacancy

# Один через ModelSerializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

# Один вручную через Serializer
class VacancySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    salary = serializers.FloatField()
    company = serializers.PrimaryKeyRelatedField(read_only=True)
    from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Company, Vacancy
from .serializers import CompanySerializer, VacancySerializer

# Function-based views

@api_view(['GET'])
def company_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def company_detail(request, id):
    try:
        company = Company.objects.get(id=id)
    except Company.DoesNotExist:
        return Response(status=404)
    serializer = CompanySerializer(company)
    return Response(serializer.data)

@api_view(['GET'])
def company_vacancies(request, id):
    try:
        company = Company.objects.get(id=id)
    except Company.DoesNotExist:
        return Response(status=404)
    vacancies = company.vacancies.all()
    serializer = VacancySerializer(vacancies, many=True)
    return Response(serializer.data)

# Class-based views

class VacancyListAPIView(APIView):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        serializer = VacancySerializer(vacancies, many=True)
        return Response(serializer.data)

class VacancyDetailAPIView(APIView):
    def get(self, request, id):
        try:
            vacancy = Vacancy.objects.get(id=id)
        except Vacancy.DoesNotExist:
            return Response(status=404)
        serializer = VacancySerializer(vacancy)
        return Response(serializer.data)

class TopTenVacanciesAPIView(APIView):
    def get(self, request):
        top_vacancies = Vacancy.objects.order_by('-salary')[:10]
        serializer = VacancySerializer(top_vacancies, many=True)
        return Response(serializer.data)

from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.company_list),
    path('companies/<int:id>/', views.company_detail),
    path('companies/<int:id>/vacancies/', views.company_vacancies),

    path('vacancies/', views.VacancyListAPIView.as_view()),
    path('vacancies/<int:id>/', views.VacancyDetailAPIView.as_view()),
    path('vacancies/top_ten/', views.TopTenVacanciesAPIView.as_view()),
]

