import sys
import os.path
import json
sys.path.append( 'lib' )
sys.path.append( 'src' )
from framework import *
from Scene import *
import math
from Constants import *

class Game (Framework):
    
    def __init__( self ) :
        self.garbage_body_list = []
        self.garbage_joint_list = []
        self.defaultZoom = 80.0
        super(Game, self).__init__()
        self.current_scene = 0
        self.world.gravity = (0,0)
        self.change_scene( "res/maps/compiled_example.js" )
        self.reset_zoom()
        
    def change_scene( self, map_file ) :
        if self.current_scene != 0 :
            self.current_scene.destroy()
        if os.path.isfile( map_file ) == False :
            return False
        with open (map_file, "r") as myfile :
            map_data = myfile.read().replace('\n', '')
            self.current_scene = Scene( self, self.world, json.loads( map_data ) )

    def reset_zoom( self ) :
        #This property manages zoom level
        self.viewZoom = self.defaultZoom
        
    def Step(self, settings):
        for garbage_body in self.garbage_body_list :
            self.world.DestroyBody( garbage_body )
            self.garbage_body_list.remove( garbage_body )
        for garbage_joint in self.garbage_joint_list :
            self.world.DestroyJoint( garbage_joint )
            self.garbage_joint_list.remove( garbage_joint )
            
        super( Game, self ).Step( settings )
        
        if self.current_scene != 0 :
            self.current_scene.Step()
        
        # Traverse the contact results. Apply a force on shapes
        # that overlap the sensor.
        for contact in self.world.contacts:
            fixtureA = contact.fixtureA
            fixtureB = contact.fixtureB
            
            if fixtureA.body.userData == None or fixtureB.body.userData == None :
                continue
            if fixtureA.body.userData.get( 'owner' ) == None or fixtureB.body.userData.get( 'owner' ) == None :
                continue
            fixtureA.body.userData.get( 'owner' ).handle_collision( fixtureA, fixtureB )
            fixtureB.body.userData.get( 'owner' ).handle_collision( fixtureB, fixtureA )
        for body in self.world.bodies :
            if body.userData == None :
                continue
            try :
                self.draw_image( settings, body.transform.position, body.userData.get( 'image' ) )
            except AttributeError: 
                pass
    
    def draw_image( self, settings, pos, image ) :
        align = image.align
        posX = pos[0] * self.viewZoom
        posY = pos[1] * self.viewZoom
        zoom = self.viewZoom/self.defaultZoom/2
        new_image = image.get_current_image( zoom )
        alignment = self.get_alignment( new_image, align )
        imgX = alignment[0] - self.viewOffset[0]
        imgY = self.viewOffset[1] + alignment[1]
        
        if imgY >= 0 :
            imgY = settings.screenSize[ 1 ] - imgY
        else :
            imgY = settings.screenSize[ 1 ] --imgY
        
        imgpos = ( imgX + posX, imgY - posY )
        self.screen.blit( new_image, imgpos )
        
    def get_alignment( self, image, align ) :
        if align == ALIGN_BOTTOM_CENTER :
            return ( -( image.get_width() / 2 ), -image.get_height() )
        elif align == ALIGN_CENTER_CENTER :
            return ( -( image.get_width() / 2 ), -( image.get_height() / 2 ) )
        elif align == ALIGN_TOP_CENTER :
            return ( -( image.get_width() / 2 ), -0 )
        elif align == ALIGN_TOP_LEFT :
            return ( -0, -0 )
        elif align == ALIGN_BOTTOM_RIGHT :
            return ( -image.get_width(), -image.get_height() )
        
    def add_garbage_body( self, garbage_body ) :
        if garbage_body == None :
            return False
        if self.garbage_body_list.__contains__( garbage_body ) :
            return False
        self.garbage_body_list.append( garbage_body )
        return True
        
    def remove_garbage_body( self, garbage_body ) :
        if self.garbage_body_list.__contains__( garbage_body ) :
            self.garbage_body_list.remove( garbage_body )
            return True
        return False
        
    def add_garbage_joint( self, garbage_joint ) :
        if garbage_joint == None :
            return False
        if self.garbage_joint_list.__contains__( garbage_joint ) :
            return False
        self.garbage_joint_list.append( garbage_joint )
        return True
        
    def remove_garbage_joint( self, garbage_joint ) :
        if self.garbage_joint_list.__contains__( garbage_joint ) :
            self.garbage_joint_list.remove( garbage_joint )
            return True
        return False
    
if __name__=="__main__":
     main(Game)
