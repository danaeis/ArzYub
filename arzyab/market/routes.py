from flask import Blueprint
from flask import render_template, url_for, request
from flask_login import current_user, login_required
from arzyab.market.utils import update_data, Data
from arzyab.models import Wallex, Nobitex
from arzyab.market.forms import FilterRecordsForm

market = Blueprint('market', __name__)

flag = False
cflag =False
@market.route("/dashboard/market/<market>")
@login_required
def market_type(market):
    
    if not (market=="btc" or market=="eth"):
        return url_for('main.dashboard')
    totalp = update_data(market)
    
    global flag 
    global cflag
    acceptablep = 1
    print('*******************************************')
    print(totalp, '&&&&&&&', acceptablep)
    # print('*******************************************')
    # 
    if (totalp < acceptablep):
        flag = False
        cflag = False
    if (not flag) and (totalp > acceptablep):
        flag = True
        cflag = True
    elif (flag) and (totalp > acceptablep):
        cflag = False
    print(flag, "flag and cflag", cflag)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('dashboard.html', image_file=image_file, market=market, Data=Data, totalp=totalp, flag=(flag and cflag))

form_data =[
{
    'search' : "",
    'fromdate' : "",
    'todate' : ""
}]

@market.route("/dashboard/records" , methods=['GET', 'POST'])
@login_required
def price_records():  
    global form_data
    page = request.args.get('page', 1, type=int)
    if request.method=='POST':
        
        form = FilterRecordsForm(request.form)
        form_data[0]['search'] = form.search.data
        form_data[0]['fromdate'] = form.fromdate.data
        form_data[0]['todate'] = form.todate.data            
        print("var",form_data)
        if form_data[0]['fromdate'] != None and form_data[0]['todate'] != None:
            nob = Nobitex.query.filter_by(curr=form.search.data).filter(Nobitex.date_created >= form.fromdate.data).order_by(Nobitex.date_created.desc()).paginate(page=page, per_page=50)
            wal = Wallex.query.filter_by(curr=form.search.data).filter(Wallex.date_created >= form.fromdate.data).order_by(Wallex.date_created.desc()).paginate(page=page, per_page=50)
        else:
            nob = Nobitex.query.filter_by(curr=form.search.data).order_by(Nobitex.date_created.desc()).paginate(page=page, per_page=50)
            wal = Wallex.query.filter_by(curr=form.search.data).order_by(Wallex.date_created.desc()).paginate(page=page, per_page=50)

        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template('records.html', image_file=image_file, nob=nob, wal=wal, form=form)


    elif request.method == 'GET':
        form = FilterRecordsForm() 
        print("var",form_data)
        if  form_data[0]['search'] or form_data[0]['fromdate'] or form_data[0]['todate']:
            
            if form_data[0]['fromdate'] != None and form_data[0]['todate'] != None:
                nob = Nobitex.query.filter_by(curr=form_data[0]['search']).filter(Nobitex.date_created >= form_data[0]['fromdate'] and Nobitex.date_created < form_data[0]['todate']).order_by(Nobitex.date_created.desc()).paginate(page=page, per_page=50)
                wal = Wallex.query.filter_by(curr=form_data[0]['search']).filter(Wallex.date_created >= form_data[0]['fromdate']).order_by(Wallex.date_created.desc()).paginate(page=page, per_page=50)
            else:
                nob = Nobitex.query.filter_by(curr=form_data[0]['search']).order_by(Nobitex.date_created.desc()).paginate(page=page, per_page=50)
                wal = Wallex.query.filter_by(curr=form_data[0]['search']).order_by(Wallex.date_created.desc()).paginate(page=page, per_page=50)
        else:
                       
            nob = Nobitex.query.order_by(Nobitex.date_created.desc()).paginate(page=page, per_page=50)
            wal = Wallex.query.order_by(Wallex.date_created.desc()).paginate(page=page, per_page=50)

        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template('records.html', image_file=image_file, nob=nob, wal=wal, form=form)
    print("out if")



