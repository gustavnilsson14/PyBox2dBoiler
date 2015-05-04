from math import atan2, sqrt, cos, sin
from framework import *

def get_radians_between_points( point1, point2 ) :
    delta = get_delta_between_points( point1, point2 )
    return atan2( delta[ 1 ], delta[ 0 ] )

def get_delta_between_points( point1, point2 ) :
    return (point2[0] - point1[0], point2[1] - point1[1])

def get_distance_between_points( point1, point2 ) :
    return sqrt( (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 )

def get_movement_vector( radians, speed ) :
    change = [speed * cos(radians), speed * sin(radians)]
    return change

def create_humanoid( owner, world, pos, size ) :
    body_offset = ( -0.4*size, 0 )
    size_definition = 0.3*size
    real_density = 5 * size
    head = world.CreateDynamicBody(
        position=pos,
        fixtures=[
            b2FixtureDef(
                shape=b2CircleShape(radius=size_definition),
                density=real_density
            )
        ],
        userData=owner
    )
    '''
    body_offset = ( -0.4*size, 0 )
    size_definition = (0.4*size, 0.1*size, (0.2*size, 0), 0)
    real_density = 0 * size
    right_arm = world.CreateDynamicBody(
        position=( pos[0]+body_offset[0], pos[1]+body_offset[0] ),
        fixtures=[
            b2FixtureDef(
                shape=b2PolygonShape( box=size_definition ),
                density=real_density
            )
        ],
        userData=owner
    )
    right_arm_joint_pos = (-0.4, 0)
    right_arm_joint=b2RevoluteJointDef(
        bodyA=head,
        bodyB=right_arm,
        localAnchorA=right_arm_joint_pos,
        localAnchorB=(0,0),
        enableMotor=True,
        motorSpeed=1000,
        enableLimit=True,
        maxMotorTorque=1000,
        #lowerAngle=-30.0 * b2_pi / 180.0,
        #upperAngle=5.0 * b2_pi / 180.0,
    )
    right_arm_joint=world.CreateJoint(right_arm_joint)
    '''
    return head
