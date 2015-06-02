import sys
import os.path
import json
sys.path.append( 'lib' )
sys.path.append( 'src' )
from framework import *
from Scene import *
import math
from Constants import *
from PlayerHandler import *

class Game (Framework):
    
    def __init__( self ) :
        self.pause_time = 0
        self.player_handler = PlayerHandler( self )
        self.garbage_body_list = []
        self.garbage_joint_list = []
        self.defaultZoom = 80.0
        super(Game, self).__init__()
        self.current_scene = 0
        self.world.gravity = (0,0)
        self.change_scene( "res/maps/compiled_example.js" )
        self.reset_zoom()
        #-100 is the mouse
        self.pressed_keys = [ -100 ]
        
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
        self.current_scene.draw( self.viewZoom, self.viewOffset, self.defaultZoom, settings )
        '''
        for body in self.world.bodies :
            if body.userData == None :
                continue
            image = body.userData.get( 'image' )
            if image != None :
                self.draw_image( settings, body.transform, image )
        '''
        if self.pause_time > 0 :
            self.pause_time -= 1
            return
        for garbage_body in self.garbage_body_list :
            self.world.DestroyBody( garbage_body )
            self.garbage_body_list.remove( garbage_body )
        for garbage_joint in self.garbage_joint_list :
            self.world.DestroyJoint( garbage_joint )
            self.garbage_joint_list.remove( garbage_joint )
            
        super( Game, self ).Step( settings )
        
        self.player_handler.update( self.pressed_keys )
        
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
        
    def Keyboard(self, key):
        if key in self.pressed_keys :
            return False
        self.pressed_keys += [ key ]
        return True

    def KeyboardUp(self, key):
        if key in self.pressed_keys :
            self.pressed_keys.remove( key )
            return True
        return False
        
    def MousePos(self):
        return pygame.mouse.get_pos()
        
    def MouseDown(self, p):
        key = -101
        if key in self.pressed_keys :
            return False
        self.pressed_keys += [ key ]
        
    def MouseUp(self, p):
        key = -101
        if key in self.pressed_keys :
            self.pressed_keys.remove( key )
            return True
        return False
        
        
if __name__=="__main__":
     main(Game)
