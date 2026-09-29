import Main
import common.service.CrudHelper as Crudhelper
from common.model.Models import db, Users, Station , Channel , ChannelUserCar ,ReportedUsersList
from flask import redirect, request, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text


class UserService:
    def __init__(self):
        self.Mainapp = Main.MainApp

    def index(self):
        if request.method == 'POST':
                match request.form['index_buttons']:
                    case 'log in':
                        return redirect('/login')
                    case 'log out':
                        return redirect('/logout')
                    case 'Order a station':
                        return redirect('/user/order_station')
                    case 'car managment':
                        return redirect('/user/add_car')
                    case 'switch back to admin page':
                        return redirect('/admin/index')
                    case _:
                        pass
        else:
            return render_template('user_index.html', username=session.get('username', ''),
                                    Username_role=session.get('role', ''))


    def admin_index(self):
        if request.method == 'POST':
                match request.form['index_buttons']:
                    case 'log in':
                        return redirect('/login')
                    case 'log out':
                        return redirect('/logout')
                    case 'switch to user account':
                        return redirect('/index')
                    case 'station managment':
                        return redirect('/admin/station_managment')
                    case 'channel managment':
                        return redirect('/admin/channel_managment')
                    case 'report':
                        return redirect('/admin/report_page')
                    case 'reported users':
                        return redirect('/admin/reported_users')
                    case _:
                        pass
        else:
            return render_template('admin_index.html', username=session.get('username', ''),
                                   user_role=session.get('role'))

    def logout(self):
        session.clear()
        return redirect('/index')

    def login(self):
        if request.method == 'POST':
            Username = request.form['Username']
            Password = request.form['Password']
            find_users = Users.query.filter_by(username=Username).first()
            if find_users is not None:
                self.Mainapp.Username_role = find_users.role
            match request.form['button']:
                case 'login':
                    try:
                        if check_password_hash(find_users.password, Password):
                            session['user_id'] = find_users.id
                            session['username'] = find_users.username
                            session['role'] = find_users.role
                            if find_users.role == 'user':
                                return redirect('/index')
                            elif find_users.role == 'admin':
                                return redirect('/admin/index')

                        else:
                            return 'wrong password...'





                    except AttributeError:
                        return 'wrong login...'
                    except Exception as e:
                        return str(e)
                case 'register':
                    users = Users.query.filter_by(username=Username).first()
                    if users:
                        return f'username {Username} exists!'
                    if Username  == '' and Password == '':
                        return redirect('/login')
                    else:
                        password_hash = generate_password_hash(Password)
                        add_user = Users(username=Username,
                                             password=password_hash,
                                             role='user')
                        db.session.add(add_user)
                        db.session.commit()
                        return redirect('/login')

        else:
            return render_template('admin_login.html')


    def report_page(self):
        if session.get('username') is None or session.get('role') != 'admin':
            return redirect('/index')
        else:
            Station_list_id = Station.query.with_entities(Station.id).all()
            Station_list_address = Station.query.with_entities(Station.addressname).all()
            channel_list = Channel.query.all()
            user_list = Users.query.all()
            if request.method == 'POST':
                if request.form['button'] == 'report':
                    station_name = request.form['station_name_select']
                    station_location = request.form['station_location_select']
                    channel_id = Crudhelper.channelname_to_id(request.form['channel_title_select'])
                    user_id = Crudhelper.username_to_id(request.form['User_select'])
                    additional_tip = request.form['textfeild']

                    report = ReportedUsersList(
                        id_station = station_name,
                        station_address = station_location,
                        id_channel = channel_id,
                        id_user = user_id,
                        additional_tip = additional_tip
                    )

                    db.session.add(report)
                    db.session.commit()
                    return redirect('/admin/report_page')

            return render_template('admin_report_page.html',
                                    stations_id = Station_list_id,
                                    stations_address = Station_list_address,
                                    channel_list = channel_list,
                                    user_list = user_list)
    def reported_users(self):
        if session['username'] == '' or session['role'] != 'admin':
            return redirect('/index')
        else:
            reportedUserslist = ReportedUsersList.query.all()
            if request.method == 'POST':
                if request.form['button'] == 'remove':
                    markers = request.form.getlist("table")
                    for i in markers:
                        ReportedUsersList.query.filter_by(id=i).delete()
                        db.session.commit()
                    return redirect('/admin/reported_users')

            return render_template('admin_reported_users_page.html', reported_users_list = reportedUserslist)