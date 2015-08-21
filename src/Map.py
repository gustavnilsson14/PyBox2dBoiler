from framework import *
from fov import *
from pathfinding import *
from Constants import *
from Core import *
from Body import *
import time
import pygame

class Map() :
    
    def __init__( self, scene, world, grid ) :
        self.scene = scene
        self.world = world
        self.grid = grid
        self.fovbits = []
        self.spawn_list = []
        self.pathfinder = Pathfinder( grid )
        self.fov = FovChecker( grid )
        self.tile_list = []
        self.sprite_group = pygame.sprite.LayeredDirty()
        x = 0
        while x < len( grid ) :
            row = grid[ x ]
            y = 0
            while y < len( row ) :
                tile = row[ y ]
                content = Floor( scene, (x,y) )
                if content.image != 0 :
                    self.sprite_group.add( content.image )
                self.tile_list.append( content )
                y += 4
            x += 4
        x = 0
        while x < len( grid ) :
            row = grid[ x ]
            y = 0
            while y < len( row ) :
                tile = row[ y ]
                content = 0
                if tile.get( 'collision' ) != None :
                    content = Block( scene, (x,y) )
                if tile.get( 'weaponpoints' ) != None :
                    from Item import *
                    if randint( 0, 4 ) > 2 :
                        item = Machinegun( self.scene, ( x, y ) )
                    else :
                        item = Shotgun( self.scene, ( x, y ) )
                    self.scene.add_entity( item )
                    item.create_body( ( x, y ) )
                    #content = Block( scene, (x,y) )
                if tile.get( 'spawn' ) != None :
                    self.spawn_list.append( ( x, y ) )
                if content != 0 :
                    if content.image != 0 :
                        self.sprite_group.add( content.image )
                    tile[ "content" ] = content
                    self.tile_list.append( content )
                y += 1
            x += 1
        x = 0
    
    def destroy( self ) :
        while len( self.tile_list ) != 0 :
            tile = self.tile_list[0]
            tile.destroy()
            self.tile_list.remove( tile )
        self.tile_list = []
    
    def update( self, view_zoom, view_offset, settings ) :
        for tile in self.tile_list :
            tile.update( view_zoom, view_offset, settings )
    
    def find_path( self, start, goal ) :
        path = self.pathfinder.find( start, goal )
        if path != False :
            return path
        return 0
            
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
        
class Tile( Entity ) :
    
    def __init__( self, scene, pos ) :
        Entity.__init__( self, scene )
        self.position = pos
        self.body_handler = Body( scene )
        self.image = 0
        
    def update( self, view_zoom, view_offset, settings ) :
        if self.image != 0 :
            self.image.update( self.position, 0, view_zoom, view_offset, settings )
    
    def destroy( self ) :
        Entity.destroy( self )
    
class Block( Tile ) :
    
    def __init__( self, scene, pos ) :
        Tile.__init__( self, scene, pos )
        self.image = Image( "res/img/environment/block.png", scene.game.image_handler, ALIGN_CENTER_CENTER )
        self.body = self.body_handler.create_block( self, scene, pos, 1, FILTER_DEFAULT )
        self.types += [ "block" ]
        
    def handle_collision( self, my_fixture, colliding_fixture ) :
        pass
        
class Floor( Tile ) :
    
    def __init__( self, scene, pos ) :
        Tile.__init__( self, scene, pos )
        #self.image = Image( "res/img/environment/floor.png", scene.game.image_handler, ALIGN_CENTER_CENTER )
        self.types += [ "floor" ]
