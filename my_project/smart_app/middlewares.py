from django.http import JsonResponse    #object or dict format
from django.http import HttpResponse    #normal text
import json

class MovieReviewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  

    def __call__(self, request):

        # ===== POST VALIDATION =====
        if request.path == "/movies/" and request.method=="POST":
            data = request.POST

            if not data.get("ratings"):
                return JsonResponse({"error": "rating required"}, status=400)
            

            rating = float(data.get("ratings"))
            if rating < 0 or rating > 5:
                return JsonResponse({"error": "rating must be 0–5"}, status=400)

            if not data.get("collections"):
                return JsonResponse({"error": "collections required"}, status=400)

            if not data.get("r_date"):
                return JsonResponse({"error": "r_date required"}, status=400)

            if not data.get("movie"):
                return JsonResponse({"error": "movie required"}, status=400)

        # ==== IMPORTANT PART ====
        response = self.get_response(request)
        return response



















        
        # elif request.method =="PUT":
        #     data=request.PUT
        #     ref_id=data.get("id")
        #     if data.get("movie"):
        #         pass
        #     elif data.get("collections"):
        #         pass
        #     elif data.get("r_date"):
        #         pass
        #     elif data.get("ratings"):
        #         pass

        # return self.get_response(request)
        


