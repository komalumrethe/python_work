from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
import datetime
from django.db import transaction
from django.contrib.auth.models import User
from app.serializers import UserDetailsSerializer
import csv
import os
from django.conf import settings

class UserApi(APIView):

	def post(self, request):
		data = request.data
		first_name = data['first_name']
		last_name = data['last_name']
		email = data['email']
		password = data['password']
		##### To check if user already exists #####
		if User.objects.filter(email=email).exists():
			return JsonResponse({"status": "failure", "message" : "email already exists"})
		else:
			##### Code to insert data in User table #####
			create_user = User(first_name = first_name, last_name = last_name, 
								email = email, username = email, last_login = datetime.datetime.now(), 
								date_joined = datetime.datetime.now(), is_active = True)
			create_user.set_password(password)
			with transaction.atomic():
				create_user.save()
			return JsonResponse({"status":"success", "message": "user created successfully"})
	
	def put(self, request):
		data = request.data
		user_id = data['user_id']
		##### Update code based on user id #####
		CurrentUser = User.objects.get(pk = user_id)
		user_ser = UserDetailsSerializer(CurrentUser, data = data, partial = True)
		user_ser.is_valid(raise_exception=True)
		user_ser.save()
		return JsonResponse({"status":"success", "message":"user data updated successfully"})

	def delete(self,request):
		data = request.data
		user_id = data['user_id']
		##### delete code based on user id #####
		CurrentUser = User.objects.get(pk = user_id)
		CurrentUser.delete()
		return JsonResponse({"status":"success", "message":"user deleted successfully"})

	def get(self, request):
		data = self.request.query_params.get
		##### code to get user details based on user id #####
		user_id = data('user_id')
		Userobject = User.objects.get(pk = user_id)
		Userserliazer = UserDetailsSerializer(Userobject)
		return JsonResponse({"status":"success", "data": Userserliazer.data})



class Csv(APIView):
	
	def post(self, request):
		
		with open(os.path.join(settings.BASE_DIR,'test.csv')) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count == 0:
					print("columns",row)
					#print(f'Column names are {", ".join(row)}')
					line_count += 1
				else:
					#print("row",row[0])
					first_name = row[0]
					last_name = row[1]
					email = row[2]
					password = row[4]
					##### To check if user already exists #####
					if User.objects.filter(email=email).exists():
						return JsonResponse({"status": "failure", "message" : "email already exists"})
					else:
						##### Code to insert data in User table #####
						create_user = User(first_name = first_name, last_name = last_name, 
											email = email, username = email, last_login = datetime.datetime.now(), 
											date_joined = datetime.datetime.now(), is_active = True)
						create_user.set_password(password)
						with transaction.atomic():
							create_user.save()
					#print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
						line_count += 1
			#print(f'Processed {line_count} lines.')
			return JsonResponse({"status":"success", "message": "user created successfully"})




		