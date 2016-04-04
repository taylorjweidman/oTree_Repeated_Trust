# -*- coding: utf-8 -*-
from __future__ import division
from otree import widgets
from otree.common import Currency as c
from otree.constants import BaseConstants
from otree.db import models
from otree.models import BaseSubsession, BaseGroup, BasePlayer
import random

doc = """ Group C """


class Constants(BaseConstants):
    name_in_url = 'Group_C'
    players_per_group = 2
    num_rounds = 15
    distrust = c(2)
    defect = c(6)
    defected = c(0)
    trust = c(3)
    endowment = c(4)
    first_cash = c(0)
    first_choice = 0

class Subsession(BaseSubsession):
    def is_displayed(self):
        return self.round_number > 1

    def before_session_starts(self):
        players = self.get_players()
        random.shuffle(players)

        players_1 = [p for p in players if p.id_in_group == 1]
        players_2 = [p for p in players if p.id_in_group == 2]

        group_matrix = []
        num_groups = int(len(players) / 2)

        for i in range(num_groups):
            new_group = [
                players_1.pop(),
                players_2.pop(),
            ]
            group_matrix.append(new_group)
        self.set_groups(group_matrix)

class Group(BaseGroup):
    group_choice = models.CharField()

    def set_variables(self):
        p1 = self.get_player_by_role('Person 1')
        p2 = self.get_player_by_role('Person 2')
        if p1.own_choice == "R":
            self.group_choice = "R"
            p1.RU = 1
            p1.SV = 0
            p1.payoff = Constants.distrust
            p2.RU = p2.SV = 0
            p2.payoff = Constants.distrust
            p2.own_choice = "NA"
            p1.other_payoff = p2.payoff
            p2.other_payoff = p1.payoff
        else:
            p1.RU = 0
            p1.SV = 1
            if p2.own_choice == "U":
                p1.payoff = Constants.defected
                p2.RU = 1
                p2.SV = 0
                p2.payoff = Constants.defect
                self.group_choice = "U"
                p1.other_payoff = p2.payoff
                p2.other_payoff = p1.payoff
            else:
                p1.payoff = Constants.trust
                p2.RU = 0
                p2.SV = 1
                p2.payoff = Constants.trust
                p1.other_payoff = p2.payoff
                p2.other_payoff = p1.payoff
        self.group_choice = "V"
        p1.other_choice = p2.own_choice
        p2.other_choice = p1.own_choice
        p1.total_payoff = sum([p.payoff for p in p1.in_all_rounds()])
        p2.total_payoff = sum([p.payoff for p in p2.in_all_rounds()])
        p1.total_RU = sum([p.RU for p in p1.in_all_rounds()])
        p1.total_SV = sum([p.SV for p in p1.in_all_rounds()])
        p2.total_RU = sum([p.RU for p in p2.in_all_rounds()])
        p2.total_SV = sum([p.SV for p in p2.in_all_rounds()])
        p1.own_score = '('+str(p1.total_RU)+','+str(p1.total_SV)+')'
        p2.own_score = '('+str(p2.total_RU)+','+str(p2.total_SV)+')'
        p1.other_score = p2.own_score
        p2.other_score = p1.own_score

class Player(BasePlayer):

    other_payoff = models.CurrencyField()
    total_payoff = models.CurrencyField()

    own_choice = models.CharField(
        choices=['R', 'S', 'U', 'V'],
        doc="""Outcome of decision tree""",
        widget=widgets.RadioSelect())

    other_choice = models.CharField()
    RU = models.IntegerField()
    SV = models.IntegerField()
    total_RU = models.IntegerField()
    total_SV = models.IntegerField()
    own_score = models.CharField()
    other_score = models.CharField()
    choice_time = models.IntegerField() #in seconds

    def role(self):
        if self.id_in_group == 1:
            return 'Person 1'
        if self.id_in_group == 2:
            return 'Person 2'
