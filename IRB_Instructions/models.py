# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>

from django_countries.fields import CountryField

class Constants(BaseConstants):
    name_in_url = 'IRB_Instructions'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    IRB_accept = models.CharField()

    def set_payoff(self):
        """Calculate payoff, which is zero for the IRB_Instructions"""
        self.payoff = 0