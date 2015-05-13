from framework import *
from fov import *
from pathfinding import *
from Constants import *
import time

class Map() :
    
    def __init__( self, scene, world, grid ) :
        self.scene = scene
        self.world = world
        self.grid = grid
        self.fovbits = []
        self.pathfinder = Pathfinder( grid )
        self.fov = FovChecker( grid )
        x = 0
        while x < len( grid ) :
            row = grid[ x ]
            y = 0
            while y < len( row ) :
                tile = row[ y ]
                if tile.get( 'collision' ) != None :
                    tile[ "content" ] = Block( world, (x,y) )
                y += 1
            x += 1
            
    def find_path( self, start, goal ) :
        path = self.pathfinder.find( start, goal )
        if path != False :
            return path
        return False
            
    def get_visible_tiles( self, pos ) :
        fov = self.fov.check_tiles( pos, 5 )
        return fov
        '''
        #Displays visible tiles as sensor blocks
        for fovbit in self.fovbits :
            self.scene.game.garbage_body_list.append( fovbit )
        self.fovbits = []
        for fovbit in fov :
            newbit = self.world.CreateKinematicBody(
                position = fovbit,
                fixedRotation=True,
                allowSleep=False,
                fixtures=b2FixtureDef(
                    shape=b2PolygonShape(
                        box=(0.3, 0.3)
                    ), 
                    density=0,
                    isSensor=True
                ),
            )
            self.fovbits.append(newbit)
        '''
            
class Block :
    
    def __init__( self, world, pos ) :
        self.body = world.CreateKinematicBody(
            position = pos,
            fixedRotation=True,
            allowSleep=False,
            fixtures=b2FixtureDef(
                filter=b2Filter(
                    groupIndex = 0,
                    categoryBits = FILTER_DEFAULT[0],
                    maskBits = FILTER_DEFAULT[1]
                ),
                shape=b2PolygonShape(
                    box=(0.5, 0.5)
                ), 
                density=20.0
                
            ),
        )
        self.body.userData = self
        
    def handle_collision( self, my_fixture, colliding_fixture ) :
        pass
