from Map import *
from Unit import *
from Order import *
from Core import *
from random import randint

class Scene() :
    
    def __init__( self, game, world, scene_data ) :
        self.unit_list = []
        self.orders = []
        self.game = game
        self.world = world
        self.map = Map( world, scene_data.get( 'grid' ) )
        self.update_list = []
        
        
        unit = Unit( self, ( 0,0 ) )
        self.add_update( Update( unit.update ) )
        self.unit_list.append( unit )
        
        
        self.screen_shake_offset = (0,0)
        self.screen_shake_magnitude = 20
        self.add_update( Update( self.screen_shake, 150, 10, 2 ) )
        
        self.orders.append( MoveOrder( [ unit ], ( 23,25 ) ) )
        
        #unit.move( (23,20) )
    
    
    def add_update( self, update ) :
        if update == None :
            return False
        if self.update_list.__contains__( update ) :
            return False
        self.update_list.append( update )
        return True
        
    def remove_update( self, update ) :
        if self.update_list.__contains__( update ) :
            self.update_list.remove( update )
            return True
        return False
    
    def Step( self ) :
        for update in self.update_list :
            update.run()
        self.update_camera_center()
        
    def update_camera_center( self ) :
        self.game.setCenter( self.unit_list[0].body.transform.position )
        self.game._viewOffset[ 0 ] += self.screen_shake_offset[0]
        self.game._viewOffset[ 1 ] += self.screen_shake_offset[1]
        
    def screen_shake( self, update ) :
        if update.burst == 0 :
            self.screen_shake_offset = (0,0)
            return
        self.screen_shake_offset = ( randint(-self.screen_shake_magnitude,self.screen_shake_magnitude), randint(-self.screen_shake_magnitude,self.screen_shake_magnitude) )
    
    def destroy( self ) :
        self.world.ClearForces()
        while len( self.world.bodies ) != 0 :
            self.world.destroyBody( self.world.bodies[0] )

class Update :
    
    def __init__( self, function, interval = 1, burst = 1, burst_interval = 1, looping = True ) :
        #This game_objects update function runs when interval is at 0, must be a GameObject
        self.function = function
        
        #The function runs these many times when interval is at 0
        self.max_burst = burst
        self.burst = burst
        
        #Each consecutive run when interval is at 0 will be delayed be this much
        self.max_burst_interval = burst_interval
        self.burst_interval = 0
        
        #Before running the function waits this long
        self.max_interval = interval
        self.interval = interval
        
        #If this is true the update resets after burst and interval are both at 0
        self.looping = looping
        
    def run( self ) :
        if self.interval > 0 :
            self.interval = self.interval - 1
            return True
        if self.burst > 0 :
            if self.burst_interval > 0 :
                self.burst_interval = self.burst_interval - 1
                return True
            self.burst_interval = self.max_burst_interval
            self.burst = self.burst - 1
            self.function( self )
            return True
        if self.looping == True :
            self.interval = self.max_interval
            self.burst = self.max_burst
            self.burst_interval = 0
            return True
        return False
        
        
        
        
        
        
        
        
        
        
        
        
