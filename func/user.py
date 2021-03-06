import discord

from . import backend
from pprint import pprint
from .logger import logger
from typing import Dict, List, Union
from dataclasses import dataclass

@dataclass
class User:
    u_name: str
    u_id: str
    dc_user: discord.User
    uuid: str = ''
    finished: bool = False
    prob_list = {}

    def register(self):
        payload = {
            "name": self.u_name,
            "platform": "Discord",
            "platform_userid": self.u_id
        }

        res = backend.seacher(self.u_id)

        if res:
            self.uuid = res['player_uuid']
            return True
        
        res = backend.register(payload)

        if res:
            self.uuid = res['player_uuid']
            return True

        return False

    def get_problem(self):
        if self.finished:
            prob = backend.get_feed_rand(self.uuid)
        else:
            prob = backend.get_feed(self.uuid)

        if not prob:
            self.finished = True
            return
        
        if prob['description'] not in self.prob_list:
            self.prob_list[prob['description']] = ""

        self.prob_list[prob['description']] = prob
        return prob

    def check_ans(self, title, answer):
        if title not in self.prob_list:
            logger.warn('can not find quiz in user\'s prob list')
            return "Error iIndex"

        payload = {
            "player_uuid": self.uuid,
            "quiz_uuid": self.prob_list[title]['quiz_uuid'],
            "answer": self.prob_list[title]['options'][answer]
        }
        ans = backend.get_ans(payload) 
        return ans

    def get_status(self):
        return backend.get_status(self.uuid)
