# -*- coding: utf-8 -*-
from __future__ import division
from otree import widgets
from otree.common import Currency as c
from otree.constants import BaseConstants
from otree.db import models
from otree.models import BaseSubsession, BaseGroup, BasePlayer
import random
from django_countries.fields import CountryField

doc = """ Group C """


class Constants(BaseConstants):
    name_in_url = 'Group_C'
    players_per_group = 2
    num_rounds = 22
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
            p2.own_choice = "NA"
            p1.RU = 1
            p1.SV = 0
            p2.RU = 0
            p2.SV = 0
            p2.own_choice_code = 1
            p1.payoff = Constants.distrust
            p2.payoff = Constants.distrust
        else:
            p1.RU = 0
            p1.SV = 1
            if p2.own_choice == "U":
                p2.RU = 1
                p2.SV = 0
                p2.own_choice_code = 1
                p2.payoff = Constants.defect
                p1.payoff = Constants.defected
            else:
                p2.RU = 0
                p2.SV = 1
                p2.own_choice_code = 0
                p1.payoff = Constants.trust
                p2.payoff = Constants.trust

        p1.own_choice_code = p1.RU
        p2.own_choice_code = p2.RU

        p1.other_choice = p2.own_choice
        p2.other_choice = p1.own_choice

        p1.other_choice_code = p2.own_choice_code
        p2.other_choice_code = p1.own_choice_code

        p1.total_RU = sum([p.RU for p in p1.in_all_rounds()])
        p2.total_RU = sum([p.RU for p in p2.in_all_rounds()])

        p1.total_SV = sum([p.SV for p in p1.in_all_rounds()])
        p2.total_SV = sum([p.SV for p in p2.in_all_rounds()])

        p1.own_score = '(' + str(p1.total_RU) + ',' + str(p1.total_SV) + ')'
        p2.own_score = '(' + str(p2.total_RU) + ',' + str(p2.total_SV) + ')'

#        p1.own_score_ratio = p1.total_RU / (p1.total_SV + 1)
#        p2.own_score_ratio = p2.total_RU / (p2.total_SV + 1)

        p1.other_RU = p2.RU
        p2.other_RU = p1.RU

        p1.other_SV = p2.SV
        p2.other_SV = p1.SV

        p1.pairing_total_RU = p2.total_RU
        p2.pairing_total_RU = p1.total_RU

        p1.pairing_total_SV = p2.total_SV
        p2.pairing_total_SV = p1.total_SV

        p1.other_score = p2.own_score
        p2.other_score = p2.own_score

#        p1.other_score_ratio = p1.other_total_RU / (p1.other_total_SV + 1)
#        p2.other_score_ratio = p2.other_total_RU / (p2.other_total_SV + 1)

        p1.other_payoff = p2.payoff
        p2.other_payoff = p1.payoff

        p1.total_payoff = sum([p.payoff for p in p1.in_all_rounds()])
        p2.total_payoff = sum([p.payoff for p in p2.in_all_rounds()])

        p1.scaled_points = p1.payoff
        p2.scaled_points = p2.payoff - 1

        #LIST MODELS

        p1.choice_history = list([str(p.own_choice) for p in p1.in_all_rounds()])
        p2.choice_history = list([str(p.own_choice) for p in p2.in_all_rounds()])

        p1.choice_code_history = list([int(p.own_choice_code) for p in p1.in_all_rounds()])
        p2.choice_code_history = list([int(p.own_choice_code) for p in p2.in_all_rounds()])

        p1.payoff_history = list([int(p.payoff) for p in p1.in_all_rounds()])
        p2.payoff_history = list([int(p.payoff) for p in p2.in_all_rounds()])

        p1.score_history = list([str(p.own_score) for p in p1.in_all_rounds()])
        p2.score_history = list([str(p.own_score) for p in p2.in_all_rounds()])

        p1.other_choice_history = list([str(p.other_choice) for p in p1.in_all_rounds()])
        p2.other_choice_history = list([str(p.other_choice) for p in p2.in_all_rounds()])

        p1.other_choice_code_history = list([int(p.other_choice_code) for p in p1.in_all_rounds()])
        p2.other_choice_code_history = list([int(p.other_choice_code) for p in p2.in_all_rounds()])

        p1.pairing_choice_history = p2.choice_history
        p2.pairing_choice_history = p1.choice_history

        p1.pairing_choice_code_history = p2.choice_code_history
        p2.pairing_choice_code_history = p1.choice_code_history

        p1.pairing_score_history = p2.score_history
        p2.pairing_score_history = p1.score_history

        #PREVIOUS VALUES
        if self.subsession.round_number > 1:
            p1.own_last_choice = p1.choice_code_history[-2]
            p2.own_last_choice = p2.choice_code_history[-2]

            p1.other_last_choice = p1.other_choice_code_history[-2]
            p2.other_last_choice = p2.other_choice_code_history[-2]

            p1.pairing_last_choice = p2.choice_code_history[-2]
            p2.pairing_last_choice = p1.choice_code_history[-2]
        else:
            p1.own_last_choice = 0
            p2.own_last_choice = 0

            p1.other_last_choice = 0
            p2.other_last_choice = 0

            p1.pairing_last_choice = 0
            p2.pairing_last_choice = 0
        if self.subsession.round_number > 2:
            p1.own_last_three = p1.choice_code_history[-4:-1]
            p2.own_last_three = p2.choice_code_history[-4:-1]

            p1.other_last_three = p1.other_choice_code_history[-4:-1]
            p2.other_last_three = p2.other_choice_code_history[-4:-1]

            p1.pairing_last_three = p2.choice_code_history[-4:-1]
            p2.pairing_last_three = p1.choice_code_history[-4:-1]
        if self.subsession.round_number == 2:
            p1.own_last_three = [0] + p1.choice_code_history
            p1.own_last_three = p1.own_last_three[:-1]
            p2.own_last_three = [0] + p2.choice_code_history
            p2.own_last_three = p2.own_last_three[:-1]

            p1.other_last_three = p1.other_choice_code_history
            p2.other_last_three = p2.other_choice_code_history

            p1.pairing_last_three = p2.choice_code_history[:-1]
            p2.pairing_last_three = p1.choice_code_history[:-1]
        else:
            p1.own_last_three = [0] + p1.choice_code_history
            p1.own_last_three = p1.own_last_three[:-1]
            p2.own_last_three = [0] + p2.choice_code_history
            p2.own_last_three = p2.own_last_three[:-1]

            p1.other_last_three = p1.other_choice_code_history
            p2.other_last_three = p2.other_choice_code_history

            p1.pairing_last_three = p2.choice_code_history[:-1]
            p2.pairing_last_three = p1.choice_code_history[:-1]

        p1.own_last_three_t = sum(p1.choice_code_history)
        p1.other_last_three_t = sum(p1.other_last_three)
        p1.pairing_last_three_t = sum(p1.pairing_last_three)
        p2.own_last_three_t = sum(p2.choice_code_history)
        p2.other_last_three_t = sum(p2.other_last_three)
        p2.pairing_last_three_t = sum(p2.pairing_last_three)

class Player(BasePlayer):
    verification = models.CharField()
    choice_time = models.IntegerField() #ran-out-of-time = 1

    #CHOICE VARIABLES
    own_choice = models.CharField()
    own_choice_code = models.IntegerField()
    own_last_choice = models.IntegerField()
    own_last_three = models.CommaSeparatedIntegerField(max_length=3000)
    own_last_three_t = models.IntegerField()

    other_choice = models.CharField()
    other_choice_code = models.IntegerField()
    other_last_choice = models.IntegerField()
    other_last_three = models.CommaSeparatedIntegerField(max_length=3000)
    other_last_three_t = models.IntegerField()

    pairing_last_choice = models.IntegerField()
    pairing_last_three = models.CommaSeparatedIntegerField(max_length=3000)
    pairing_last_three_t = models.IntegerField()


    RU = models.IntegerField()
    SV = models.IntegerField()
    total_RU = models.IntegerField()
    total_SV = models.IntegerField()
    own_score = models.CharField()
    own_score_ratio = models.FloatField()

    other_RU = models.IntegerField()
    other_SV = models.IntegerField()
    pairing_total_RU = models.IntegerField()
    pairing_total_SV = models.IntegerField()
    other_score = models.CharField()
    other_score_ratio = models.FloatField()

    #POINTS AND PAYOFF VARIABLES
    other_payoff = models.CurrencyField()
    total_payoff = models.CurrencyField()
    scaled_points = models.FloatField()

    #LIST MODEL VARIABLES
    choice_history = models.CommaSeparatedIntegerField(max_length=3000)
    choice_code_history = models.CommaSeparatedIntegerField(max_length=3000)
    payoff_history = models.CommaSeparatedIntegerField(max_length=3000)
    score_history = models.CommaSeparatedIntegerField(max_length=3000)
    other_choice_history = models.CommaSeparatedIntegerField(max_length=3000)
    other_choice_code_history = models.CommaSeparatedIntegerField(max_length=3000)
    pairing_choice_history = models.CommaSeparatedIntegerField(max_length=3000)
    pairing_choice_code_history = models.CommaSeparatedIntegerField(max_length=3000)
    pairing_score_history = models.CommaSeparatedIntegerField(max_length=3000)

    #DEFINES ROLE
    def role(self):
        if self.id_in_group == 1:
            return 'Person 1'
        if self.id_in_group == 2:
            return 'Person 2'
