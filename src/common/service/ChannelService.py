import Main
from common.model.Models import db, Users, Channel, ChannelUserCar
from flask import redirect, request, render_template, session
from sqlalchemy import text

class ChannelService:
    def __init__(self):
        self.Mainapp = Main.MainApp
        #self.exec_channel_non_occupied = text('SELECT * FROM channels WHERE occupancy = false ORDER BY id_station ASC')
    def order_station(self):
        exec_usercars_filtered = text('SELECT * FROM user_cars WHERE id_user = :user_id')
        if session['username'] == '':
            return redirect('/index')
        else:
            channel_list = Channel.query.filter_by(occupancy=False).order_by(Channel.id_station.asc()).all()
            car_list = db.session.execute(exec_usercars_filtered, {'user_id': session['user_id']})
            if request.method == 'POST':
                match request.form['button']:
                    case 'Order a station':
                        #channel_list.close()
                        car_list.close()
                        markers = request.form.getlist("table")
                        getcar = request.form['Car_selection']
                        for i in markers:
                            channel = Channel.query.filter_by(id=i).first()
                            channel_usercars = ChannelUserCar.query.filter_by(id_channel=i, id_user=session['user_id']).first()
                            if channel.occupiedby is None:
                                if (channel_usercars is None or channel_usercars.id_channel is None or
                                        channel_usercars.id_user_car is None):
                                    add_to_channel_user_car = ChannelUserCar (id_channel = i,
                                                                            id_user = session['user_id'],
                                                                            id_user_car = getcar)
                                    db.session.add(add_to_channel_user_car)
                                else:
                                    channel_usercars.id_user_car = int(getcar)
                                channel.occupancy = True
                                channel.occupiedby = session['username']
                                db.session.commit()

                            elif channel.occupiedby != session['username']:
                                return 'this channel was occupied by someone else! Choose other channel!'

                        return redirect('/user/order_station')
                    case 'Release a station':
                        channel_list.close()
                        car_list.close()
                        markers = request.form.getlist("table")
                        for i in markers:
                            channel = Channel.query.filter_by(id=i).first()
                            if channel.occupiedby == session['username']:
                                ChannelUserCar.query.filter_by(id_channel=i, id_user=session['user_id']).delete()
                                channel.occupancy = False
                                channel.occupiedby = None
                                db.session.commit()
                            else:
                                return "You can't release station, which you didn't occupied!"

                        return redirect('/user/order_station')
                    case 'show occupied channels by you':
                        filter_occupied_ch = text("SELECT * FROM channels WHERE occupiedby = :username")
                        filter_occupied_channels_by_user = db.session.execute(filter_occupied_ch, {'username': session['username']})
                        return render_template('user_order_stations_show_occupied_stations.html',
                                               channel=channel_list,
                                               channel_filtered=filter_occupied_channels_by_user,
                                               username=session['username'],
                                               car_list=car_list)
                    case _:
                        return str(request.form['button'])
            else:
                return render_template('user_order_station.html', channel=channel_list,
                                       username=session['username'], car_list=car_list)

    def channel_managment(self):
        if session['username'] == '' or session['role'] != 'admin':
            return redirect('/index')
        else:
            channel_list = Channel.query.order_by(Channel.id_station.asc()).all()
            if request.method == 'POST':
                match request.form['button']:
                    case 'remove selected rows':
                        markers = request.form.getlist("table")
                        for i in markers:
                            Channel.query.filter_by(id=i).delete()
                        db.session.commit()
                        return redirect('/admin/channel_managment')
                    case 'submit changes':
                        channel_parrent_station = request.form['channel_parrent_station']
                        channel_title = request.form['channel_title']
                        channel_price = request.form['channel_price']
                        if channel_parrent_station == '' or channel_title == '' or channel_price == '':
                            return redirect('/admin/channel_managment')
                        else:
                            add_station = Channel(id_station = channel_parrent_station,
                                            title = channel_title,
                                            price = channel_price)
                            db.session.add(add_station)
                            db.session.commit()
                            return redirect('/admin/channel_managment')
                    case 'Release a station':
                        markers = request.form.getlist("table")
                        for i in markers:
                            channel = Channel.query.filter_by(id=i).first()
                            channel.occupancy = False
                            channel.occupiedby = None
                            db.session.commit()
                        return redirect('/admin/channel_managment')
                    case _:
                        return str(request.form['button'])
            else:
                return render_template('admin_channel_managment.html', channels=channel_list
                                       , username=session['username']) #channel_station_name=channel_station_name)


