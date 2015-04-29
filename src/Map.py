from framework import *

class Map() :
    
    def __init__( self, world, grid ) :
        self.world = world
        self.grid = grid
        x = 0
        while x < len( grid ) :
            row = grid[ x ]
            y = 0
            while y < len( row ) :
                tile = row[ y ]
                if tile.get( 'collision' ) != None :
                    tile[ "content" ] = self.create_block( (x,y) )
                    print tile
                y += 1
            x += 1
            
    def create_block( self, pos ) :
        return self.world.CreateStaticBody(
            position = pos,
            fixedRotation=True,
            allowSleep=False,
            fixtures=b2FixtureDef(shape=b2PolygonShape(box=(0.5, 0.5)), density=20.0),
        )
