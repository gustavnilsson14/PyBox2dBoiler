from Map import *

class Scene() :
    
    def __init__( self, world, scene_data ) :
        self.world = world
        self.map = Map( world, scene_data.get( 'grid' ) )

    def Step( self ) :
        pass
        
    def destroy( self ) :
        self.world.ClearForces()
        while len( self.world.bodies = != 0 :
            self.world.destroyBody( self.world.bodies[0] )
