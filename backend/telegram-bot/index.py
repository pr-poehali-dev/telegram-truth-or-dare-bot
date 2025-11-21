import json
import os
import random
from typing import Dict, Any

truth_questions = [
    "Какую самую большую глупость ты совершил(-а) в жизни?",
    "Кого из присутствующих ты считаешь самым привлекательным?",
    "Какую тайну ты скрываешь от всех?",
    "О чём ты врал(-а) родителям?",
    "Какой твой самый стыдный момент в жизни?",
    "Что ты никогда не расскажешь своим родителям?",
    "Кто тебе нравится из этой компании?",
    "Какую оценку ты бы поставил(-а) своей внешности?",
    "Что самое безумное ты делал(-а) в нетрезвом состоянии?",
    "Кому из присутствующих ты завидуешь?",
    "Какое твоё самое большое сожаление?",
    "За что тебе больше всего стыдно?",
    "Кого бы ты поцеловал(-а) из присутствующих?",
    "Какой комплимент тебе было труднее всего принять?",
    "О чём ты думаешь перед сном?"
]

dare_actions = [
    "Станцуй танец без музыки в течение минуты",
    "Сделай комплимент каждому игроку",
    "Покажи последние 5 фотографий в телефоне",
    "Говори с акцентом до конца игры",
    "Отправь сообщение бывшему(-ей) 'Привет, как дела?'",
    "Сделай 20 приседаний",
    "Позвони родителям и скажи 'Я люблю вас'",
    "Покажи содержимое своей сумки или карманов",
    "Съешь что-нибудь, не используя руки",
    "Расскажи анекдот или смешную историю",
    "Сделай селфи с каждым игроком",
    "Покажи свой самый глупый танец",
    "Изобрази кого-то из присутствующих",
    "Спой песню, которую выберут другие",
    "Сделай планку 30 секунд"
]

def send_telegram_message(chat_id: int, text: str, reply_markup: Dict = None) -> Dict:
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    import urllib.request
    import urllib.parse
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def get_main_menu_keyboard():
    return {
        'inline_keyboard': [
            [{'text': '💬 Правда', 'callback_data': 'truth'}],
            [{'text': '⚡ Действие', 'callback_data': 'dare'}]
        ]
    }

def get_next_keyboard(mode: str):
    return {
        'inline_keyboard': [
            [{'text': '🔄 Следующий вопрос', 'callback_data': f'next_{mode}'}],
            [{'text': '🏠 Главное меню', 'callback_data': 'menu'}]
        ]
    }

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Telegram bot webhook handler for Truth or Dare game
    Args: event with httpMethod, body containing Telegram update
    Returns: HTTP response with statusCode 200
    '''
    method: str = event.get('httpMethod', 'POST')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    if method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'Telegram bot is running'}),
            'isBase64Encoded': False
        }
    
    if method != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Method not allowed'}),
            'isBase64Encoded': False
        }
    
    body_str = event.get('body', '{}')
    update = json.loads(body_str)
    
    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        if text == '/start':
            bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
            if bot_token:
                send_telegram_message(
                    chat_id,
                    '<b>🎮 Правда или Действие</b>\n\nКлассическая игра для компании!\n\nВыбери режим игры:',
                    get_main_menu_keyboard()
                )
    
    elif 'callback_query' in update:
        callback = update['callback_query']
        chat_id = callback['message']['chat']['id']
        message_id = callback['message']['message_id']
        data = callback['data']
        
        import urllib.request
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        
        urllib.request.urlopen(
            f'https://api.telegram.org/bot{bot_token}/answerCallbackQuery?callback_query_id={callback["id"]}'
        )
        
        if data == 'menu':
            urllib.request.urlopen(urllib.request.Request(
                f'https://api.telegram.org/bot{bot_token}/editMessageText',
                data=json.dumps({
                    'chat_id': chat_id,
                    'message_id': message_id,
                    'text': '<b>🎮 Правда или Действие</b>\n\nКлассическая игра для компании!\n\nВыбери режим игры:',
                    'parse_mode': 'HTML',
                    'reply_markup': get_main_menu_keyboard()
                }).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            ))
        
        elif data == 'truth':
            question = random.choice(truth_questions)
            urllib.request.urlopen(urllib.request.Request(
                f'https://api.telegram.org/bot{bot_token}/editMessageText',
                data=json.dumps({
                    'chat_id': chat_id,
                    'message_id': message_id,
                    'text': f'<b>💬 Правда</b>\n\n{question}',
                    'parse_mode': 'HTML',
                    'reply_markup': get_next_keyboard('truth')
                }).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            ))
        
        elif data == 'dare':
            action = random.choice(dare_actions)
            urllib.request.urlopen(urllib.request.Request(
                f'https://api.telegram.org/bot{bot_token}/editMessageText',
                data=json.dumps({
                    'chat_id': chat_id,
                    'message_id': message_id,
                    'text': f'<b>⚡ Действие</b>\n\n{action}',
                    'parse_mode': 'HTML',
                    'reply_markup': get_next_keyboard('dare')
                }).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            ))
        
        elif data.startswith('next_'):
            mode = data.split('_')[1]
            if mode == 'truth':
                question = random.choice(truth_questions)
                urllib.request.urlopen(urllib.request.Request(
                    f'https://api.telegram.org/bot{bot_token}/editMessageText',
                    data=json.dumps({
                        'chat_id': chat_id,
                        'message_id': message_id,
                        'text': f'<b>💬 Правда</b>\n\n{question}',
                        'parse_mode': 'HTML',
                        'reply_markup': get_next_keyboard('truth')
                    }).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                ))
            else:
                action = random.choice(dare_actions)
                urllib.request.urlopen(urllib.request.Request(
                    f'https://api.telegram.org/bot{bot_token}/editMessageText',
                    data=json.dumps({
                        'chat_id': chat_id,
                        'message_id': message_id,
                        'text': f'<b>⚡ Действие</b>\n\n{action}',
                        'parse_mode': 'HTML',
                        'reply_markup': get_next_keyboard('dare')
                    }).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                ))
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'ok': True}),
        'isBase64Encoded': False
    }