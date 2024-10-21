from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import re
import logging

# In-memory data store
registrations = {}

# Set up logging
logging.basicConfig(level=logging.INFO)

# Rate limiting variables
RATE_LIMIT = 5  # Number of allowed requests
TIME_WINDOW = 60  # Time window in seconds
request_count = {}

def rate_limiter(client_ip):
    from time import time

    current_time = time()
    if client_ip not in request_count:
        request_count[client_ip] = {'count': 1, 'start_time': current_time}
        return False

    count_info = request_count[client_ip]
    if current_time - count_info['start_time'] > TIME_WINDOW:
        request_count[client_ip] = {'count': 1, 'start_time': current_time}
        return False

    if count_info['count'] >= RATE_LIMIT:
        return True

    request_count[client_ip]['count'] += 1
    return False

@csrf_exempt
def register(request):
    if request.method == "POST":
        client_ip = request.META.get('REMOTE_ADDR')

        if rate_limiter(client_ip):
            return JsonResponse({"error": "Rate limit exceeded"}, status=429)

        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            mobile_network = data.get('mobile_network')
            message = data.get('message')
            ref_code = data.get('ref_code')

            if not re.match(r'^[a-zA-Z0-9]{16,}$', ref_code):
                return JsonResponse({"error": "Invalid ref_code. Must be alphanumeric and at least 16 characters."}, status=400)

            if ref_code in registrations:
                return JsonResponse({"error": "ref_code must be unique."}, status=400)

            # Register the details
            registrations[ref_code] = {
                "phone_number": phone_number,
                "mobile_network": mobile_network,
                "message": message,
                "status": "successful"
            }

            # Log the request and response
            logging.info(f"Registered: {data}")
            return JsonResponse({"status": "Registration successful", "ref_code": ref_code})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

@csrf_exempt
def check_status(request, ref_code):
    if request.method == "GET":
        if ref_code in registrations:
            return JsonResponse({"status": registrations[ref_code]["status"]})
        return JsonResponse({"error": "ref_code not found"}, status=404)
    return JsonResponse({"error": "Only GET method is allowed"}, status=405)

@csrf_exempt
def update_message(request, ref_code):
    if request.method == "PUT":
        client_ip = request.META.get('REMOTE_ADDR')

        if rate_limiter(client_ip):
            return JsonResponse({"error": "Rate limit exceeded"}, status=429)

        try:
            data = json.loads(request.body)
            message = data.get('message')

            if ref_code not in registrations:
                return JsonResponse({"error": "ref_code not found"}, status=404)

            if not message:
                return JsonResponse({"error": "Message field is required"}, status=400)

            # Update the message
            registrations[ref_code]["message"] = message
            registrations[ref_code]["status"] = "updated"

            # Log the request and response
            logging.info(f"Updated message for {ref_code}: {data}")
            return JsonResponse({"status": "Message updated successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Only PUT method is allowed"}, status=405)

# Create your views here.
