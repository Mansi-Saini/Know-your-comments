from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from home.models import UserProfile, Post
from django.contrib import messages
from home.forms import UserImage

from googleapiclient.discovery import build
import csv
import tweepy
import ssl
import re
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import nltk
import io
import unicodedata
import numpy as np
import re
import string
from numpy import linalg
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import webtext
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from io import BytesIO
import base64

#youtube keys
# AIzaSyAEGvsV19znGbSoUJDT5zkPKOBsDFM2KqY
# api_key = 'AIzaSyCieultKnPOoUFoSusidx48LCTE3c4NgWE'
api_key = 'AIzaSyAEGvsV19znGbSoUJDT5zkPKOBsDFM2KqY'

#twitter keys

link = ''

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')

context = {'pos' : 0, 'neg' : 0, 'neu' : 0, 'link' : link, 'time' : 0}

# Create your views here.
def index(request):
    global context
    if not request.user.is_anonymous:
        u = UserProfile.objects.get(username = request.user)
        context = {'pos' : 0, 'neg' : 0, 'neu' : 0, 'time' : 0, 'lname' : u.lname, 'fname' : u.fname, 'tid' : u.tid, 'yid' : u.yid, 'link' : link}
    else:
        context = {'pos' : 0, 'neg' : 0, 'neu' : 0, 'link' : link, 'time' : 0}
        # return render(request, 'index2.html')
    if request.method == 'POST':
        try:
            def youtubeComments(video_id):
                cmnts = []

                youtube = build('youtube', 'v3',developerKey=api_key)
                video_response = youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()
                time = video_response['items'][0]['snippet']['topLevelComment']['snippet']['publishedAt']
                # context['time'] = time
                context['time'] = time
                # print(context['time'])
                i = 0
                while i < 500:
                    i += 1

                    for item in video_response['items']:
                        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                        replycount = item['snippet']['totalReplyCount']

                        if replycount>0:
                            for reply in item['replies']['comments']:
                                reply = reply['snippet']['textDisplay']
                                
                        cmnts.append(comment)

                    if 'nextPageToken' in video_response:
                        video_response = youtube.commentThreads().list(part = 'snippet,replies',videoId = video_id).execute()
                    else:
                        break
                return cmnts

                
        except:
            pass
        
        def twitterComments(userName, tweet_id):
            consumer_key = "rOFHenppg7Bpz4pm9O7PRFcqx"
            consumer_secret = "L8nK4xmdOD6Y3jKDvdVlpgywTHpnX0iSmFv2t1i8LlO3EQlQxA"
            access_token = "1602983022382698497-3XsBNJhmxl7YGLN1KilSTkk1Uj69XV"
            access_token_secret = "zJSQwvhp3DmVU2InqT8N8nAUEHqa1Mquc9U9gQQkzHqUT"
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            replies = []
            cmnts = []
            user = api.get_status(tweet_id)
            created_at = user.created_at 
            context['time'] = created_at
            # print("The status was created at : " + str(created_at))

            for tweet in tweepy.Cursor(api.search_tweets,q='to:'+name, result_type='recent').items():
                if hasattr(tweet, 'in_reply_to_status_id_str'):
                    if (tweet.in_reply_to_status_id_str==tweet_id):
                        replies.append(tweet)
            
            # with open('static/replies.txt', 'w') as f:
            for tweet in replies:
                t = tweet.text.replace('\n', ' ')
                t = tweet.text.replace(userName, ' ')
                cmnts.append(t)
                    # f.write(t)
                    # f.write('\n')
            return cmnts

        def sentimentAnalysis(text):
            # with open('replies.txt') as f:
            #     text = f.read()

            t = " ".join(text)

            sent_tokenizer = PunktSentenceTokenizer(t)
            sents = sent_tokenizer.tokenize(t)

            porter_stemmer = PorterStemmer()
            nltk_tokens = nltk.word_tokenize(t)

            wordnet_lemmatizer = WordNetLemmatizer()
            nltk_tokens = nltk.word_tokenize(t)

            t = nltk.word_tokenize(t)

            sid = SentimentIntensityAnalyzer()

            d = {'pos' : 0, 'neg' : 0, 'neu' : 0}
            for t in text:
                scores = sid.polarity_scores(t)
                s = scores['compound']
                if s < 0:
                    d['neg'] += 1
                elif s > 0:
                    d['pos'] += 1
                elif s == 0:
                    d['neu'] += 1

            return d

        url = request.POST.get('link')
        if 'youtube' in url:
            video_id = url[-11:]
            text = youtubeComments(video_id)
        
        elif 'twitter' in url:
            match1 = re.search(r'twitter.com/', url)
            match2 = re.search(r'/status/', url)
            name = url[match1.end() : match2.start()]
            tweet_id = url[match2.end() :]
            userName = '@' + name + ' '
            text = twitterComments(userName, tweet_id)

        result = sentimentAnalysis(text)
        context['pos'] = result['pos']
        context['neg'] = result['neg']
        context['neu'] = result['neu']
        context['link'] = url
        l = []
        values = []
        for i, j in result.items():
            l.append(i)
            values.append(j)

        plt.pie(values, labels = l)

        plt.savefig('static/analysis_figures/figure.png')
        context['chart'] = 'static/analysis_figures/figure.png'
        if not request.user.is_anonymous:
            return render(request, 'index.html', context)
        else:
            return render(request, 'index2.html', context)

    
    if not request.user.is_anonymous:
        return render(request, 'index.html', context)
    else:
        return render(request, 'index2.html', context)


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passward = request.POST.get('password')
        user = authenticate(username = username, password = passward)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect("/")

def registerUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passward = request.POST.get('password')
        passward2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'register.html')

        if User.objects.filter(email = email).exists():
            messages.error(request, "You already have a account with this email.")
            return render(request, 'register.html')

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters")
            return render(request, 'register.html')
        
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return render(request, 'register.html')

        if len(passward) < 8:
            messages.error(request, "Password must contain atleast 8 characters")
            return render(request, 'register.html')

        if passward != passward2:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html')

        user = User.objects.create_user(username, email, passward)
        profile =  UserProfile(username = username, email = email, image = 'static/profilePic.jpeg', fname = ' ', lname = ' ', tid = ' ', yid = ' ')
        profile.save()
        user.save()
        user = authenticate(username = username, password = passward)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html')
        return redirect("/")
    
    return render(request, 'register.html')


def userProfile(request):

    if request.user.is_authenticated:
        u = UserProfile.objects.get(username = request.user)
        p = list(Post.objects.filter(username = request.user).values())
        # print(p)
        p.sort(key = lambda x : x['time'])
        context = {
            'email' : request.user.email,
            'lname' : u.lname,
            'fname' : u.fname,
            'yid' : u.yid,
            'tid' : u.tid,
            'image' : u.image.url,
            'post' : p
        }
    if request.method == 'POST':

        if request.user.is_authenticated:
            username = request.user
        email = request.user.email
        lname = request.POST.get('lname')
        fname = request.POST.get('fname')
        tid = request.POST.get('tid')
        yid = request.POST.get('yid')
        image = request.FILES['image']

        context['lname'] = lname
        context['fname'] = fname
        context['tid'] = tid
        context['yid'] = yid
        if UserProfile.objects.filter(username = username).exists():
            u = UserProfile.objects.get(username = username)
            u.lname = lname
            u.save(update_fields=['lname'])
            u.fname = fname
            u.save(update_fields=['fname'])
            u.tid = tid
            u.save(update_fields=['tid'])
            u.yid = yid
            u.save(update_fields=['yid'])
            u.image = image
            u.save(update_fields=['image'])
            path =  u.image.url

            context['image'] = path
            

        else:
            profile = UserProfile(username = username, email = email, fname = fname, lname = lname, tid = tid, yid = yid, image = image)
            profile.save()
            path =  profile.image.url
            context['image'] = path

    return render(request, 'userprofile.html', context)

def about(request):
    if request.user.is_anonymous:
        return render(request, 'about2.html')
    return render(request, 'about.html')
    
def save(request):
    global context
    post = Post(username = request.user, pos = context['pos'], neg = context['neg'], neu = context['neu'], link = context['link'], time = context['time'])
    post.save()
    return redirect("/", context)

def Analysis(request):
    if request.user.is_authenticated:
        # u = UserProfile.objects.get(username = request.user)
        p = list(Post.objects.filter(username = request.user).values())
        # print(p)
        context = {}
        if len(p) == 0:
            context = {'flag': 0, 't': 0, 'y': 0 }
            render(request, "Analysis.html", context)
        
        else:
            p.sort(key = lambda x : x['time'])
            posdt = {}
            negdt = {}
            neudt = {}
            posdy = {}
            negdy = {}
            neudy = {}
            context = {'flag': 1, 't': 0, 'y': 0 }

            for  i in p:
                if 'twitter' in i['link']:
                    context['t'] = 1
                    posdt[i['time']] = i['pos']
                    negdt[i['time']] = i['neg']
                    neudt[i['time']] = i['neu']

                if 'youtube' in i['link']:
                    context['y'] = 1
                    posdy[i['time']] = i['pos']
                    negdy[i['time']] = i['neg']
                    neudy[i['time']] = i['neu']

            # tx = list(total.keys())
            # ty = list(total.values())
            # fig = plt.figure(figsize = (10, 5))
            # plt.bar(tx, ty, width = 0.4)
            # plt.xlabel('Time')
            # plt.ylabel('Number of Comments')
        
            # plt.savefig('static/analysis_figures/total.png')
            # context['total'] = 'static/analysis_figures/total.png'
            if context['t'] == 1:
                px = list(posdt.keys())
                py = list(posdt.values())
                fig = plt.figure(figsize = (10, 5))
                plt.bar(px, py, width = 0.4, color = '#927AF5')
                plt.xlabel('Time')
                plt.ylabel('Number of Comments')
                plt.title("Positive Comment Analysis")
            
                plt.savefig('static/figures/tpositive.png')
                context['tpositive'] = 'static/figures/tpositive.png'

                nx = list(negdt.keys())
                ny = list(negdt.values())
                fig = plt.figure(figsize = (10, 5))
                plt.bar(nx, ny, width = 0.4, color = '#927AF5')
                plt.xlabel('Time')
                plt.ylabel('Number of Comments')
                plt.title("Negative Comment Analysis")
            
                plt.savefig('static/figures/tnegative.png')
                context['tnegative'] = 'static/figures/tnegative.png'

                neux = list(neudt.keys())
                neuy = list(neudt.values())
                fig = plt.figure(figsize = (10, 5))
                plt.bar(neux, neuy, width = 0.4, color = '#927AF5')
                plt.xlabel('Time')
                plt.ylabel('Number of Comments')
                plt.title("Neutral Comment Analysis")
            
                plt.savefig('static/figures/tneutral.png')
                context['tneutral'] = 'static/figures/tneutral.png'

            if context['y'] == 1:
                px = list(posdy.keys())
                py = list(posdy.values())
                fig = plt.figure(figsize = (10, 5))
                plt.bar(px, py, width = 0.4, color = '#927AF5')
                plt.xlabel('Time')
                plt.ylabel('Number of Comments')
                plt.title("Positive Comment Analysis")
            
                plt.savefig('static/figures/ypositive.png')
                context['ypositive'] = 'static/figures/ypositive.png'

                nx = list(negdy.keys())
                ny = list(negdy.values())
                fig = plt.figure(figsize = (10, 5))
                plt.bar(nx, ny, width = 0.4, color = '#927AF5')
                plt.xlabel('Time')
                plt.ylabel('Number of Comments')
                plt.title("Negative Comment Analysis")
            
                plt.savefig('static/figures/ynegative.png')
                context['ynegative'] = 'static/figures/ynegative.png'

                neux = list(neudy.keys())
                neuy = list(neudy.values())
                fig = plt.figure(figsize = (10, 5))
                plt.bar(neux, neuy, width = 0.4, color = '#927AF5')
                plt.xlabel('Time')
                plt.ylabel('Number of Comments')
                plt.title("Neutral Comment Analysis")
            
                plt.savefig('static/figures/yneutral.png')
                context['yneutral'] = 'static/figures/yneutral.png'


        return render(request, 'Analysis.html', context)  