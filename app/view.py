from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from app import app, oauth, user_datastore, db
from flask_security import login_required, current_user, login_user

from config.config import Configuration
from app.color_print import cprint


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
    print("\n {} \n".format(resp))
    print("email: {}".format(resp['email']))
    print("name: {}".format(resp['name']))

    user = user_datastore.find_user(email=resp['email'])

    if not user:
        # print('not exist')
        if resp['verified_email']:
            user_datastore.create_user(lastname=resp['family_name'], name=resp['given_name'], email=resp['email'], active=False, picture_url=resp['picture'], roles=['user'])
            db.session.commit()
            message = 'Аккаунт создан. Для активации свяжитесь с администратором.'
            flash(message, 'success')
            return redirect(url_for('security.login'))
    else:
        # print('exist')
        if not user.active:
            print('user active: False')
            message = 'Свяжитесь с администратором ваш аккаунт не активирован'
            flash(message, 'warning')
            return redirect(url_for('security.login'))

    login_user(user)
    return redirect('/')


# NOTE: Домашняя страница
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    cprint("YELLOW", "User name: {} lastname: {}".format(current_user.name, current_user.lastname))

    return render_template("home.html", pgname="Home", company=Configuration.HTML_TITLE_COMPANY, User="{} {}".format(current_user.lastname, current_user.name))


# # NOTE: Страница с смс таблицей
# @app.route('/smstable', methods=['GET', 'POST'])
# @login_required
# def smstable():
#     smsdelivery = dbase().loadTableSMS()
#     if smsdelivery:
#         return render_template("smstable.html", pgname="SMS manager", company=html_title_company, smsdelivery=smsdelivery, User=session["User"], groups=session["groups"])
#     else:
#         return render_template("smstable.html", pgname="SMS manager", company=html_title_company, User=session["User"], groups=session["groups"])
#
#
# # NOTE: Обновление таблицы смс оповещений
# @app.route('/updatesmsdelivery', methods=['POST'])
# @login_required
# def updatesmsdelivery():
#     pk = request.form['pk']
#     name = request.form['name']
#     value = request.form['value']
#     res = dbase().updateSmsTable(name, pk, value)
#     if res == 0:
#         # flash("Такой login уже существует", "error")
#         message = "mysql error"
#     else:
#         # flash("Пользователь добавлен", "success")
#         message = "mysql успешно"
#
#     # return json.dumps({'status': 'OK'})
#     return jsonify({'message': message})
#
#
# @app.route('/syncdatafromjira')
# def syncdatafromjira():
#     output = subprocess.getoutput("{}/scripts/get_customers.sh".format(WORK_DIR))
#     cprint("PURPLE", "Sync output: {}".format(output))
#     return jsonify({'message': "success"})
