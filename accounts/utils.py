import requests
import json

def send_kakao_message(access_token, message):
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'template_object': json.dumps({
            'object_type': 'text',
            'text': message,
            'link': {
                'web_url': 'http://www.yourwebsite.com',
                'mobile_web_url': 'http://www.yourwebsite.com'
            }
        })
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()
