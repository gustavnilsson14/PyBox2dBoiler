from math import atan2, sqrt, cos, sin
from Constants import *
from framework import *

def get_radians_between_points( point1, point2 ) :
    delta = get_delta_between_points( point1, point2 )
    return atan2( delta[ 1 ], delta[ 0 ] )

def get_delta_between_points( point1, point2 ) :
    return (point2[0] - point1[0], point2[1] - point1[1])

def get_distance_between_points( point1, point2 ) :
    return sqrt( (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 )

def get_movement_vector( radians, speed ) :
    change = b2Vec2(speed * cos(radians), speed * sin(radians))
    return change
