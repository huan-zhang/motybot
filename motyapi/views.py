from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
import json

from motyapp.models import BotResponse


REGION = 'us-west-2'
SRC_LANG = 'auto'
TRG_LANG_ZH = 'zh'
TRG_LANG_EN = 'en'

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
                result_json['responses'].append(response.to_json());
        except Exception as e:
            print (e);
            return JsonResponse({'status':'false','message':'Getting bot responses failed.'}, status=400);
        return JsonResponse(result_json, status=200);
    
    @csrf_exempt
    def translate_to_chinese(request):
        try:
            post_data = json.loads(request.body);
            original_text = post_data['original_text'];
            translate = boto3.client(service_name='translate', region_name=REGION, use_ssl=True);
            response = translate.translate_text(Text=original_text, SourceLanguageCode=SRC_LANG, TargetLanguageCode=TRG_LANG_ZH);
            if response['SourceLanguageCode'] == TRG_LANG_ZH:
                response = translate.translate_text(Text=original_text, SourceLanguageCode=SRC_LANG, TargetLanguageCode=TRG_LANG_EN);
            result = response.get('TranslatedText')
            result_json = {};
            result_json["origin_text"] = original_text;
            result_json["translated_text"] = result;
        except Exception as e:
            print (e)
            return JsonResponse({'status':'false','message':'Getting bot responses failed.'}, status=400)
        return JsonResponse(result_json, status=200)