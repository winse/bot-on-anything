# encoding:utf-8

from model.model import Model
from config import model_conf
from common import const
from common.log import logger
import requests
import time
import uuid
import json 

sessions = {}

# 请求头
headers = {
    'accept': 'application/json,text/plain,*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://tongyi.aliyun.com',
    'referer': 'https://tongyi.aliyun.com/chat',
    'sec-ch-ua': '\\"MicrosoftEdge\\";v=\\"111\\",\\"Not(A:Brand\\";v=\\"8\\",\\"Chromium\\";v=\\"111\\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/113.0.0.0Safari/537.36',
    # 'x-xsrf-token': userinfo.token, # token
    # 'cookie': userinfo.cookie # cookie
}

tongyi_token = ''
tongyi_cookie = ''

# https://github.com/dfvips/aliyuntongyiqianwen/blob/main/tongyi.py
class TongyiModel(Model):

    def __init__(self):
        global tongyi_token, tongyi_cookie
        if tongyi_token == '':
            tongyi_token = model_conf("tongyi").get('token')
        if tongyi_cookie == '':
            tongyi_cookie = model_conf("tongyi").get('cookie').replace('"', '')
        self.openSearch = model_conf("tongyi").get('openSearch')

    def reply(self, query, context=None):
        logger.info("[TONGYI] query={}".format(query))

        global tongyi_token, tongyi_cookie
        if query.startswith("[token]"):
            tongyi_token = query.replace('[token]', '').strip()
            context['reply'] = tongyi_token
            return context['reply']
        if query.startswith("[cookie]"):
            tongyi_cookie = query.replace('[cookie]', '').replace('"', '').strip()
            context['reply'] = tongyi_cookie
            return context['reply']

        try:
            user_id = context.get('session_id') or context.get('from_user_id')
            context['query'] = query

            # 1.create session
            chat_session = sessions.get(user_id)
            if not chat_session:
                sessionId = self.addSession(context)['sessionId']
                lastChatId = self.getParentMsg(sessionId) # 获取上一条消息的id

                chat_session = dict()
                chat_session['sessionId'] = sessionId
                chat_session['pId'] = lastChatId
                chat_session['ifSearch'] = self.openSearch
                sessions[user_id] = chat_session

            context['session'] = chat_session

            # 2. chat
            context['reply'] = ''
            self.chat(context)

            print(context)
            return context['reply']
        except Exception as e:
            print(e)
            raise Exception("[TONGYI] chat获取失败!!!")

    # 添加会话凭证
    def addSession(self, context):
        headers = self._create_header()
        ##print(headers)
        res = requests.post(url='https://tongyi.aliyun.com/qianwen/addSession', headers=headers, json={
            'firstQuery': context['query']
        })
        logger.info("[TONGYI] query={}, res={}".format(context['query'], str(res.text)))

        return res.json()['data']

    # 获取上一个问题消息id
    def getParentMsg(self, s):
        res = requests.post(url='https://tongyi.aliyun.com/qianwen/queryMessageList', headers=self._create_header(), json={
            'sessionId': s
        })
        logger.info("[TONGYI] sessionId={}, res={}".format(str(s), str(res.text)))

        data = res.json()['data']
        if isinstance(data, list) and len(data) != 0:
            return data[0]['msgId']
        else:
            print('当前为会话的初始的聊天')
            return 0

    def chat(self, context):
        headers = self._create_header(True)
        msgId = str(uuid.uuid4()).replace('-', '') # 生成新消息Id
        data = {
            'action': 'next',
            'msgId': msgId,
            'parentMsgId': context['session']['pId'],
            'contents': [
                {
                    'contentType': 'text',
                    'content': context['query']
                }
            ],
            'openSearch': context['session']['ifSearch'],
            'sessionId': context['session']['sessionId'],
            'model': ''
        }

        ##print(headers)
        ##print(data)
        response = requests.post(url='https://tongyi.aliyun.com/qianwen/conversation', headers=headers, json=data, stream=True)
        ##print(response)

        previous_content = ''
        for line in response.iter_lines():
            if line:
                stripped_line = line.decode('utf-8').replace('data:', '')
                ##print(stripped_line)
                try:
                    data = json.loads(stripped_line)
                    content = data['content'][0]

                    # 去除已经包含在前一条数据中的部分
                    if content.startswith(previous_content):
                        content = content.replace(previous_content, '', 1).strip()

                    print(content.strip(), end='',flush=True)
                    context['session']['pId'] = data['msgId']
                    context['reply'] = context['reply'] + content.strip()

                    previous_content = data['content'][0]  # 更新前一条数据
                except json.decoder.JSONDecodeError as e:
                    print(f"Failed to decode JSON: {e}")    
                    pass

    def _create_header(self, event_stream=False):
        chat_headers = headers.copy()
        if event_stream:
            chat_headers['accept'] = 'text/event-stream' # 启用时间流
        chat_headers['X-Xsrf-Token'] = tongyi_token
        chat_headers['cookie'] = tongyi_cookie
        return chat_headers
