import datetime
import time

from flask import Flask, render_template, send_file, send_from_directory, redirect, url_for, session, request, flash
from pymongo import MongoClient
import os
from dateutil.rrule import rrule, DAILY, MONTHLY
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message, Mail
import random

machine_number = 0
OTP_dict = {}

app = Flask(__name__)

app.config['SECRET_KEY'] = 'STARDOM'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'stonedgetechmachines@gmail.com'
sender = 'stonedgetechmachines@gmail.com'
app.config['MAIL_PASSWORD'] = 'StonEdge$123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)

# DataBase
cluster = MongoClient(
    "mongodb+srv://king:kingqueen@cluster0.opj1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster['test']
fillings = db['Fillings']
payments = db['Payments']
users = db['Users']
machines = db['Machines']



class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    u = users.find_one({'_id': user_id})

    user =User()
    user.id = user_id
    user.machine = u['Machines']

    return user



# ===============================================================================================================================
#                                                   FUNCTIONS
# ===============================================================================================================================
def sales_data(m_no, mode, s_date, e_date):

    sel_machine = current_user.machine[int(m_no)]
    query1 = eval('''mode.find(
        {'$and':[
            {'Machine_id': sel_machine},
            {'Date': {'$gte': s_date}},
            {'Date': {'$lte': e_date}}
        ]}
    )''')
    return query1



def line_graph(m_no, mode, s_date, e_date, type):
    a = {DAILY: '%d-%m-%y', MONTHLY: '%b %y'}

    sel_machine = current_user.machine[int(m_no)]
    query1 = eval('''mode.find(
        {'$and':[
            {'Machine_id': sel_machine},
            {'Date': {'$gte': s_date}},
            {'Date': {'$lte': e_date}}
        ]}
    )''')

    dates = [dt.strftime(a[type]) for dt in rrule(type, dtstart=s_date, until=e_date)]

    revenue_One = [0] * len(dates)
    revenue_Two = [0] * len(dates)
    sale_One = [0] * len(dates)
    sale_Two = [0] * len(dates)

    for i in query1:
        if i['Date'].strftime(a[type]) in dates:
            index = dates.index(i['Date'].strftime(a[type]))
            if mode == payments:
                for indx, j in enumerate(i['Purchase']):
                    exec('sale_{0}[index] = sale_{0}[index] + {1}'.format(j, i['Purchase'][j]))
                    exec('revenue_{0}[index] = revenue_{0}[index] + {1}'.format(j, int(i['Amount_breakout'].split(';')[indx])))

            if mode == fillings:
                for j in i['Filling']:
                    exec('sale_{0}[index] = sale_{0}[index] + {1}'.format(j.split(':')[0], int(j.split(':')[1])))

    return dates, revenue_One, revenue_Two, sale_One, sale_Two


def machine(m_no):
    query = machines.find(
        {'_id': current_user.machine[int(m_no)]}
    )
    return query


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/<m_no>/dashboard')
@login_required
def dashboard(m_no):
    if not current_user.machine:
        return render_template('blank.html')
    print(OTP_dict)
    now_month = datetime.datetime.now().strftime('%m%Y')
    a = sales_data(m_no, payments,  datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'))
    b, c, d, e, f = line_graph(m_no, payments, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'), DAILY)
    g = machine(m_no)


    return render_template('dashboard.html', table=a, labels=b, graph1=c, graph_t1=[c[i]+d[i] for i in range(len(b))], graph2=d, bar=g, box1=sum(c) + sum(d), box2=sum(e) + sum(f), box3='dummy', m_no=m_no)


@app.route('/<m_no>/table')
@login_required
def table(m_no):
    if not current_user.machine:
        return render_template('blank.html')

    now_month = datetime.datetime.now().strftime('%m%Y')
    now_year = datetime.datetime.now().strftime('%Y')
    a = sales_data(m_no, payments, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'))
    b = sales_data(m_no, fillings, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'))
    c = sales_data(m_no, fillings, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'))
    d1, e1, f1, g1, h1 = line_graph(m_no, payments, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'), DAILY)
    d2, e2, f2, g2, h2 = line_graph(m_no, payments, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'), MONTHLY)

    return render_template('table.html', table_a=a, table_b=b, table_c=c, table1a=d1, table1b=e1, table1c=f1, len1=len(d1), table1d=g1, table1e=h1,
                           table2a=d2, table2b=e2, table2c=f2, len2=len(d2), table2d=g2, table2e=h2, m_no=m_no)


@app.route('/<m_no>/chart')
@login_required
def chart(m_no):
    if not current_user.machine:
        return render_template('blank.html')

    now_month = datetime.datetime.now().strftime('%m%Y')
    now_year = datetime.datetime.now().strftime('%Y')
    b, c, d, e, f = line_graph(m_no, payments, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'), DAILY)
    bb, cc, dd, ee, ff = line_graph(m_no, payments, datetime.datetime.strptime('11'+now_year, '%d%m%Y'),  datetime.datetime.strptime('3112'+now_year, '%d%m%Y'), MONTHLY)
    b1, _, _, e1, f1 = line_graph(m_no, fillings, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'), DAILY)
    bb1, _, _, ee1, ff1 = line_graph(m_no, fillings, datetime.datetime.strptime('11'+now_year, '%d%m%Y'),  datetime.datetime.strptime('3112'+now_year, '%d%m%Y'), MONTHLY)

    g = machine(machine_number)

    print(bb)

    return render_template('chart.html', bar=g, labels1=b, graph1a=c, graph1b=d, graph_t1=[c[i]+d[i] for i in range(len(c))],
                           graph2a=e, graph2b=f, graph_t2=[e[i]+f[i] for i in range(len(e))],
                           labels2=bb, graph3a=cc, graph3b=dd, graph_t3=[cc[i] + dd[i] for i in range(len(cc))],
                           graph4a=ee, graph4b=ff, graph_t4=[ee[i] + ff[i] for i in range(len(ee))],
                           labels3=b1, graph6a=e1, graph6b=f1, graph_t6=[e1[i] + f1[i] for i in range(len(e1))],
                           labels4=bb1, graph8a=ee1, graph8b=ff1, graph_t8=[ee1[i] + ff1[i] for i in range(len(ee1))], m_no=m_no
                           )


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile(m_no):
    if request.method == 'POST':
        if request.form['submit'] == 'machine_add':
            machine_id = request.form['machine_id']
            machine_pass = request.form['machine_password']

            if machine_id not in current_user.machine:
                query = machines.find_one({'_id': machine_id})
                if query:
                    if query['Machine Code'] == machine_pass:
                        users.update_one(
                            {'_id': current_user.id},
                            {'$push': {
                                'Machines': machine_id
                            }}
                        )
                        return redirect(url_for('dashboard'))
                    else:
                        flash("Wrong Password", 'info')
                else:
                    flash('No Machine found with this ID', 'warning')
            else:
                flash('Machine Already added', 'info')
    return render_template('profile.html', m_no=m_no)


@app.route('/<m_no>/update', methods=['POST', 'GET'])
def update(m_no):
    q = machines.find_one({'_id': current_user.machine[int(m_no)]})
    items = q['Items']
    prices = q['Price']

    if request.method == 'POST':
        i, p = {}, {}
        for j in items:
            exec("itm_j = request.form.get('{}')".format('i_'+str(j)))
            exec("i[j] = itm_j")
        print(i)
        for j in prices:
            exec("itm_k = request.form.get('{}')".format('p_' + str(j)))
            exec("p[j] = itm_k")
        print(p)

        machines.update_one(
            {'_id': current_user.machine[int(m_no)]},
            {'$set': {'Items': i, 'Price': p},
             '$currentDate': {'lastModified': True}}
        )

        return redirect(url_for('dashboard', m_no=m_no))
    return render_template('update.html', m_no=m_no, items=items, prices=prices)





@app.route('/download')
def download():
    files = os.listdir('.')
    if 'a.csv' in files:
        return send_file('a.csv', as_attachment=True)

    return 'dashboard'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        usr = users.find_one(
            {'_id': username}
        )

        if usr:
            print(check_password_hash(request.form.get('password'), usr['Password']))
            if check_password_hash(usr['Password'], request.form.get('password')):
                if usr['Verified']:
                    user = User()
                    user.id = username
                    login_user(user)
                    return redirect(request.args.get('next') or url_for('dashboard', m_no=machine_number))
                else:
                    flash('Please verify your email to continue', 'info')
                    time.sleep(2)
                    return redirect(url_for('otp_generator', uid=usr['_id']))
            else:
                flash('Wrong Password', 'warning')
        else:
            flash('No user Found with this username', 'info')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        userid = request.form.get('userid')
        name = request.form.get('name')
        e_mail = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        address = request.form.get('address')
        city = request.form.get('city')

        usr = users.find_one({'_id': userid})

        if usr:
            flash('Username already taken', 'warning')
        else:
            user_data = {
                '_id': userid,
                'Name': name,
                'Phone Number': phone,
                'Email': e_mail,
                'Address': address,
                'City': city,
                'Password': generate_password_hash(password, 'sha256'),
                'Verified': False,
                'Machines': []
            }
            users.insert_one(user_data)

            return redirect(url_for('otp_generator', uid=userid))
    return render_template('signup.html')


@app.route('/otpgenerator/<uid>')
def otp_generator(uid):
    OTP = random.randint(000000, 999999)
    u_mail = users.find_one({'_id': uid})
    print(u_mail['Email'])
    msg = Message('OTP', sender=sender, recipients=[u_mail['Email']])
    msg.body = str(OTP)
    mail.send(msg)
    OTP_dict[uid] = OTP

    return redirect(url_for('verify', uid=uid))


@app.route('/verify/<uid>', methods=['POST', 'GET'])
def verify(uid):
    if request.method == 'POST':
        OTP = request.form.get('otp')
        print(OTP_dict[uid], OTP)
        if str(OTP_dict[uid]) == OTP:
            flash('E mail verified', 'success')
            time.sleep(2)
            u = users.update(
                {'_id': uid},
                {'$set': {'Verified': True}}
            )
            return redirect(url_for('login'))
        else:
            flash('Wrong OTP', 'danger')

    return render_template('verify.html', eml=uid)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_page'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4000)


