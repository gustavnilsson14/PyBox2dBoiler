from framework import *
from Util import *
from Core import *

class Unit :
    
    def __init__( self, scene, pos ) :
        self.body = scene.world.CreateDynamicBody(
            position=pos,
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=0.4),
                density=0.5,
            )
        )
        self.scene = scene
        self.current_path = 0
        self.current_order = 0
        self.speed = 10
        
    def set_order( self, order ) :
        if self.current_order == 0 :
            self.current_order = order
            return True
        if self.current_order.remove_unit( self ) == True :
            self.current_order = order
            return True
        return False
        
    def update( self, update ) :
        if self.current_order != 0 :
            if self.current_order.Step() == False :
                return False
        
    def move( self, new_pos ) :
        if self.body == 0 :
            self.pos = new_pos
            return True
        
        if self.current_path != 0 :
            next_tile = self.current_path[ 0 ]
            next_tile_distance = get_distance_between_points( self.body.transform.position, next_tile )
            if next_tile_distance > 0.3 :
                #MOVE ME
                #get_new_position( self.body.transform.position, next_tile )
                radians_to_tile = get_radians_between_points( self.body.transform.position, next_tile )
                movement_vector = get_movement_vector( radians_to_tile, self.speed )
                self.body.linearVelocity = movement_vector
                #new_position = ( self.body.transform.position[0] + movement_vector[0], self.body.transform.position[1] + movement_vector[1] )
                #self.body.transform = [ new_position, 0 ]
                
                return True
            self.current_path.pop( 0 )
            if len( self.current_path ) == 0 :
                self.current_path = 0
                self.body.linearVelocity = ( 0, 0 )
                return False
            #self.set_rotation( get_angle_between_points( self.body.transform.position, self.current_path[ self.current_tile ] ) )
            return True
        self.current_path = self.scene.map.find_path( self.body.transform.position, new_pos )
        #self.body.
        
    def set_rotation( self, angle ) :
        self.body.transform = [ self.body.transform.position, angle ]
        
