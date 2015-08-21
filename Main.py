import sys
import os.path
import json
sys.path.append( 'lib' )
sys.path.append( 'src' )
from framework import *
from SoundHandler import *
from Scene import *
from GameSettings import *
import math
from Constants import *
from PlayerHandler import *
from Core import *
from pygame.locals import *
import time

class Game (Framework):

    def __init__( self ) :
        pygame.mixer.init()
        self.gamesettings = GameSettings()
        self.sound_handler = SoundHandler( self.gamesettings )
        self.pause_time = 0
        self.garbage_body_list = []
        self.garbage_joint_list = []
        self.defaultZoom = 80.0
        self.minZoom = 15.0
        self.maxZoom = 285.0
        super(Game, self).__init__()
        self.current_scene = 0
        self.world.gravity = (0,0)
        self.image_handler = ImageHandler( self )

        self.change_scene( SCENE_TYPE_MENU )
        #self.change_scene(SCENE_TYPE_GAME, 'res/maps/compiled_map1.js')

        self.reset_zoom()

        self.player_handler = PlayerHandler( self )
        self.check_joysticks()
        #-100 is the mouse
        self.pressed_keys = [ -100 ]

    def change_scene( self, type, map_file = False) :
        print self.current_scene
        if self.current_scene != 0 :
            self.current_scene.destroy()
        self.player_handler = PlayerHandler( self )

        if type == SCENE_TYPE_MENU :
            self.current_scene = MenuScene( self )
            self.current_scene.run_top()
            return True

        if os.path.isfile( map_file ) == False :
            return False
        with open (map_file, "r") as myfile :
            map_data = myfile.read().replace('\n', '')
            self.current_scene = GameScene( self, self.world, json.loads( map_data ) )

    def reset_zoom( self ) :
        #This property manages zoom level
        self.viewZoom = self.defaultZoom

    def Step(self, settings):
        if self.pause_time > 0 :
            self.pause_time -= 1
            return
        while len( self.garbage_joint_list ) != 0:
            garbage_joint = self.garbage_joint_list[0]
            self.world.DestroyJoint( garbage_joint )
            self.garbage_joint_list.remove( garbage_joint )
        while len( self.garbage_body_list ) != 0:
            garbage_body = self.garbage_body_list[0]
            self.world.DestroyBody( garbage_body )
            self.garbage_body_list.remove( garbage_body )

        background_colour = (55,55,55)

        self.screen.fill( background_colour )
        if self.current_scene != 0 :
            self.current_scene.Step()
        super( Game, self ).Step( settings )

        self.current_scene.draw( self.viewZoom, self.viewOffset, settings )

        self.player_handler.update( self.pressed_keys )

        for contact in self.world.contacts :
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

    def check_joysticks( self ) :
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick( i )
            joystick.init()
            self.player_handler.joystick_list.append( joystick )

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

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == Keys.K_ESCAPE):
                return False
            elif event.type == KEYDOWN:
                self._Keyboard_Event(event.key, down=True)
            elif event.type == KEYUP:
                self._Keyboard_Event(event.key, down=False)
            elif event.type == MOUSEBUTTONDOWN:
                p = self.ConvertScreenToWorld(*event.pos)
                if event.button == 1: # left
                    mods = pygame.key.get_mods()
                    if mods & KMOD_LSHIFT:
                        self.ShiftMouseDown( p )
                    else:
                        self.MouseDown( p )
                elif event.button == 2: #middle
                    pass
                elif event.button == 3: #right
                    self.rMouseDown = True
                elif event.button == 4:
                    self.viewZoom *= 1.1
                    if self.viewZoom > self.maxZoom :
                        self.viewZoom = self.maxZoom
                    self.image_handler.zoom_images()
                elif event.button == 5:
                    self.viewZoom /= 1.1
                    if self.viewZoom < self.minZoom :
                        self.viewZoom = self.minZoom

                    self.image_handler.zoom_images()
            elif event.type == MOUSEBUTTONUP:
                p = self.ConvertScreenToWorld(*event.pos)
                if event.button == 3: #right
                    self.rMouseDown = False
                else:
                    self.MouseUp(p)
            elif event.type == MOUSEMOTION:
                p = self.ConvertScreenToWorld(*event.pos)

                self.MouseMove(p)

                if self.rMouseDown:
                    self.viewCenter -= (event.rel[0]/5.0, -event.rel[1]/5.0)


        return True

if __name__=="__main__":
     main(Game)
