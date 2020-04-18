#import requests
import myfunc
#from flask import Flask,request
#from json import loads
from cqhttp import CQHttp
bot = CQHttp(api_root='http://127.0.0.1:5700')

@bot.on_message('group')
def handle_group_msg(event):
    #print(event)
    try:
        # 插件实时监控聊天，如果对话中没有@机器人下面这个if语句就会报错，所以保护代码
        if event['message'][0]['data']['qq'] == '3442863073' and event['message'][0]['type'] == 'at': # 判断用户是否艾特机器人
            # 功能dic
            menu_dic = {
                '1': myfunc.weather,
                '2': myfunc.drame,
                '3': myfunc.virusNcp,
                '4': myfunc.movies,
            }
            # 提取群组用户发送的消息，并二次提取用户选择
            usr_msg = event['message'][1]['data']['text']
            usr_msg = usr_msg.strip(' ')
            usr_chooce = usr_msg[0]
            if usr_msg == '功能':
                bot_msg = '1查询天气(输入1+你的城市)\n2美剧查询(输入2+你订阅的美剧，则返回该剧的最新更新)\n'
                bot.send(event, message=bot_msg)
            if usr_chooce in menu_dic:
                usr_msg = usr_msg.strip(usr_chooce)
                bot.send(event, menu_dic[usr_chooce](usr_msg))
    except KeyError:
        # 聊天语句没有@机器人就会报错内容为KeyErro
        pass

@bot.on_message('private')
def handle_private_msg(event):
    print(event)
    bot.send(event, message='私人消息发送成功')

bot.run(host='127.0.0.1', port=5701, debug=True)

#bot_server = Flask(__name__)
#@bot_server.route('/api/message',methods=['POST'])
#def server():
#    data = request.get_data().decode('utf8')
#    data = loads(data)
#    print(data['message'][0]['data']['text'])
#bot_server.run(port=5701)
#data = {
#    'user_id':394761716,
#    'message':myfunc.weather(),
#    'auto_escape':False,
#}
#api_url = 'http://127.0.0.1:5700/send_private_msg'
#r = requests.post(api_url, data=data)
