# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from stocks.models import *

# Register your1 models here.
admin.site.register(StockProfileModel)
admin.site.register(StockStatusModel)
admin.site.register(TransactionModel)
admin.site.register(ForumModel)
admin.site.register(Room)
admin.site.register(Message)