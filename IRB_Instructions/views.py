# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

class IRB(Page):
    form_model = models.Player
    form_fields = ['IRB_accept']

class Instructions(Page):
    pass

page_sequence = [
    IRB,
    Instructions
]
