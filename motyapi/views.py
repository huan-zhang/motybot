from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from motyapp.models import BotResponse
  
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

class BotResponseView:
    @csrf_exempt
    def get_bot_responses(request):
        try:
            responses = BotResponse.objects.all();
            result_json = {};
            result_json['responses'] = [];
            for response in responses:
                result_json['responses'].append(response.to_json())
        except Exception as e:
            print (e)
            return JsonResponse({'status':'false','message':'Getting bot responses failed.'}, status=400)
        return JsonResponse(result_json, status=200)