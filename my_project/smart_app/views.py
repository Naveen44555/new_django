from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# from django.db import connection
import json
from smart_app.models import Students
from smart_app.models import movies_review
from smart_app.models import employees
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.hashers import make_password,check_password
from smart_app.models import basic_users_login

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
    

# @csrf_exempt
# def movies(request):
#     if (request.method =="POST"):
#         # data=json.loads(request.body)
#         data=request.POST
#         rating=float(data.get("ratings"))
#         stars="⭐"*int(rating)
#         review=movies_review.objects.create(
#             movie=data.get("movie"),
#             collections=data.get("collections"),
#             r_date=data.get("r_date"),
#             ratings=rating
#         )
#         print(review.movie,review.collections,review.r_date,stars)
#         return JsonResponse({"status":"success",
#                              "movie":review.movie,
#                              "collections":review.collections,
#                              "r_date":review.r_date,
#                              "stars":stars})

#     # return JsonResponse({"error": "Only POST allowed"}, status=400)

#     # GET
#     elif request.method == "GET":
#       rev=list(movies_review.objects.values())
#       return(JsonResponse({"status":"success",
#                            "data":rev}))
    
#     # PUT
#     elif request.method == "PUT":
#         if not request.body:
#             return JsonResponse({"status":"error"})
#         data=json.loads(request.body)
#         ref_id=data.get("id")
#         review = movies_review.objects.get(id=ref_id)
        
#         review.movie = data.get("movie")
#         review.collections= data.get("collections")
#         review.r_date=data.get("r_date")
#         review.ratings=data.get("ratings")
#         review.save()
#         return(JsonResponse({"status":"error","message":"body required"}))
    
    
#     # PATCH
#     elif request.method == "PATCH":
#         if not request.body:    #if body empty
#             return JsonResponse({"status":"e"})
#         data = json.loads(request.body)
#         ref_id = data.get("id")
#         review = movies_review.objects.get(id =ref_id)
#         if "movie" in data:
#             review.movie = data.get("movie")
#         if "collections" in data:
#             review.collections = data.get("collections")
#         if "r_date" in data:
#             review.ref_id = data.get("r_date")
#         if "ratings" in data:
#             review.ratings = data.get("ratings") 
        
#         review.save()
#         return JsonResponse({"status":"updated (PATCH)"})

#     #  get() throws an error if the ID doesn’t exist
#     #  filter() returns an empty queryset (no error)
    
#     # DELETE
#     elif request.method == "DELETE":
#         if not request.body:
#             return JsonResponse({"status":"not in body & it is empty"})
#         data =  json.loads(request.body)
#         ref_id = data.get("id")
#         delete_data = movies_review.objects.filter(id=ref_id).delete()[0]
#         if delete_data == 0:
#             return JsonResponse({"status":"error","deletedc_count":"zero nothing deleted"})
#         return JsonResponse({"status":"deleted"})

@csrf_exempt
def movies(request):
    if request.method == "GET":
        # read correct query params
        min_rating = request.GET.get("min_rating")
        max_rating = request.GET.get("max_rating")

        # convert to float
        min_rating = float(min_rating) if min_rating else None
        max_rating = float(max_rating) if max_rating else None

        movies_info = movies_review.objects.all()
        result = []

        for m in movies_info:

            # CASE 1: Both min and max provided → range filter
            if min_rating is not None and max_rating is not None:
                if not (min_rating <= m.ratings <= max_rating):
                    continue

            # CASE 2: Only max provided → rating < max
            elif max_rating is not None:
                if m.ratings >= max_rating:
                    continue

            # CASE 3: Only min provided → rating >= min
            elif min_rating is not None:
                if m.ratings < min_rating:
                    continue

            # CASE 4: No params → include all

            result.append({
                "movie": m.movie,
                "collections": m.collections,
                "r_date": m.r_date,
                "ratings": m.ratings
            })

        return JsonResponse({"status": "success", "data": result})

        # movies_info = movies_review.objects.all()
        # print(movies_info)
        # movie_list = []
        # for m in movies_info:
        #     movie_list.append({
        #         "movie":m.movie,
        #         "collections":m.collections,
        #         "r_date":m.r_date,
        #         "ratings":m.ratings
        #     })
        # print(movie_list)
        # return JsonResponse({"status":"success","data":movie_list})

    if (request.method =="POST"):
        # data=json.loads(request.body)
        data=request.POST

        review=movies_review.objects.create(
            movie=data.get("movie"),
            collections=data.get("collections"),
            r_date=data.get("r_date"),
            ratings=data.get("ratings")
        )
      
        return JsonResponse({"status":"success",
                             "movie":review.movie,
                             "collections":review.collections,
                             "r_date":review.r_date,
                             "ratings":review.ratings})

    # return JsonResponse({"error": "Only POST allowed"}, status=400)
    
    

    elif request.method == "PUT":
        data = json.loads(request.body)
        print(data)

        ref_id = data.get("id")
        print(ref_id)

        movie_all = movies_review.objects.get(id=ref_id)
        print(movie_all)

        if data.get("movie"):
            movie_all.movie = data.get("movie")
        if data.get("collections"):
            movie_all.collections = data.get("collections")
        if data.get("r_date"):
            movie_all.r_date = data.get("r_date")
        if data.get("ratings"):
            movie_all.ratings = data.get("ratings")
        movie_all.save()     # save only once

        return JsonResponse({"status": "success"})
    




@csrf_exempt   
def emp(request):
    if request.method == "POST":
         data=json.loads(request.body)  #when ever we send data in js format we have to use
         empl=employees.objects.create(
         name=data.get("name"),
         emp_id=data.get("emp_id"),
         date=data.get("date"),
         location=data.get("location")
         )
         print(empl.name) 
         return(JsonResponse({"status":"success"},status=200))
         
    # GET
    elif request.method=="GET":
        rev=tuple(employees.objects.values())
        return JsonResponse({"employees":rev})
    
    # put
    elif request.method=="PUT":
        data =json.loads(request.body)
        ref_id=data.get("id")
        empl=employees.objects.get(id=ref_id)
        empl.name=data.get("name")
        empl.emp_id=data.get("emp_id")
        empl.date=data.get("date")
        empl.location=data.get("location")
        empl.save()
        return JsonResponse({"status":"succes","employee":empl.name})

    # patch
    elif request.method=="PATCH":
        data=json.loads(request.body)
        ref_id=data.get("id")
        empl=employees.objects.get(id=ref_id)

        if "name" in data:
            empl.name=data.get("name")
        if "emp_id" in data:
            empl.emp_id=data.get("emp_id")
        if "date" in data:
            empl.date=data.get("date")
        if "location" in data:
            empl.location=data.get("location")
        empl.save()
        print(empl)
        return JsonResponse({"status":"success"})
    
    # DELETE
    elif request.method=="DELETE":
        data=json.loads(request.body)
        ref_id=data.get("id")
        empl=employees.objects.filter(id=ref_id).delete()
        return JsonResponse({"status":"success"})


@csrf_exempt 
def signup(request):
    if request.method =="POST":
        data=json.loads(request.body)
        print(data)
        user = basic_users_login.objects.create(
            username =data.get("username"),
            email = data.get("email"),
            password = make_password(data.get("password"))
        )
        return JsonResponse({"status":"success"},status =200)






@csrf_exempt
def login(request):
    if request.method =="POST":
        data=request.POST
        print(data)
        username=data.get("username")
        password=data.get("password")
        print(username,password)
    
        try:
            user1=basic_users_login.objects.get(username=username)
            print(username)
            if check_password(password,user1.password):
                print("Entered password:", password)
                print("DB hashed password:", user1.password)
                print(user1.password)
                return JsonResponse({"status":"successfully loggedin"},status=200)
            else:
                return JsonResponse({"status":"failure","message":"invalid password"},status=400)
       
        except basic_users_login.DoesNotExist:
            return JsonResponse ({"status":"failure","message":"user not found"},status=200)



@csrf_exempt
def change_pswd(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        ref_id = data.get("id")
        print(ref_id)
    
        uff = basic_users_login.objects.get(id=ref_id)
        
        # uff.username = data.get("username")
        # uff.email = data.get("email")
        uff.password = make_password(data.get("password"))
        uff.save()
        print(uff.password)

        return JsonResponse({"status": "successfully changed password"})
    
    return JsonResponse({"status": "failed to change"})


# data store in varibales, files database
@csrf_exempt
def check(request):
    hashed = "pbkdf2_sha256$870000$HtHHE01vhgHLeySTLJa8q7$+lk/ocT5YVjrm6jKPSczyUOxNKj4XF6Shsuv1/j2GIk="
    ipdata=request.POST
    print(ipdata)
    # hashed = make_password(ipdata.get("ip"))    #encrypting
    x= check_password(ipdata.get("ip"),hashed)
    # print(hashed)
    print(x)
    return JsonResponse({"status":"success","data":x},status=200)












# def check(request):
#     ipdata=request.POST
#     hashed = "pbkdf2_sha256$870000$eVbKtaSl9nlpx48GcVwtuZ$QKtNyjOJbqwOV36lcHUTGsT24gciAykMj81ywRZYGfs="
#     # ipdata=make_password(ipdata.get("ip"))  #make_password() is a Django function that encrypts (hashes) a password using Django’s default hashing algorithms.
#     x=check_password(ipdata.get("ip"),hashed)
#     # print(ipdata)
#     print(x)
#     return JsonResponse({"status":"succes",'data':x})
    
