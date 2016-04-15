# -*- coding: utf-8 -*-
from __future__ import division
from ._builtin import Page, WaitPage
from . import models
from .models import Constants
import random

class Verification(Page):
    form_model = models.Player
    form_fields = ['verification']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def before_next_page(self):
        self.player.participant.label = self.player.verification

class Pre_Round_Page(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        p1 = self.group.get_player_by_role('Person 1')
        p2 = self.group.get_player_by_role('Person 2')
        p1.own_choice = p1.own_score = p1.other_choice = p1.other_score = "Current"
        p2.own_choice = p2.own_score = p2.other_choice = p2.other_score = "Current"

        #LIST MODELS
        p1.pairing_choice_history = p2.choice_history
        p1.pairing_score_history = p2.score_history
        p1.pairing_payoff_history = p2.payoff_history
        p2.pairing_choice_history = p1.choice_history
        p2.pairing_score_history = p1.score_history
        p2.pairing_payoff_history = p1.payoff_history

class First_Choice(Page):
    form_model = models.Player
    form_fields = ['own_choice']
    timeout_seconds = 50

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return {'player_in_all_rounds': player_in_all_rounds}

    def before_next_page(self):
        if self.timeout_happened:
            p1 = self.group.get_player_by_role('Person 1')
            p1.own_choice = 'S'
        self.player.choice_time = 0
        if self.timeout_happened:
            self.player.choice_time = 1

class WaitForP1(WaitPage):
    def after_all_players_arrive(self):
        p1 = self.group.get_player_by_role('Person 1')
	p2 = self.group.get_player_by_role('Person 2')
        self.group.group_choice = p1.own_choice
	p2.other_choice = p1.own_choice
#	self.group.set_pre_variables()

class Second_Choice(Page):
    form_model = models.Player
    form_fields = ['own_choice']
    timeout_seconds = 50

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.group.group_choice == "S"

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return {'player_in_all_rounds': player_in_all_rounds}

    def before_next_page(self):
        if self.timeout_happened:
            p2 = self.group.get_player_by_role('Person 2')
            p2.own_choice = 'V'
        self.player.choice_time = 0
        if self.timeout_happened:
            self.player.choice_time = 1

class No_Choice(Page):
    timeout_seconds = 10
    def is_displayed(self):
        return self.player.id_in_group == 2 and self.group.group_choice == "R"

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        p1 = self.group.get_player_by_role('Person 1')
        p2 = self.group.get_player_by_role('Person 2')
        self.group.set_variables()

class Results(Page):
    timeout_seconds = 30

class ResultsSummary(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

page_sequence = [
    Verification,
    Pre_Round_Page,
    First_Choice,
    WaitForP1,
    Second_Choice,
    No_Choice,
    ResultsWaitPage,
    Results
]
