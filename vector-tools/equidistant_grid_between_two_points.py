"""
A tools for obtaining corner vertices of each plot polygon and create rectangular
polygon shapefile based on the points.

Usage: generating gridding shapefile for UAV/MAV processing and
    crop plot boundary for metric generation
"""

from math import *
import csv

def get_path_length_meter(lat1, lon1, lat2, lon2):
    """
    calculates the the Haversine distance between two lat, long coordinate pairs
    Please refer to this page for details
    http://www.movable-type.co.uk/scripts/latlong.html

    :Parameters:
      - pointA: The tuple representing the longitude/latitude for the
        first point. Latitude and longitude must be in decimal degrees
      - pointB: The tuple representing the longitude/latitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      distance between two points in meter
    :Returns Type:
      float

    """
    R = 6371000 # radius of earth in m
    delta_lat = radians((lat2-lat1))
    delta_lon = radians((lon2-lon1))

    a = (sin(delta_lat / 2) * sin(delta_lat / 2) +
         cos(radians(lat1)) * cos(radians(lat2)) *
         sin(delta_lon / 2) * sin(delta_lon / 2))

    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance

def get_destination_latlong(lat, lon, azimuth, distance):
    """
    :Parameters:
      - starting point: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
    :Returns:
      a list of points (lat/lon) in decimal degree
    :Returns Type:
      list

    returns the lat an long of destination point
    given the start lat, long, aziuth, and distance
    """

    R = 6378.1 #Radius of the Earth in km

    bearing = radians(azimuth) #Bearing is degrees converted to radians.
    d = float(distance/1000) #Distance m converted to km
    lat1 = radians(lat) #Current dd lat point converted to radians
    lon1 = radians(lon) #Current dd long point converted to radians

    lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1)* sin(d/R)* cos(bearing))
    lon2 = lon1 + atan2(sin(bearing) * sin(d/R)* cos(lat1),
                             cos(d/R)- sin(lat1)* sin(lat2))

    #convert back to degrees
    lat2 = degrees(lat2)
    lon2 = degrees(lon2)

    return[lat2, lon2]

def calculate_bearing(lat1, lon1, lat2, lon2):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    start_lat = radians(lat1)
    start_lon = radians(lon1)
    end_lat = radians(lat2)
    end_lon = radians(lon2)

    dLong = end_lon - start_lon
    dPhi = log(tan(end_lat/2.0+pi/4.0)/tan(start_lat/2.0+pi/4.0))

    if abs(dLong) > pi:
        if dLong > 0.0:
             dLong = -(2.0 * pi - dLong)
        else:
             dLong = (2.0 * pi + dLong)
    bearing = (degrees(atan2(dLong, dPhi)) + 360.0) % 360.0;
    return bearing

def main(interval, azimuth, lat1, lon1, lat2, lon2):
    """
    returns every coordinate pair inbetween two coordinate
    pairs given the desired interval
    """


    d = get_path_length_meter(lat1, lon1, lat2, lon2)
    remainder, dist = modf((d / interval))
    counter = float(interval)
    coords = []
    coords.append([lat1, lon1])
    for distance in range(0,int(dist)):
        coord = get_destination_latlong(lat1, lon1, azimuth, counter)
        counter = counter + float(interval)
        coords.append(coord)
    coords.append([lat2, lon2])
    return coords

if __name__ == "__main__":

    #point interval in meters
    interval = 5.334

    #start and end point
    point_s = (-90.3078692899072, 39.0617323189125)
    point_e = (-90.3103375785536, 39.0617472633370)

    lat1 = point_s[1]
    lon1 = point_s[0]

    lat2 = point_e[1]
    lon2 = point_e[0]

    #direction of line in degrees
    azimuth = calculate_bearing(lat1, lon1, lat2, lon2)
    print (azimuth)

    coords = main(interval, azimuth, lat1, lon1, lat2, lon2)

    csvfile = '/Users/hojin.kim/pc-share/test.csv'

    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(coords)

    print (coords)
