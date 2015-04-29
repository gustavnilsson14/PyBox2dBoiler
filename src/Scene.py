from Map import *

class Scene() :
    
    def __init__( self, world, scene_data ) :
        self.world = world
        self.map = Map( world, scene_data.get( 'grid' ) )
        
    def destroy( self ) :
        pass
