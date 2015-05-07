import sys
import os.path
import json
sys.path.append( 'lib' )
sys.path.append( 'src' )
from framework import *
from Scene import *
import pygame
import math

class Game (Framework):
    
    def __init__( self ) :
        self.garbage_body_list = []
        self.defaultZoom = 40.0
        super(Game, self).__init__()
        self.current_scene = 0
        self.world.gravity = (0,0)
        self.change_scene( "res/maps/compiled_example.js" )
        self.reset_zoom()
        self.testimg = pygame.image.load("image.png")
        
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
            if fixtureA.sensor == True :
                fixtureA.body.userData.handle_collision( fixtureA, fixtureB )
            if fixtureB.sensor == True :
                fixtureB.body.userData.handle_collision( fixtureB, fixtureA )
        '''
        for image in self.draw_list :
            p = logo_shape.body.position
            p = Vec2d(p.x, flipy(p.y))
            
            # we need to rotate 180 degrees because of the y coordinate flip
            angle_degrees = math.degrees(logo_shape.body.angle) + 180 
            rotated_logo_img = pygame.transform.rotate(logo_img, angle_degrees)
            
            offset = Vec2d(rotated_logo_img.get_size()) / 2.
            p = p - offset
            
            self.screen.blit(rotated_logo_img, p)
        '''
        #print settings.screenSize
        self.draw_image( settings, (20,1), self.testimg )
        #print imgpos
        #self.DrawStringAt(500, 100, "LULZLULZLULZLULZLULZLULZLULZLULZ", ( 255, 0, 0, 255 ) )
        
    def draw_image( self, settings, pos, image ) :
        posX = pos[0]  * self.viewZoom
        posY = pos[1]  * self.viewZoom
        zoom = self.viewZoom/self.defaultZoom
        self.newimg = pygame.transform.scale( image, ( int( self.testimg.get_width() * zoom ), int( self.testimg.get_height() * zoom ) ) )
        imgX = -( self.newimg.get_width() / 2 ) - self.viewOffset[0]
        imgY = self.viewOffset[1] - self.newimg.get_height() 
        if imgY >= 0 :
            imgY = settings.screenSize[ 1 ] - imgY
        else :
            imgY = settings.screenSize[ 1 ] - math.fabs( imgY )
        imgpos = ( imgX + posX, imgY - posY )
        self.screen.blit( self.newimg, imgpos )
        
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
    
if __name__=="__main__":
     main(Game)
