# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.
class StockProfileModel(models.Model):
    """
    Model representing basic information about a stock including abbreviated name and full name
    """

    #The ticker name is the abbreviated name for a company used on the stock market
    tickerName = models.CharField(max_length=10, primary_key=True)
    #The full name is the full name of the company
    fullName = models.CharField(max_length=50)
    overview = models.CharField(max_length=2000)
    founded = models.CharField(max_length=4)
    category= models.CharField(max_length=50)

    def __unicode__(self):
        return self.fullName




class StockStatusModel(models.Model):
    """
    Model representing information about a stock's status over time; includes date, time of day, high/low price for that date, and current price
    """

    #Which stock is the entry is about
    whichStock = models.ForeignKey(StockProfileModel)
    #The date/time that the entry is for
    date = models.DateTimeField()
    #High price for the stock that day
    highPrice = models.DecimalField(max_digits=8, decimal_places=2)
    #Low Price for the stock that day
    lowPrice = models.DecimalField(max_digits=8, decimal_places=2)
    #Current price for the stock at time of measurement
    currentPrice = models.DecimalField(max_digits=8, decimal_places=2)


    def __unicode__(self):
        return str(self.whichStock) + ': ' + self.date.strftime("%d/%m/%y ; %H:%M")



class TransactionModel(models.Model):
    """
    Model representing transactions that a use has made, keeps track of money spent on stock, amount purchased, date purchased
    """

    #What user the transaction is associated with
    user = models.ForeignKey(User)
    #The amount of money that the user spent on the stock
    amountSpent = models.DecimalField(max_digits=8, decimal_places=2)
    #The number of stocks purchased
    numberPurchased = models.IntegerField()
    #The date on which the stocks were purchased
    datePurchased = models.DateTimeField()
    #The company that the stock purchased was for
    whichStock = models.ForeignKey(StockProfileModel)

    def __unicode__(self):
        return str(self.user) + ': ' + str(self.whichStock) + ' amount:' + str(self.numberPurchased) + ' date: ' + self.datePurchased.strftime("%d/%m/%y ; %H:%M")

class ForumModel(models.Model):
    """
    Model representing transactions that a use has made, keeps track of money spent on stock, amount purchased, date purchased
    """
    #What user the transaction is associated with
    user = models.ForeignKey(User)
    #The message title for the forum
    messageTitle = models.CharField(max_length=200)
    #The number of stocks purchased
    messageBody = models.CharField(max_length=2000)
    #The date on which day it was posted
    datePosted = models.DateTimeField()

    def __unicode__(self):
        return str(self.user) + ': ' + str(self.messageTitle)+ ' date: ' + self.datePosted.strftime("%d/%m/%y ; %H:%M")

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return str(self.label)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
    
    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}
