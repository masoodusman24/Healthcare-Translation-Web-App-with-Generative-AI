import json
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
    
def home(request):
    return render(request, 'translator/home.html')

@csrf_exempt
def translate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            source = data.get('sourceLang', 'en').split('-')[0]
            target = data.get('targetLang', 'ar').split('-')[0]

            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": f"{source}|{target}"
            }
            response = requests.get(url, params=params)

            print(f"MyMemory response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                result = response.json()
                translated = result.get("responseData", {}).get("translatedText", "")
                if not translated:
                    return JsonResponse({"error": "Empty translation received"}, status=500)
                return JsonResponse({"translatedText": translated})
            else:
                return JsonResponse({"error": "MyMemory API error"}, status=500)
        except Exception as e:
            print(f"Exception in translate view: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST requests allowed"}, status=405)
