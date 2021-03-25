from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import flash, session, jsonify
from datetime import datetime as dt
from app import app, oauth, user_datastore, db, User, Customer, myspreadsheet
from flask_security import login_required, current_user, login_user
import subprocess
import json

from config.config import Configuration
from app.color_print import cprint


def update_field_on_logon(request, user):
    if user.email:

        data = {}
        data.clear()

        if user.current_login_ip:
            user_last_login_ip = user.current_login_ip
            cprint("PURPLE", "[update_field_on_logon] user_last_login_ip:" + user_last_login_ip)
            data.update({'last_login_ip': user_last_login_ip})

        if user.current_login_at:
            user_last_login_at = user.current_login_at
            cprint("PURPLE", "[update_field_on_logon] user_last_login_at:" + str(user_last_login_at))
            data.update({'last_login_at': user_last_login_at})

        if request.environ.get('HTTP_X_REAL_IP', request.remote_addr):
            user_cur_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            cprint("PURPLE", "[update_field_on_logon] user_cur_ip:" + user_cur_ip)
            data.update({'current_login_ip': user_cur_ip})

        user_cur_login_at = dt.now()
        cprint("PURPLE", "[update_field_on_logon] user_cur_login_at:" + str(user_cur_login_at))
        data.update({'current_login_at': user_cur_login_at})

        if user.login_count is not None:
            user_login_count = user.login_count + 1
            cprint("PURPLE", "[update_field_on_logon] user_login_count:" + str(user_login_count))
            data.update({'login_count': user_login_count})
        else:
            data.update({'login_count': 1})

        session["User"] = "{} {}".format(user.lastname, user.name)
        res = User.query.filter(User.email == user.email).update(data)
        cprint("RED", "[update_field_on_logon] res: " + str(res))
        db.session.commit()


@app.before_request
def update_cur_login_at():
    if not current_user.is_anonymous:
        data = {}
        data.clear()
        last_activity = dt.now()
        # cprint("PURPLE", "user_cur_login_at:" + str(user_cur_login_at))
        data.update({'last_activity': last_activity})
        User.query.filter(User.email == current_user.email).update(data)
        # cprint("RED", "res: " + str(res))
        db.session.commit()

        # if not session.get("User"):
        session["User"] = "{} {}".format(current_user.lastname, current_user.name)

    # cprint("CYAN", "[update_cur_login_at] SESSION: {}".format(dict(session)))


'''
    Google Authentication
'''


# NOTE: Google auth. Перенаправление в гугл
@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_auth', _external=True)
    return google.authorize_redirect(redirect_uri)


# NOTE: Получение данных от гугла. Проверка. Авторизация
@app.route('/login/google/auth')
def google_auth():
    google = oauth.create_client('google')
    google.authorize_access_token()
    # user = google.parse_id_token(token)
    resp = google.get('userinfo').json()
    # print("\n {} \n".format(resp))
    # print("email: {}".format(resp['email']))
    # print("name: {}".format(resp['name']))
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    cprint("CYAN", "[google_auth] user ip: {}".format(user_ip))

    user = user_datastore.find_user(email=resp['email'])

    if not user:
        # print('not exist')
        if resp['verified_email']:
            user_datastore.create_user(lastname=resp['family_name'], name=resp['given_name'], email=resp['email'], active=False, picture_url=resp['picture'], login_count=0, roles=['user'])
            db.session.commit()
            message = 'Аккаунт создан. Для активации свяжитесь с администратором.'
            flash(message, 'success')
            return redirect(url_for('security.login'))
            update_field_on_logon(request, user)
    else:
        # print('exist')
        if not user.active:
            cprint('RED', '[google_auth] user active: False')
            update_field_on_logon(request, user)
            message = 'Свяжитесь с администратором ваш аккаунт не активирован'
            flash(message, 'warning')
            return redirect(url_for('security.login'))

    update_field_on_logon(request, user)
    login_user(user, True)
    return redirect('/')


'''
    ДОМАШНЯЯ СТРАНИЦА
'''


# NOTE: Домашняя страница
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    cprint("YELLOW", "User name: {} lastname: {}".format(current_user.name, current_user.lastname))

    return render_template("home.html", pgname="Home", company=Configuration.HTML_TITLE_COMPANY, User=session["User"])


'''
    Вьюхи СМС таблицы
'''


# NOTE: Страница с смс таблицей
@app.route('/smstable', methods=['GET', 'POST'])
@login_required
def smstable():
    smsdelivery = Customer.query.all()
    if smsdelivery:
        return render_template("smstable.html", pgname="SMStable", company=app.config['HTML_TITLE_COMPANY'], smsdelivery=smsdelivery, User=session["User"])
    else:
        return render_template("smstable.html", pgname="SMStable", company=app.config['HTML_TITLE_COMPANY'], User=session["User"])


# NOTE: Обновление таблицы смс оповещений
@app.route('/updatesmsdelivery', methods=['POST'])
@login_required
def updatesmsdelivery():
    data = {}
    data.clear()
    data.update({request.form['name']: request.form['value']})

    res = Customer.query.filter(Customer.email == request.form['pk']).update(data)
    db.session.commit()
    if res == 0:
        # flash("Такой login уже существует", "error")
        message = "mysql error"
    else:
        # flash("Пользователь добавлен", "success")
        message = "mysql успешно"

    # return json.dumps({'status': 'OK'})
    return jsonify({'message': message})


# NOTE: Обновление таблицы Customer. Загрузка данных из джиры
@app.route('/syncdatafromjira')
def syncdatafromjira():
    output = subprocess.getoutput("{}/scripts/get_customers.sh".format(app.config['WORK_DIR']))
    cprint("PURPLE", "Sync output: {}".format(output))
    return jsonify({'message': "success"})


'''
    Google spreadsheet
'''


# NOTE: Страница гугл таблицы
@app.route('/gspreadsheet', methods=['GET'])
def gspreadsheet():
    # table = myspreadsheet.get_sheet_values()
    table = None
    debug = myspreadsheet.get_sheet_values_hard()


    # return render_template("gspread.html", pgname="Gspread", company=html_title_company)
    # return jsonify(rows)
    return render_template("gspreadsheet.html", pgname="gSpreadSheet", company=app.config['HTML_TITLE_COMPANY'], table=table, User=session["User"], debug=debug)


# NOTE: Страница гугл таблицы в json формате
@app.route('/googlesheets', methods=['GET'])
def gspreadsheet_debug():
    # table = myspreadsheet.get_sheet_values()
    data = myspreadsheet.get_sheet_colors()

    # return render_template("gspread.html", pgname="Gspread", company=html_title_company)
    return jsonify(data)
    # return render_template("gspreadsheet.html", pgname="gSpreadSheet", company=app.config['HTML_TITLE_COMPANY'], table=table, User=session["User"])
