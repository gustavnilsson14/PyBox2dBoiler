from Map import *
from Unit import *
from Order import *

class Scene() :
    
    def __init__( self, game, world, scene_data ) :
        self.units = []
        self.orders = []
        self.game = game
        self.world = world
        self.map = Map( world, scene_data.get( 'grid' ) )
        
        unit = Unit( self, ( 0,0 ) )
        self.units.append( unit )
        
        self.orders.append( MoveOrder( [ unit ], ( 23,25 ) ) )
        
        #unit.move( (23,20) )
        
    
    def Step( self ) :
        for unit in self.units :
            unit.Step()
    
    def destroy( self ) :
        pass
