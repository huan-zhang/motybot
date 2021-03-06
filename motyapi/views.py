from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
import json
import requests

from motyapp.models import BotResponse, BotParam


REGION = 'us-west-2'
SRC_LANG = 'auto'
TRG_LANG_ZH = 'zh'
TRG_LANG_EN = 'en'
BOT_ENDPOINT = 'https://api.telegram.org/bot1109107118:AAFLl7EOefQ17p7DIz0aFeUH1vrao0ptkNI/'

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

class BotResponseView:
   
    @staticmethod
    @csrf_exempt
    def get_bot_response(test_str):
        result_str = "No response found.";
        try:
            responses = BotResponse.objects.all();
            for response in responses:
                if test_str == response.search_str:
                    result_str = response.response_str;
        except Exception as e:
            print (e);
            pass;
        return result_str;
    
    @staticmethod
    @csrf_exempt
    def get_bot_response_list(request):
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
    
    @staticmethod
    @csrf_exempt
    def translate_to_chinese(original_str):
        result_str = '';
        try:
            translate = boto3.client(service_name='translate', region_name=REGION, use_ssl=True);
            response = translate.translate_text(Text=original_str, SourceLanguageCode=SRC_LANG, TargetLanguageCode=TRG_LANG_ZH);
            if response['SourceLanguageCode'] == TRG_LANG_ZH:
                response = translate.translate_text(Text=original_str, SourceLanguageCode=SRC_LANG, TargetLanguageCode=TRG_LANG_EN);
            result_str = response.get('TranslatedText')
        except Exception as e:
            print (e);
            pass;
        return result_str;    
        
    @staticmethod
    @csrf_exempt
    def translate(request):
        try:
            post_data = json.loads(request.body);
            print(post_data);
            original_text = post_data['original_text'];
            result = BotResponseView.translate_to_chinese(original_text);
            result_json = {};
            result_json["origin_text"] = original_text;
            result_json["translated_text"] = result;
        except Exception as e:
            print (e)
            return JsonResponse({'status':'false','message':'Getting bot responses failed.'}, status=400)
        return JsonResponse(result_json, status=200)

    @staticmethod
    @csrf_exempt
    def process_bot_request(request):
        try:
            post_data = json.loads(request.body);
            print(post_data);
            payload = BotResponseView.prepare_payload(post_data);
            """
            payload = {
                "method": "sendMessage",
                "chat_id": "" + postData['message']['chat']['id'],
                "text": resultText,
            };
            """
            resp = requests.post(BOT_ENDPOINT, payload);
            if (resp.ok):
                print(resp.text)
                result_json = json.loads(resp.text);
            else:
                return JsonResponse({'status':'false','message':'Getting bot responses failed.'}, status=400)
            
        except Exception as e:
            print (e)
            return JsonResponse({'status':'false','message':'Getting bot responses failed.'}, status=400)
        return JsonResponse(result_json, status=200, safe=False)
    
    @staticmethod
    def prepare_payload(data):
        payload = {};
        try:
            message = data['message'];
            chat_id = str(message['chat']['id']);
            result_text = "hey, " + message['from']['first_name'] + " " + message['from']['last_name'];
            
            if 'text' in message:
                msg_txt = message['text'].upper();
                print (msg_txt);
                if msg_txt.startswith('/'):
                    print ("this is a command:::");
                    result_text = BotResponseView.handle_command(msg_txt[1:].split(' '), chat_id);
                payload = {
                    "method": "sendMessage",
                    "chat_id": chat_id,
                    "text": result_text,
                };
            elif 'sticker' in message:
                payload = {
                    "method": "sendMessage",
                    "chat_id": chat_id,
                    "sticker": message['sticker']['file_id'],
                };
            elif 'photo' in message:
                payload = {
                    "method": "sendMessage",
                    "chat_id": chat_id,
                    "photo": message['photo']['file_id'],
                };
            else:            
                payload = {
                    "method": "sendMessage",
                    "chat_id": chat_id,
                    "text": "Unknowm message type.",
                };
            return payload;
        except Exception as e:
            print(e)
            pass;
        
    @staticmethod
    def handle_command(param, chat_id):
        return_text  = "Hey!"
        command = param.pop(0); 
        if 'TR' == command:
            return_text = BotResponseView.translate_to_chinese(' '.join([str(i) for i in param]));
        elif "TW" == command:
             tw_param = BotParam.objects.get(param_key = 'chat_id');
             tw_param.param_val = chat_id;
             tw_param.save();
             return_text = 'Bot Param chat_id: ' + chat_id + ' is saved.';
        else:
            return_text = BotResponseView.get_bot_response(command);
        return return_text;
            
    @staticmethod
    @csrf_exempt
    def send_tweet(request):
        
        payload = {};
        try:
            post_data = json.loads(request.body);
            print(post_data);
            tweet_txt = post_data["tweet"];
            tw_param = BotParam.objects.get(param_key = 'chat_id');
            chat_id = tw_param.param_val;
            payload = {
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": "Orig Tweet: " + tweet_txt + "Transfered Tweet: " + BotResponseView.translate_to_chinese(tweet_txt),
            };   
            resp = requests.post(BOT_ENDPOINT, payload);
            if (resp.ok):
                print(resp.text)
                result_json = json.loads(resp.text);
                return JsonResponse(result_json, status=200, safe=False)
            else:
                return JsonResponse({'status':'false','message':'Getting bot responses failed.'}, status=400)
        except Exception as e:
            print(e)
            pass;