# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from django.http import HttpResponseRedirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from PocketStock.forms import RegistrationForm, TransactionAddForm

from django.db.models import Q
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from social_django.models import UserSocialAuth

from PocketStock import duo_auth
from datetime import datetime
from stocks import models
from stocks.models import TransactionModel, StockStatusModel, StockProfileModel, Room
import requests
from collections import OrderedDict
from django.db import transaction
import random
import string
import decimal
# Create your views here.
def home(request):
    if request.user.is_authenticated():
        return registered_home(request)
    else:
        return render(request,'base_generic.html')

def publicForum(request):
    # Retreiving all the posts
    posts = models.ForumModel.objects.all().order_by('-datePosted')
    userPosts = []
    for post in posts:
        tempPost = {}
        tempPost['username'] = post.user.username
        tempPost['messageTitle'] = post.messageTitle
        tempPost['messageBody'] = post.messageBody
        tempPost['date'] = post.datePosted.strftime("%b %d, %Y, %HH: %Mm")
        userPosts.append(tempPost)

    return render(request, 'publicforums.html', {'posts': userPosts})

@login_required
@duo_auth.duo_auth_required
def predict(request):
    all_entries = TransactionModel.objects.filter(user=request.user)
    companies1=[]
    companies=[]

    #iterate through to get all companies the user has stocks in
    for i in all_entries:
        if i.whichStock.tickerName not in companies1:
            companies1.append(i.whichStock.tickerName)
            #companies.append(i.whichStock.fullName)
    print companies1
    #print companies

    B={}
    A={}
    #Changes
    count=1
    for i in companies1:
        tickName=i

        respons = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+tickName+'&apikey=2NWT4MKPZ594L2GF')
        #print respons
        ll = json.loads(respons.text)
        if len(ll) is not 1 :

            ll = ll['Time Series (Daily)']
            ll = OrderedDict(sorted(ll.items(), key=lambda t: t[0]))
            #print ll

            B[tickName]=[]

            for x in ll:
               #if count==1:
                   #print x
               #B[tickName]['open'].append(ll[x]['1. open'])
               B[tickName].append(ll[x]['4. close'])
               today= '%.2f' % float(B[tickName][-1])

            sell_stock,future_value= get_prediction(B[tickName])
            A[tickName]=(sell_stock,future_value,today)
            print "A is",A
        else:
            continue
    return render(request, 'prediction.html',{'predictions': A,})

def get_prediction(data_list):
    #print data_list

    data_list1=[]

    for i in range(0,len(data_list)):
        x1=float(data_list[i])

        #print data_list[3:len(data_list[i])-1]
        #data_list1.append(float(data_list[i][3:len1])
        data_list1.append(x1)

    #print data_list1

    def short_predict(data_list1):


        data_list1.reverse()

        count22 = 0.0
        count01 = 0.0
        count10 = 0.0
        percentage = 0.0
        v=len(data_list1)-20


        for i in range(v, len(data_list1) - 1):
            #print data_list1[i]
            percentage += float((data_list1[i + 1] - data_list1[i]) / data_list1[i])
            if data_list1[i] > data_list1[i + 1]:
                count10 += 1
            elif data_list1[i] < data_list1[i + 1]:
                count01 += 1
            else:
                count22 += 1
        count10 = float(count10 / len(data_list1))
        count01 = float(count01 / len(data_list1))
        count22 = float(count22 / len(data_list1))

        if count10 > count22 and count10 > count01:
            return "Sell the Stock (Day Trading)"
        elif count01 > count22 and count01 > count10:
            return "Buy more of this Stock (Day Trading)"
        elif count22 > count01 and count22 > count10:
            return "Keep holding to the stock (Day Trading)"
        else:
            return "Keep holding to the stock (Day Trading)"




    def long_predict(data_list1):


        data_list1.reverse()

        percentage = 0.0
        for i in range(0, len(data_list1) - 1):
            percentage += float((data_list1[i + 1] - data_list1[i]) / data_list1[i])


        predict = (1 + percentage / 100) * data_list1[len(data_list1) - 1]
        for i in range(0, 7):
            predict = predict * (1 + percentage / 100)

        return ('%.2f' % predict)

    #return short_predict(data_list1)
    return short_predict(data_list1),long_predict(data_list1)

@login_required
@duo_auth.duo_auth_required
def registered_home(request):
    all_entries = TransactionModel.objects.filter(user=request.user)

    #we need to pass the user a series of associated objects with the following characteristics
    #quantity, percent, currentPrice, companyName, valuation

    output_list = []

    companies = []

    #iterate through to get all companies the user has stocks in
    for i in all_entries:
        if i.whichStock not in companies:
            companies.append(i.whichStock)

    company_statuses = {}

    #get the most recent status of the companies that the user has stock in
    for i in companies:
        company_statuses[i] = StockStatusModel.objects.filter(whichStock=i).order_by('date')[0].currentPrice

    # company_fullnames = {}

    # #get the full name of the companies that the user has stock in
    # for i in companies:
    #     company_fullnames[i] = StockProfileModel.objects.get(tickerName=i).fullName

    #Associate all related info
    for i in all_entries:
        obj = {}
        obj['qty'] = i.numberPurchased
        obj['percent'] = round((company_statuses[i.whichStock] - (i.amountSpent / i.numberPurchased)) / (i.amountSpent / i.numberPurchased) * 100, 2)
        obj['currentPrice'] = company_statuses[i.whichStock]
        obj['fullname'] = i.whichStock.fullName
        link = '/stockProfile?stockname=' + i.whichStock.tickerName
        obj['link'] = link
        obj['valuation'] = '%.2f' % float(i.numberPurchased * company_statuses[i.whichStock])
        output_list.append(obj)

    return render(request, 'dashboard.html', {
        'transactions': output_list,
        })

@login_required
@duo_auth.duo_auth_required
def settings(request):
    user = request.user
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
        })


@login_required
@duo_auth.duo_auth_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/dashboard')
    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {'form': form})


@login_required
@duo_auth.duo_auth_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionAddForm(request.POST)
        if form.is_valid():
            #process data
            form.save(request.user)
            return redirect('/dashboard')
    else:
        form = TransactionAddForm()

    return render(request, 'create_transaction.html', {'form': form})

@login_required
@duo_auth.duo_auth_required
def searchResults(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        #Before Changes
        # results = StockProfileModel.objects.filter(Q(tickerName__icontains=query)|Q(fullName__icontains=query))
        # if len(results) == 1:
        #     link = '/stockProfile?stockname='+ results[0].tickerName
        #     return redirect(link)
        # resultsToSend = {}
        # for i in range(0, len(results)):
        #     link = '/stockProfile?stockname='+ results[i].tickerName
        #     resultsToSend[results[i].fullName] = link
        # return render(request, 'searchresults.html', {'searchres': resultsToSend})

        #After Changes
        qu= request.GET['category']
        print query
        print qu
        resultsToSend = {}
        results = StockProfileModel.objects.filter(Q(tickerName__icontains=query)|Q(fullName__icontains=query))
        print "results",results
        if qu !="All":
            results1= StockProfileModel.objects.filter(Q(category__icontains=qu))
            print results1
            if not query:
                print "yes"
                for i in range(len(results1)):
                    link = '/stockProfile?stockname='+ results1[i].tickerName
                    resultsToSend[results1[i].fullName] = link
            else:
                i=0
                Search={}
                for i in range(len(results)):
                    Search[i]=results[i]
                print Search
                for j in range(len(results1)):
                    print results1[j]

                    if results1[j] in Search.values():
                        if len(results)==1:
                             print "success"
                             link = '/stockProfile?stockname='+ results1[j].tickerName
                             return redirect(link)
                        else:
                             print "success"
                             link = '/stockProfile?stockname='+ results1[j].tickerName
                             resultsToSend[results1[j].fullName] = link

        else:
            if len(results) == 1:
                link = '/stockProfile?stockname='+ results[0].tickerName
                return redirect(link)

            for i in range(0, len(results)):
                link = '/stockProfile?stockname='+ results[i].tickerName

                resultsToSend[results[i].fullName] = link
        return render(request, 'searchresults.html', {'searchres': resultsToSend,'categ':qu})

def getDashBoardData(request):
    # get all transactions made by the current user
    all_entries = TransactionModel.objects.filter(user=request.user)

    # we need to pass the user a series of associated objects with the following characteristics
    # quantity, percent, currentPrice, companyName, valuation

    output_list = {}

    companies = []

    # iterate through to get all companies the user has stocks in
    for i in all_entries:
        if i.whichStock not in companies:
            print i.whichStock.tickerName
            companies.append(i.whichStock)

    company_statuses = {}
    # get the most recent status of the companies that the user has stock in
    # for i in companies:
    #     company_statuses[i] = StockStatusModel.objects.filter(whichStock=i).order_by('date')[0].currentPrice

    # Company status object has company name
    # Making the API call to get the real time data
    APIKEY = '2NWT4MKPZ594L2GF'
    for i in companies:
        companyShortName = i.tickerName
        function = 'TIME_SERIES_INTRADAY'
        # api-endpoint
        URL = "https://www.alphavantage.co/query?function=" + function + "&symbol=" + companyShortName + "&interval=1min&outputsize=compact&apikey=" + APIKEY
        data = None
        try:
            # sending get request and saving the response as response object
            response = requests.get(url=URL)
            if response.headers['Via'] == '1.1 vegur':
                # print 'Status OK'
                # extracting data in json format
                data = response.json()
                lastRefreshed = data['Meta Data']['3. Last Refreshed']
                company_statuses[i] = decimal.Decimal(data['Time Series (1min)'][lastRefreshed]['4. close'])
            else:
                print "Api didn't respond"
                company_statuses[i] = decimal.Decimal('0')
                return HttpResponse('failure')
        except:
            company_statuses[i] = decimal.Decimal('0')
            return HttpResponse('failure')
    row = 0;
    # Associate all related info
    for i in all_entries:
        row = row + 1
        obj = {}
        obj['qty'] = i.numberPurchased
        obj['percent'] = str(round((company_statuses[i.whichStock] - (i.amountSpent / i.numberPurchased)) / (
            i.amountSpent / i.numberPurchased) * 100, 2))
        obj['currentPrice'] = str(company_statuses[i.whichStock])
        obj['fullname'] = i.whichStock.fullName
        link = '/stockProfile?stockname=' + i.whichStock.tickerName
        obj['link'] = link
        obj['valuation'] = str('%.2f' % (i.numberPurchased * company_statuses[i.whichStock]))
        output_list[row] = obj

    return HttpResponse(json.dumps(output_list), content_type="application/json");

def getCompanyDomain(companyName):
    URL = 'https://api.fullcontact.com/v2/company/search.json?apiKey=5556c95482238100&companyName=' + companyName
    try:
        # sending get request and saving the response as response object
        response = requests.get(url=URL)
        data = response.json()
        for i in data:
            return str(i['lookupDomain'])
            break;
    except Exception as e:
        print e
        return 'Completed'

def insertData(request):
    k={
        'WFC':'Wells Fargo & Co',
        'WMT' : 'Walmart',
        'GOOGL' : 'Alphabet Inc',
        'XOM' : 'Exxon Mobil Corporation',
        'FB' : 'Facebook',
        'TWTR': 'Twitter',
        'CRM': 'Salesforce.com',
        'ORCL': 'Oracle Corporation',
        'GS': 'Goldman Sachs Group Inc',
        'JPM': 'JPMorgan Chase & Co.',
        'AAPL':'Apple Inc',
    }
    #code to companies to the stockprofile model
    for i in k.keys():
        s = StockProfileModel(tickerName=i, fullName=k[i])
        s_ins = StockProfileModel.objects.get(tickerName=i)
        domain = getCompanyDomain(s_ins.fullName)
        print domain

        URL = 'https://api.fullcontact.com/v2/company/lookup.json?apiKey=5556c95482238100&domain=' + domain
        try:
            # sending get request and saving the response as response object
            response = requests.get(url=URL)
            data = response.json()
            s_ins.overview = data['organization']['overview']
            s_ins.founded = data['organization']['founded']

        except:
            s_ins.overview = "couldn't Fetch"
            s_ins.founded = "couldn't fetch"

        s_ins.save()

    return HttpResponse('done')
    #code to add stocks
    # tickName = 'AAPL'
    # respons = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+tickName+'&apikey=2NWT4MKPZ594L2GF')
    # ll = json.loads(respons.text)
    # ll = ll['Time Series (Daily)']
    # for i in ll.keys():
    #     s = i
    #     s = s + ' 00:00:00'
    #
    #     datetime_object = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    #     s_ins = StockProfileModel.objects.get(tickerName=tickName)
    #     s = StockStatusModel(whichStock=s_ins, date=datetime_object, highPrice=ll[i]['2. high'], lowPrice = ll[i]['3. low'], currentPrice=ll[i]['4. close'])
    #     s.save()


@login_required
@duo_auth.duo_auth_required
def getCompanies(request):
    query = request.GET.get('query')
    results = StockProfileModel.objects.all()
    ll = {}
    for result in results:
        ll[result.fullName] = result.fullName
    return HttpResponse(json.dumps(ll) ,content_type="application/json")

@login_required
@duo_auth.duo_auth_required
def stockProfile(request):
    tickerName = request.GET.get('stockname')
    s_ins = StockProfileModel.objects.get(tickerName=tickerName)
    dataForStock = StockStatusModel.objects.filter(whichStock = s_ins).order_by('date')
    finalData = OrderedDict()
    for data in dataForStock:
        tempMap = {'highPrice': str(data.highPrice), 'lowPrice': str(data.lowPrice), 'closePrice': str(data.currentPrice)}
        finalData[data.date.strftime('%Y/%m/%d')] = tempMap
    finalData = json.dumps(finalData)
    #print finalData
    return render(request, 'StockProfile.html',{'stockName': s_ins.fullName,'tickerName':s_ins.tickerName,'overview':s_ins.overview,'founded':s_ins.founded, 'finalData': finalData})

@login_required
@duo_auth.duo_auth_required
def forumPage(request):

    #Getting the post details  from the post request
    postTitle =  request.POST.get('posttitle')
    postBody =  request.POST.get('postbody')
    if postBody != None:
        #Saving the post
        post = models.ForumModel()
        post.user = request.user
        post.messageTitle = postTitle
        post.messageBody = postBody
        post.datePosted = datetime.now()
        post.save()

    #Retreiving all the posts
    posts = models.ForumModel.objects.all().order_by('-datePosted')
    userPosts = []
    for post in posts:
        tempPost = {}
        tempPost['username'] = post.user.username
        tempPost['messageTitle'] = post.messageTitle
        tempPost['messageBody'] = post.messageBody
        tempPost['date'] = post.datePosted.strftime("%b %d, %Y, %HH: %Mm")
        userPosts.append(tempPost)

    return render(request,'forum.html',{'posts':userPosts})


@login_required
@duo_auth.duo_auth_required
def chat_room(request, label):

    #check to make sure that this use is connecting to the proper chat room
    #only advisors should be able to connect to chat rooms that don't belong to them
    if ('advisor' not in request.user.groups.values_list('name', flat=True) and label != request.user.username):
        return chat_room(request, request.user.username)

    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room, created = Room.objects.get_or_create(label=label)

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "room.html", {
        'room': room,
        'messages': messages,
    })


@login_required
@duo_auth.duo_auth_required
def chat_room_direct(request):
    """directs a user to the proper chat room or redirects an admin to the admin chat room layout"""
    if ('advisor' in request.user.groups.values_list('name', flat=True)):
        return chat_room_admin(request)
    else:
        return HttpResponseRedirect('/chat/' + request.user.username)
        #return chat_room(request, request.user.username)


@login_required
@duo_auth.duo_auth_required
def chat_room_admin(request):
    """allows an admin to connect to any chatroom"""

    rooms = Room.objects.all()

    return render(request, "admin_chat_room.html", {
        'rooms': rooms
        })


@login_required
@duo_auth.duo_auth_required
def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            #label = haikunator.haikunate()
            label = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(chat_room, label=label)
