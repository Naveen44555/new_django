from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# from django.db import connection
import json
from smart_app.models import Students
from smart_app.models import movies_review
from smart_app.models import employees
from django.views.decorators.csrf import csrf_exempt 

# Create your views here.

def sample(request):
    return HttpResponse("hello world")

def sample2(request):
    return HttpResponse("good morning")

def info(request):
    data={"name":"naveen","age":22}
    return JsonResponse(data)

# query parameter
def params(request):
    name=request.GET.get("name","naveen")
    age=request.GET.get("age",2)
    village=request.GET.get("village",'annaram')
    return JsonResponse({"name":name,"age":age,"village:":village})

def params(request):
    data = {
        "name": request.GET.get("name"),
        "age": request.GET.get("age"),
        "village": request.GET.get("village"),
    }
    return JsonResponse(data)


def add(request):
    a=request.GET.get("a",5)
    b=request.GET.get("b",6)
    result=a+b
    return HttpResponse(result)

def mul(request):
    c=request.GET.get("c",6)
    d=request.GET.get("d",8)
    result1=c*d
    return HttpResponse(result1)

# def health(request):
#     try:
#         with connection.cursor() as c:
#             c.execute("SELECT 1")
#         return JsonResponse({"status":"ok","db":"connected"})
#     except Exception as e:
#         return JsonResponse({"status":"error","db":str(e)})


# ----------pOST
# POST is used when you want to send data from client → server (like form data, JSON, etc.)
# 👉 Only run this block when the client sends data using POST request.
# POST is used for actions like:
# creating a student
# submitting a form
# sending JSON data
# uploading a file
# ✔ POST is secure because the data is not shown in the URL
# ❌ GET request shows data in the URL (not secure for forms)

# ✅ Why We Use @csrf_exempt
# @csrf_exempt disables Django’s CSRF protection for this function.

# ✋ What is CSRF?
# CSRF = Cross Site Request Forgery
# Django normally protects POST requests using a CSRF token, so that:
# Only trusted websites can send POST requests to your server.
# Hackers cannot send fake POST requests.
# Example:
# When you submit an HTML form, Django expects:

# {% csrf_token %}  ---html
# If the token is missing → request is blocked.

# Important Warning
# @csrf_exempt makes your API less secure.
# Better option in production:

# use REST framework

# or use token authentication

# or send the CSRF token properly


# In Django, objects is a built-in manager that helps you interact with the database.
# Think of it like a remote control for your model.


@csrf_exempt
def addstudent(request):
    if request.method =="POST":
        data = json.loads(request.body)
        students=Students.objects.create(  # objects = Django’s default database manager,Helps you talk to your table
            name=data.get("name"),
            age=data.get("age"),
            gmail=data.get("gmail")
        )
    return JsonResponse({"status":"succes"})
    

@csrf_exempt
def movies(request):
    if (request.method =="POST"):
        data1=json.loads(request.body)
        rating=int(data1.get("ratings"))
        stars="⭐"*rating
        review=movies_review.objects.create(
            movie=data1.get("movie"),
            collections=data1.get("collections"),
            r_date=data1.get("r_date"),
            ratings=rating    
        )
        print(review.movie,review.collections,review.r_date,stars)
        return JsonResponse({"status":"success",
                             "movie":review.movie,
                             "collections":review.collections,
                             "r_date":review.r_date,
                             "stars":stars})

    # return JsonResponse({"error": "Only POST allowed"}, status=400)

    # GET
    elif request.method == "GET":
      rev=list(movies_review.objects.values())
      return(JsonResponse({"status":"success",
                           "data":rev}))
    
    # PUT
    elif request.method == "PUT":
        if not request.body:
            return JsonResponse({"status":"error"})
        data=json.loads(request.body)
        ref_id=data.get("id")
        review = movies_review.objects.get(id=ref_id)
        
        review.movie = data.get("movie")
        review.collections= data.get("collections")
        review.r_date=data.get("r_date")
        review.ratings=data.get("ratings")
        review.save()
        return(JsonResponse({"status":"error","message":"body required"}))
    
    
    # PATCH
    elif request.method == "PATCH":
        if not request.body:    #if body empty
            return JsonResponse({"status":"e"})
        data = json.loads(request.body)
        ref_id = data.get("id")
        review = movies_review.objects.get(id =ref_id)
        if "movie" in data:
            review.movie = data.get("movie")
        if "collections" in data:
            review.collections = data.get("collections")
        if "r_date" in data:
            review.ref_id = data.get("r_date")
        if "ratings" in data:
            review.ratings = data.get("ratings") 
        
        review.save()
        return JsonResponse({"status":"updated (PATCH)"})
    

    #  get() throws an error if the ID doesn’t exist
    #  filter() returns an empty queryset (no error)
    
    # DELETE
    elif request.method == "DELETE":
        if not request.body:
            return JsonResponse({"status":"not in body & it is empty"})
        data =  json.loads(request.body)
        ref_id = data.get("id")
        delete_data = movies_review.objects.filter(id=ref_id).delete()[0]
        if delete_data == 0:
            return JsonResponse({"status":"error","deletedc_count":"zero nothing deleted"})
        return JsonResponse({"status":"deleted"})

        
def emp(request):
    if request.method == "POST":
         data=json.loads(request.body)
         emp=employees.objects.create(
         name=data.get("name"),
         emp_id=data.get("emp_id"),
         date=data.get("date"),
         location=data.get("location")
         )
         return(JsonResponse({"status":"success"},status=200))
         
