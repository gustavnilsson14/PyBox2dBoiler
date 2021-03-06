import sys
import os.path
import json
import math
import time
import Box2D
from importlib import import_module
sys.path.append( os.path.abspath("./lib") )
sys.path.append( os.path.abspath("./src") )
sys.path.append( os.path.abspath("./res") )
sys.path.insert(0, './lib')
from framework import *
from SoundHandler import *
from Scene import *
from GameSettings import *
from Constants import *
from PlayerHandler import *
from Core import *
from pygame.locals import *

class Game (Framework):

    def __init__( self ) :
        pygame.mixer.init()
        self.gamesettings = GameSettings()
        self.sound_handler = SoundHandler( self.gamesettings )
        self.pause_time = 0
        self.time = 0
        self.garbage_body_list = []
        self.garbage_joint_list = []
        self.defaultZoom = 80.0
        self.minZoom = 15
        self.maxZoom = 285
        super(Game, self).__init__()
        self.current_scene = 0
        self.world.gravity = (0,0)
        self.image_handler = ImageHandler( self )

        #self.change_scene(SCENE_TYPE_GAME, 'res/maps/compiled_map1.js')

        self.reset_zoom()

        #-100 is the mouse
        self.pressed_keys = [ -100 ]
        self.change_scene( SCENE_TYPE_MENU )

    def change_scene( self, type, map_file = False ) :
        if self.current_scene != 0 :
            self.current_scene.destroy()
        self.take_out_garbage()
        self.total_reset()
        if type == SCENE_TYPE_MENU or type == SCENE_TYPE_DEFETED :
            self.sound_handler.stop_music( 'demons_acecream' )
            self.sound_handler.stop_music( 'default' )
            self.sound_handler.play_music( 'default' )
            self.player_handler = PlayerHandler( self )
            self.check_joysticks()
            self.current_scene = MenuScene( self )

            if type == SCENE_TYPE_MENU:
                self.current_scene.run_top()
            elif type == SCENE_TYPE_DEFETED:
                self.current_scene.run_defeated()
            return True

        self.player_handler.check_player_opt_in( self.pressed_keys )
        if os.path.isfile( map_file ) == False :
            self.current_scene = 0
            return False

        with open (map_file, "r") as myfile :
            map_data = myfile.read().replace('\n', '')
            self.sound_handler.stop_music( 'demons_acecream' )
            self.sound_handler.stop_music( 'default' )
            self.sound_handler.play_music( 'demons_acecream' )
            self.current_scene = GameScene( self, self.world, json.loads( map_data ) )

    def reset_zoom( self ) :
        #This property manages zoom level
        self.viewZoom = self.defaultZoom

    def total_reset( self ) :
        while len( self.world.joints ) != 0 :
            garbage_joint = self.world.joints[0]
            self.world.DestroyJoint( garbage_joint )
        while len( self.world.bodies ) != 0 :
            garbage_body = self.world.bodies[0]
            self.world.DestroyBody( garbage_body )

    def take_out_garbage( self ) :
        while len( self.garbage_joint_list ) != 0:
            garbage_joint = self.garbage_joint_list[0]
            self.world.DestroyJoint( garbage_joint )
            self.garbage_joint_list.remove( garbage_joint )
        while len( self.garbage_body_list ) != 0:
            garbage_body = self.garbage_body_list[0]
            self.world.DestroyBody( garbage_body )
            self.garbage_body_list.remove( garbage_body )

    def Step(self, settings):
        if self.pause_time > 0 :
            self.pause_time -= 1
            return
        self.time += 1
        self.take_out_garbage()

        background_colour = (55,55,55)

        self.screen.fill( background_colour )
        if self.current_scene != 0 :
            self.current_scene.Step()
        super( Game, self ).Step( settings )

        self.current_scene.draw( self.viewZoom, self.viewOffset, settings )

        self.player_handler.update( self.pressed_keys )

        for contact in self.world.contacts :
            if contact.touching == False :
                continue
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
            if event.type == QUIT :
                return False
            elif (event.type == KEYDOWN and event.key == Keys.K_ESCAPE) :
                self.change_scene(SCENE_TYPE_MENU)
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
                    self.viewZoom += 1
                    if self.viewZoom > self.maxZoom :
                        self.viewZoom = self.maxZoom
                    self.image_handler.zoom_images()
                elif event.button == 5:
                    self.viewZoom -= 1
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
