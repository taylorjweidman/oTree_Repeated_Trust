# -*- coding: utf-8 -*-
from __future__ import division
from ._builtin import Page, WaitPage
from . import models
from .models import Constants

def before_session_starts(self):
    for p in self.get_players():
        p.payoff = 0

class ShuffleWaitPage(WaitPage):
    def is_displayed(self):
        return self.subsession.round_number > 1

    def after_all_players_arrive(self):

        # sort players by 'score'
        # see python docs on sorted() function
        sorted_players = sorted(
            self.subsession.get_players(),
            key=lambda player: player.participant.vars['score']
        )

        # chunk players into groups
        group_matrix = []
        ppg = Constants.players_per_group
        for i in range(0, len(sorted_players), ppg):
            group_matrix.append(sorted_players[i:i+ppg])

        # set new group
        self.subsession.set_groups(group_matrix)

class Pre_Round_Page(WaitPage):
    def after_all_players_arrive(self):
        p1 = self.group.get_player_by_role('Person 1')
        p2 = self.group.get_player_by_role('Person 2')
        p1.own_choice = p1.own_score = p1.other_choice = p1.other_score = "Current"
        p2.own_choice = p2.own_score = p2.other_choice = p2.other_score = "Current"

class First_Choice(Page):
    form_model = models.Player
    form_fields = ['own_choice']
    timeout_seconds = 100

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return {'player_in_all_rounds': player_in_all_rounds}

class WaitForP1(WaitPage):
    def after_all_players_arrive(self):
        p1 = self.group.get_player_by_role('Person 1')
        self.group.group_choice = p1.own_choice

class Second_Choice(Page):
    form_model = models.Player
    form_fields = ['own_choice']
    timeout_seconds = 100

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.group.group_choice == "S"

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return {'player_in_all_rounds': player_in_all_rounds}

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        p1 = self.group.get_player_by_role('Person 1')
        p2 = self.group.get_player_by_role('Person 2')
        self.group.set_variables()

class Results(Page):
    timeout_seconds = 100

class ResultsSummary(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

page_sequence = [
    Pre_Round_Page,
    First_Choice,
    WaitForP1,
    Second_Choice,
    ResultsWaitPage,
    Results
]
