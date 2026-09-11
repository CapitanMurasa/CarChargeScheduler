from common.model.Models import Users, Station

def username_to_id(value):
    user = Users.query.filter_by(username=value).first()
    return user.id if user else None

def id_to_username(value):
    user = Users.query.get(value)
    return user.username if user else None

def stationname_to_id(value):
    station = Station.query.filter_by(title=value).first()
    return station.id if station else None


            

    
#class sort_channel:
#    def __init__(self):
#        pass


