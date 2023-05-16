# encoding:utf-8

from model.model import Model
from config import model_conf, common_conf_val
from common import const
from common import log
import openai
import time

from model._24._24 import _24


class _24Model(Model):
    def __init__(self):
        log.info("24点")

    def reply(self, query, context=None):
        try:
            list = _24.calcuate(query)
            return '\n'.join(list) if len(list) > 0 else "None"
        except:
            return "格式：num num num num, 比如输入：@me 12 12 12 12 "
