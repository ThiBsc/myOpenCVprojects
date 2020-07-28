import os, time, multiprocessing
import telepot
import telegram_cfg
import objtrack

p = multiprocessing.Process()
act = multiprocessing.Value('i', 0)

def sendCapture(chat_id):
    bot.sendPhoto(chat_id=chat_id, photo=open('capture.jpg', 'rb'), caption='\U0001F4F7 Instant capture')
    act.value = 0

def sendVideo(chat_id):
    bot.sendVideo(chat_id=chat_id, video=open('record.mp4', 'rb'), caption='\U0001F3A5 Instant 5 seconds movie')
    act.value = 0

def sendAlert(chat_id):
    bot.sendPhoto(chat_id=chat_id, photo=open('alert.jpg', 'rb'), caption='\U0001F6A8 A movement has been detected')
    act.value = 0

def handle(msg):
    global p
    chat_id = msg['chat']['id']
    command = msg['text']

    if str(msg['from']['id']) not in telegram_cfg.TELEGRAM_USRID_WHITELIST:
        bot.sendMessage(chat_id=chat_id, text='\u2694\U0001F512 Forbidden access')
    else:
        print('Receive: %s' % command)

        if command == '/runtracking':
            if p.is_alive():
                bot.sendMessage(chat_id=chat_id, text='Tracking already running')
            else:
                dic_fun = {'capture': sendCapture, 'video': sendVideo, 'alert': sendAlert}
                p = multiprocessing.Process(target=objtrack.startTracking, args=(True, chat_id, dic_fun, act))
                p.start()
        elif command == '/stoptracking':
            if p.is_alive():
                act.value = 3
                p.join()
                act.value = 0
            else:
                bot.sendMessage(chat_id=chat_id, text='Tracking is not running')
        elif command == '/status':
            bot.sendMessage(chat_id=chat_id, text=('\U0001F7E2' if p.is_alive() else '\U0001F534'))
        elif command == '/capture':
            if p.is_alive():
                act.value = 1
            else:
                bot.sendMessage(chat_id=chat_id, text='Tracking is not running')
        elif command == '/video':
            if p.is_alive():
                act.value = 2
                bot.sendMessage(chat_id=chat_id, text='\u231B The video is recording')
            else:
                bot.sendMessage(chat_id=chat_id, text='Tracking is not running')

# Replace the next line with your token
bot = telepot.Bot(token=telegram_cfg.TELEGRAM_API)
bot.message_loop(handle)

print('Telegram Bot is listening')

while 1:
    time.sleep(25)
