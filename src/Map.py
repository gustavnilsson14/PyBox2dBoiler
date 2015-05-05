from framework import *
from fov import *
from pathfinding import *
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
                    tile[ "content" ] = self.create_block( (x,y) )
                y += 1
            x += 1
            
    def create_block( self, pos ) :
        return self.world.CreateKinematicBody(
            position = pos,
            fixedRotation=True,
            allowSleep=False,
            fixtures=b2FixtureDef(shape=b2PolygonShape(box=(0.5, 0.5)), density=20.0),
        )
        
    def find_path( self, start, goal ) :
        path = self.pathfinder.find( start, goal )
        if path != False :
            return path
        return False
            
    def get_visible_tiles( self, pos ) :
        fov = self.fov.check( pos, 5 )
        for fovbit in self.fovbits :
            self.scene.game.garbage_body_list.append( fovbit )
        self.fovbits = []
        for fovbit in fov :
            print fovbit
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
        
            
        
