from Util import *
import time

class Unit() :
    
    def __init__( self, scene, pos ) :
        '''
        self.body = scene.world.CreateDynamicBody(
            position=pos,
            fixedRotation=True,
            fixtures=[b2FixtureDef(
                shape=b2CircleShape(radius=0.3),
                density=0.5
            ),
            b2FixtureDef(
                shape=b2PolygonShape(vertices=[(-0.1, 0), (0.1, 0), (0, 1.5)]),
                density=0,
                isSensor=True
            )]
        )
        '''
        self.scene = scene
        self.body = create_humanoid( self, self.scene.world, pos, 0.5 )
        self.body.userData = self
        self.current_path = []
        self.current_tile = ()
        self.current_order = 0
        self.speed = 5
        
        
    def handle_collision( self, my_fixture, colliding_fixture ) :
        self.scene.world.DestroyBody( colliding_fixture.body )
        
    def set_order( self, order ) :
        if self.current_order == 0 :
            self.current_order = order
            return True
        if self.current_order.remove_unit( self ) == True :
            self.current_order = order
            return True
        return False
        
        
    def update( self, update ) :
        if self.scene.map.fov.is_pos_visible( self.body.transform.position, (5+13,5+4),5 ) :
            print "I C U"
        if self.current_order != 0 :
            if self.current_order.Step() == False :
                return False
        
    def move( self, new_pos ) :
        if self.body == 0 :
            self.pos = new_pos
            return True
        
        #self.move_along_path( new_pos )
        self.move_towards_target( self.scene.target_unit, 1 )
        
    def move_towards_target( self, target, final_distance ) :
        my_pos = self.body.transform.position
        target_pos = target.body.transform.position
        if get_distance_between_points( my_pos, target_pos ) > final_distance :
            radians_to_target = get_radians_between_points( my_pos, target_pos )
            movement_vector = get_movement_vector( radians_to_target, self.speed )
            self.body.linearVelocity = movement_vector
            return False
        self.body.linearVelocity = (0,0)
        return True
        
    def move_along_path( self, new_pos ) :
        if len( self.current_path ) != 0 :
            next_tile = self.current_path[ 0 ]
            next_tile_distance = get_distance_between_points( self.body.transform.position, next_tile )
            if next_tile_distance > ( 0.07 * self.speed ) :
                #MOVE ME
                radians_to_tile = get_radians_between_points( self.body.transform.position, next_tile )
                movement_vector = get_movement_vector( radians_to_tile, self.speed )
                self.body.linearVelocity = movement_vector
                
                return True
            self.current_tile = self.current_path.pop( 0 )
            self.scene.map.get_visible_tiles( self.body.transform.position )
            if len( self.current_path ) == 0 :
                self.current_path = []
                self.body.linearVelocity = ( 0, 0 )
                return False
            return True
        self.current_path = self.scene.map.find_path( self.body.transform.position, new_pos )
        
    def set_rotation( self, angle ) :
        self.body.transform = [ self.body.transform.position, angle ]
        
