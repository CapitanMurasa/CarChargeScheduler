from flask import render_template, Flask, request, redirect
import os
from common.model.Models import Users, Station, Channel, UserCar, ChannelUserCar, db
from sqlalchemy.sql import text
import common.service.CrudHelper as CrudHelper
# custom service modules
from common.service import UserService, ChannelService, UserCarService, StationService

# changelog




# todo
# use flask's session function to store current user variable instead of loading it to global server variable
# .env file

# bootstrap


class MainApp:
    app = Flask(__name__)
    db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not db_uri:
        raise RuntimeError("SQLALCHEMY_DATABASE_URI is not set!")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    db.init_app(app)

    @app.route('/login', methods = ['POST', 'GET'])
    def login():
        userservice = UserService.UserService()
        return userservice.login()

    @app.route('/logout')
    def logout():
        userservice = UserService.UserService()
        return userservice.logout()

    @app.route('/admin/index', methods = ['POST', 'GET'])
    def admin_index():
        userservice = UserService.UserService()
        return userservice.admin_index()

    @app.route('/user/order_station', methods=['POST', 'GET'])
    def order_station():
        channelservice = ChannelService.ChannelService()
        return channelservice.order_station()


    @app.route('/user/add_car', methods=['POST', 'GET'])
    def add_car():
        usercarservice = UserCarService.UserCarService()
        return usercarservice.add_car()


    @app.route('/admin/station_managment', methods=['POST', 'GET'])
    def station_managment():
        stationservice = StationService.StationService()
        return stationservice.station_managment()

    @app.route('/admin/channel_managment', methods=['POST', 'GET'])
    def channel_managment():
        channelservice = ChannelService.ChannelService()
        return channelservice.channel_managment()
    @app.route('/admin/report_page', methods = ['POST', 'GET'])
    def report_page():
        userservice = UserService.UserService()
        return userservice.report_page()

    @app.route('/admin/reported_users', methods = ['POST', 'GET'])
    def reported_users():
        userservice = UserService.UserService()
        return userservice.reported_users()
    @app.route('/index', methods=['POST', 'GET'])
    def index():
        userservice = UserService.UserService()
        return userservice.index()


# @app.route('/test')
# def test():
#     return f'username is {Username}\n username id is {Username_id}\n username role is {Username_role}'
#     #return CrudHelper.channel_usercars(Username_id).sync_user()

mainapp = MainApp
app = MainApp.app

if __name__ == '__main__':
    app.run(debug=True)