import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from arzyab import app, db, bcrypt
from arzyab.forms import RegistrationForm, LoginForm, UpdateAccountForm
from arzyab.models import User
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import and_, or_, not_
from datetime import datetime
from threading import Timer
 
from flask import Flask, Response
# import json
import urllib3
from flask import jsonify
from urllib.request import urlopen
import json
import requests
from requests import get
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO
import urllib.request  
import brotli



Data = [
        {
        'NPriceB' : 0.00000,
        'NAmountB' : 0.0,
        'NPriceS' : 0.00000,
        'NAmountS' : 0.0,
        'WPriceB' : 0.00000,
        'WAmountB' : 0.0,
        'WPriceS' : 0.00000,
        'WAmountS' : 0.0
        },
        {
        'NPriceB' : 0.00000,
        'NAmountB' : 0.0,
        'NPriceS' : 0.00000,
        'NAmountS' : 0.0,
        'WPriceB' : 0.00000,
        'WAmountB' : 0.0,
        'WPriceS' : 0.00000,
        'WAmountS' : 0.0
        }
    ]

def assign():

    Data = [
        {
        'NPriceB' : 1.00000,
        'NAmountB' : 1.0,
        'NPriceS' : 1.00000,
        'NAmountS' : 1.0,
        'WPriceB' : 1.00000,
        'WAmountB' : 1.0,
        'WPriceS' : 1.00000,
        'WAmountS' : 1.0
        },
        {
        'NPriceB' : 1.00000,
        'NAmountB' : 1.0,
        'NPriceS' : 1.00000,
        'NAmountS' : 1.0,
        'WPriceB' : 1.00000,
        'WAmountB' : 1.0,
        'WPriceS' : 1.00000,
        'WAmountS' : 1.0
        }
    ]



# def checkApi():
#     URL = "https://wallex.ir/markets/btc-tmn"
    
#     resp = requests.get(
#             URL, 
#             headers={
                
#                 'Host': 'wallex.ir',
#                 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#                 'Accept-Language': 'en-US,en;q=0.5',
#                 'Accept-Encoding': 'gzip, deflate, br',
#                 'Connection': 'keep-alive',
#                 'Cookie': 'XSRF-TOKEN=R1Vva4xKuGxw5NeN32X4NKeb5XBg6iiO8SV6YCCx; wallex_session=6rUF5naivYoQybY5IWmq0oktXQKUcwEMGJ6f0n25; analytics_campaign={%22source%22:%22direct%22%2C%22medium%22:null}; analytics_session_token=866d654e-a15f-7236-b446-49d34e4762e4; analytics_token=92e6bc78-e5b9-1ab6-fddd-6a383dde4465; yektanet_session_last_activity=7/17/2021; _yngt_iframe=1; _yngt=43e8f886-68d54-4ccd0-0af17-7c1235896192a',
#                 'Upgrade-Insecure-Requests': '1',
#                 'Sec-GPC': '1'
#             }
#         )
#     page = brotli.decompress(resp.content)

#     soup = BeautifulSoup(page, "html.parser")
#     resultsS = soup.find(id="sellers-table")
#     elements = resultsS.find_all("td", class_="value req-sell")
#     # for job_element in job_elements:
#     #     print(job_element.findNext('td'), end="\n"*2)

#     assign()

#     Data[0]['WAmountS'] = float(elements[0].contents[0][1:-1].replace(',',''))
#     Data[0]['WPriceS'] = (elements[0].findNext('td').contents[0][1:-1].replace(',',''))
    
#     resultsB = soup.find(id="buyers-table")
#     elementsB = resultsB.find_all("td", class_="value req-buy")
    
#     # for element in elementsB:
#     #     print(element.findNext('td'), end="\n"*2)

#     Data[0]['WAmountB'] = float(elementsB[0].contents[0][1:-1].replace(',',''))
#     Data[0]['WPriceB'] = (elementsB[0].findNext('td').contents[0][1:-1].replace(',',''))

#     print(Data[0])
#     return page
    

def nobitex(market):
    if market == 'btc' :
        nobitex_url = 'https://api.nobitex.ir/v2/orderbook/BTCIRT'
        
    elif market == 'eth':
        nobitex_url = 'https://api.nobitex.ir/v2/orderbook/ETHIRT'

    resp = requests.get(
                nobitex_url, 
                headers={
                    'Content-Type': 'application/json',
                    'access-control-allow-origin': 'https://nobitex.ir'}
            )
    json_resp = json.loads(resp.text)
    global Data
    assign()
    if market=='btc':
        Data[0]['NPriceS'] = int(json_resp["bids"][0][0])/10
        Data[0]['NAmountS'] = float(json_resp["bids"][0][1])
        Data[0]['NPriceB'] = int(json_resp["asks"][0][0])/10
        Data[0]['NAmountB'] = float(json_resp["asks"][0][1])
    elif market=='eth':
        Data[1]['NPriceS'] = int(json_resp["bids"][0][0])/10
        Data[1]['NAmountS'] = float(json_resp["bids"][0][1])
        Data[1]['NPriceB'] = int(json_resp["asks"][0][0])/10
        Data[1]['NAmountB'] = float(json_resp["asks"][0][1])

def wallex(market):
    if market == 'btc' :
        URL = "https://wallex.ir/markets/btc-tmn"
    elif market == 'eth':   
        URL = "https://wallex.ir/markets/eth-tmn"
    resp = requests.get(
            URL, 
            headers={
                
                
                'Host': 'wallex.ir',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cookie': 'analytics_campaign={%22source%22:%22direct%22%2C%22medium%22:null}; analytics_token=92e6bc78-e5b9-1ab6-fddd-6a383dde4465; yektanet_session_last_activity=7/18/2021; _yngt=43e8f886-68d54-4ccd0-0af17-7c1235896192a; XSRF-TOKEN=rtjjo6NCjlTxaNgtoCASs7zfc4AgSx8JgtVK6lS6; wallex_session=ehI2Svf4Xrw0pTrkc9oD1DjikFeDxzT8AIYxzOnn; analytics_session_token=f05bd49d-8061-7c13-bac8-d37a07df30de; _yngt_iframe=1',
                'Upgrade-Insecure-Requests': '1',
                'Sec-GPC': '1'
            }
        )   
    page = brotli.decompress(resp.content)
    soup = BeautifulSoup(page, "html.parser")

    assign()
    resultsS = soup.find(id="sellers-table")
    elements = resultsS.find_all("td", class_="value req-sell")
    if market == 'btc' :
        Data[0]['WAmountS'] = float(elements[0].contents[0][1:-1].replace(',',''))
        Data[0]['WPriceS'] = int(elements[0].findNext('td').contents[0][1:-1].replace(',',''))
    elif market=='eth':
        Data[1]['WAmountS'] = float(elements[0].contents[0][1:-1].replace(',',''))
        Data[1]['WPriceS'] = int(elements[0].findNext('td').contents[0][1:-1].replace(',',''))
    
    resultsB = soup.find(id="buyers-table")
    elementsB = resultsB.find_all("td", class_="value req-buy")
    if market == 'btc' :
        Data[0]['WAmountB'] = float(elementsB[0].contents[0][1:-1].replace(',',''))
        Data[0]['WPriceB'] = int(elementsB[0].findNext('td').contents[0][1:-1].replace(',',''))
    elif market=='eth':
        Data[1]['WAmountB'] = float(elementsB[0].contents[0][1:-1].replace(',',''))
        Data[1]['WPriceB'] = int(elementsB[0].findNext('td').contents[0][1:-1].replace(',',''))



    


def update_data(market):
    #nobitex
    # Timer(interval, update_data, [interval]).start()
    nobitex(market)
    #wallex
    wallex(market)


@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    
    return render_template('dashboard.html', image_file=image_file)

flag = True
@app.route("/dashboard/<market>")
@login_required
def market_type(market):
    
    update_data(market)
    bp1 = ((Data[0]['WPriceS'] - Data[0]['NPriceB'])/Data[0]['NPriceB'])*100
    bp2 = ((Data[0]['NPriceS'] - Data[0]['WPriceB'])/Data[0]['WPriceB'])*100

    ep1 = ((Data[1]['WPriceS'] - Data[1]['NPriceB'])/Data[1]['NPriceB'])*100
    ep2 = ((Data[1]['NPriceS'] - Data[1]['WPriceB'])/Data[1]['WPriceB'])*100

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    if market=='eth':
        p1=ep1
        p2=ep2
        market='Etherium'
    elif market=='btc':
        p1=bp1
        p2=bp2
        market='Bitcoin'

    if p1>p2:
        totalp = p1
    else:
        totalp = p2

    global flag

    acceptablep = 1.5
    if totalp > acceptablep:
        flag = True
    if flag and totalp > acceptablep:
        flag = False
    if totalp < acceptablep:
        flag = False
    return render_template('dashboard.html', image_file=image_file, market=market, Data=Data, totalp=totalp, flag=flag)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/about")
def about():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('about.html', title='About', image_file=image_file)
