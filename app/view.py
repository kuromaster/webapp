from flask import render_template
from app import app
from flask_security import login_required, current_user

from config.config import Configuration
from app.color_print import cprint


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
