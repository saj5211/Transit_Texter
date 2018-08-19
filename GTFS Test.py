from google.transit import gtfs_realtime_pb2
import requests



feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('http://nextride.brampton.ca:81/API/TripUpdates')
feed.ParseFromString(response.content)
for entity in feed.entity:
  if entity.HasField('trip_update'):
    print entity.trip_update