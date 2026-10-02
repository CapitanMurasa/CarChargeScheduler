from common.model.Models import Users, Station, Channel
from datetime import datetime

def username_to_id(value):
    user = Users.query.filter_by(username=value).first()
    return user.id if user else None

def id_to_username(value):
    user = Users.query.get(value)
    return user.username if user else None

def stationname_to_id(value):
    station = Station.query.filter_by(title=value).first()
    return station.id if station else None

def channelname_to_id(value):
    channel = Channel.query.filter_by(title=value).first()
    return channel.id if channel else None

def str_to_datetime(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None
  
