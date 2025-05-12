from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
def secure_view(request):
    if request.method == "POST":
        data = request.POST.get("data", "")
        sanitized_data = data.replace("<", "&lt;").replace(">", "&gt;")
        return JsonResponse({"sanitized_data": sanitized_data})
    return JsonResponse({"error": "Invalid request method"}, status=400)
