from Map import *
from Unit import *
from Item import *
from Order import *
from PlayerHandler import *
from random import randint
import pygame
import random
from Constants import *

sys.path.append( 'lib' )
from menu import *

class Scene :

    def __init__( self, game) :
        self.game = game

    def draw( self, view_zoom, view_offset, settings ) :
        pass

    def Step( self ) :
        pass

    def destroy( self ) :
        pass

class MenuScene(Scene) :

    def __init__( self, game) :
        Scene.__init__(self, game)

    def run_top( self ) :
        surface = pygame.display.set_mode((1280,720))
        surface.fill((51,51,51))
        img = pygame.image.load('res/img/bg.jpg')
        surface.blit(img,(0,0))
        menu = Menu()
        menu.init(['Start','Options','Quit'], surface)
        menu.draw()
        pygame.key.set_repeat(199,69)#(delay,interval)
        pygame.display.update()
        self.running = 1
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        menu.draw(-1) #here is the Menu class function
                    if event.key == K_DOWN:
                        menu.draw(1) #here is the Menu class function
                    if event.key == K_RETURN :
                        if menu.get_position() == 0:
                            #self.game.change_scene(SCENE_TYPE_GAME, 'res/maps/compiled_map1.js')
                            self.run_select()
                            self.running = 0
                        elif menu.get_position() == 1:
                            self.run_option()
                            self.running = 0
                        elif menu.get_position() == 2:#here is the Menu class function
                            pygame.display.quit()
                            sys.exit()
                    if event.key == K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                    pygame.display.update()
                elif event.type == QUIT:
                    pygame.display.quit()
                    sys.exit()
            pygame.time.wait(8)

    def run_option( self ) :
        surface = pygame.display.set_mode((1280,720))
        surface.fill((51,51,51))
        menu = Menu()

        if self.game.gamesettings.sound == True :
            soundsettings = 'ON'
        elif self.game.gamesettings.sound == False :
            soundsettings = 'OFF'

        menu.init(['SOUND - '+soundsettings,'DIFFICULTY - '+self.game.gamesettings.difficulty,'Back'], surface)

        menu.draw()
        pygame.key.set_repeat(199,69)#(delay,interval)
        pygame.display.update()
        self.running = 1
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        menu.draw(-1) #here is the Menu class function
                    if event.key == K_DOWN:
                        menu.draw(1) #here is the Menu class function
                    if event.key == K_RETURN:
                        if menu.get_position() == 0:
                            if self.game.gamesettings.sound == True :
                                self.game.gamesettings.sound = False
                            else :
                                self.game.gamesettings.sound = True
                            self.run_option()
                            self.running = 0
                        elif menu.get_position() == 1:
                            if self.game.gamesettings.difficulty == 'EASY' :
                                self.game.gamesettings.difficulty = 'HARD'
                            else :
                                self.game.gamesettings.difficulty = 'EASY'
                            self.run_option()
                            self.running = 0
                        elif menu.get_position() == 2:#here is the Menu class function
                            self.run_top()
                            self.running = 0
                    if event.key == K_ESCAPE:
                        self.run_top()
                        self.running = 0
                    pygame.display.update()
                elif event.type == QUIT:
                    pygame.display.quit()
                    sys.exit()
            pygame.time.wait(8)

    def run_select( self ) :
        surface = pygame.display.set_mode((1280,720))
        surface.fill((0,0,0))
        #img = pygame.image.load('res/img/bg.jpg')
        #surface.blit(img,(0,0))
        myfont = pygame.font.SysFont("monospace", 15)
        keynotset = 1
        for x in range(0, 4):
            if x < len(self.game.player_handler.player_to_join_list):
                player = myfont.render("Joined", 1, (255,255,0))
                surface.blit(player, (300+(200*x), 100))
            elif self.game.player_handler.player_to_join_keyboard == 1 and keynotset == 1:
                player = myfont.render("Joined", 1, (255,255,0))
                surface.blit(player, (300+(200*x), 100))
                keynotset = 0
            else:
                player = myfont.render("Press Start", 1, (255,255,0))
                surface.blit(player, (300+(200*x), 100))

        player = myfont.render("Press Y to Start", 1, (255,255,0))
        surface.blit(player, (600, 500))

        pygame.key.set_repeat(199,69)#(delay,interval)
        pygame.display.update()
        self.running = 1
        while self.running:
            for event in pygame.event.get():
                for joystick in self.game.player_handler.joystick_list :
                    start = joystick.get_button( JOYSTICK_BUTTON_START )
                    if start == 1 and self.joystick_player_exists( joystick.get_id() ) == False :
                        self.game.player_handler.player_to_join_list += [ joystick.get_id() ]
                        self.run_select()
                        self.running = 0
                    if joystick.get_button( JOYSTICK_BUTTON_PICKUP ) == 1 :
                        if len(self.game.player_handler.player_to_join_list) > 0:
                            self.game.change_scene(SCENE_TYPE_GAME, 'res/maps/compiled_map1.js')
                            self.running = 0
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.game.player_handler.player_to_join_keyboard = 1
                        self.run_select()
                        self.running = 0
                    if event.key == K_y:
                        self.game.change_scene(SCENE_TYPE_GAME, 'res/maps/compiled_map1.js')
                        self.running = 0
                    pygame.display.update()
                elif event.type == QUIT:
                    pygame.display.quit()
                    sys.exit()
            pygame.time.wait(8)

    def joystick_player_exists( self, joystick_id ) :
        for player in self.game.player_handler.player_to_join_list :
            if player == joystick_id :
                return True
        return False

class GameScene(Scene) :

    def __init__( self, game, world, scene_data ) :
        Scene.__init__(self, game)
        self.game.sound_handler.play_music('default')
        self.entity_list = []
        self.orders = []
        self.world = world
        self.update_list = []
        self.screen = Screen( game )
        self.sprite_group = pygame.sprite.LayeredDirty()
        self.map = Map( self, world, scene_data.get( 'grid' ) )

        image = Image( "res/img/environment/default.png", game.image_handler, ALIGN_BOTTOM_CENTER )
        self.sprite_group.add( image )
        self.hud = Hud( self )

        '''self.target_unit = PlayerCharacter( self, ( 44,40 ) )
        self.screen.focus_positions += [ self.target_unit.body.transform.position ]


        player1 = Player( self.game, self.target_unit )
        self.hud.add_player( player1 )
        self.game.player_handler.add_player( player1 )
        self.game.player_handler.add_input( Input( player1, Keys.K_m, player1.change_scene ) )
        self.game.player_handler.add_input( Input( player1, Keys.K_w, player1.move_up ) )
        self.game.player_handler.add_input( Input( player1, Keys.K_s, player1.move_down ) )
        self.game.player_handler.add_input( Input( player1, Keys.K_a, player1.move_left ) )
        self.game.player_handler.add_input( Input( player1, Keys.K_d, player1.move_right ) )
        self.game.player_handler.add_input( Input( player1, Keys.K_e, player1.pickup, False ) )
        self.game.player_handler.add_input( Input( player1, -100, player1.turn ) )
        self.game.player_handler.add_input( Input( player1, -101, player1.use_item ) )

        self.add_entity( self.target_unit )

        '''

        '''
        self.target_unit = PlayerCharacter( self, ( 24,40 ) )
        self.add_entity( self.target_unit )
        unit = Character( self, ( 40,25 ) )
        self.screen.focus_positions += [ unit.body.transform.position ]
        self.add_entity( unit )
        self.orders.append( AttackOrder( [ unit ], self.target_unit ) )
'''
        '''player2 = Player( self.game, unit )
        self.hud.add_player( player2 )'''

    def get_spawn_point( self ) :
        return random.choice( self.map.spawn_list )

    def draw( self, view_zoom, view_offset, settings ) :
        rects = []
        self.map.update( view_zoom, view_offset, settings )
        rects += self.map.sprite_group.draw( self.game.screen )
        self.hud.update( settings )
        rects += self.hud.sprite_group.draw( self.game.screen )
        for entity in self.entity_list :
            body = entity.body_handler
            if body != 0 :
                body.update_images( view_zoom, view_offset, settings )
                rects += body.sprite_group.draw( self.game.screen )
        pygame.display.update( rects )
        return

    def add_entity( self, entity ) :
        if self.entity_list.__contains__( entity ) :
            return False
        self.entity_list.append( entity )
        self.add_update( Update( entity, entity.update ) )

    def remove_entity( self, entity ) :
        if self.entity_list.__contains__( entity ) == False :
            print entity.__class__.__name__ + " ALREADY GONE"
            return False
        self.entity_list.remove( entity )
        for update in self.update_list :
            if update.owner == entity :
                self.remove_update( update )
        entity.body_handler.destroy()

    def add_update( self, update ) :
        if update == None :
            return False
        if self.update_list.__contains__( update ) :
            return False
        self.update_list.append( update )
        return True

    def remove_update( self, update ) :
        if self.update_list.__contains__( update ) :
            self.update_list.remove( update )
            return True
        return False

    def Step( self ) :
        #self.game.sound_handler.play_sound('shoot')
        self.screen.update_camera_center()
        for update in self.update_list :
            update.run()

    def destroy( self ) :
        while len( self.entity_list ) != 0 :
            entity = self.entity_list[0]
            entity.alive = False
            self.remove_entity( entity )
        while len( self.orders ) != 0 :
            order = self.orders[0]
            self.orders.remove( order )
        while len( self.update_list ) != 0 :
            update = self.update_list[0]
            self.update_list.remove( update )
        self.hud.destroy()
        self.map.destroy()
        self.update_list = 0
        self.map = 0
        self.hud = 0
        self.screen = 0
        self.entity_list = 0
        self.orders = 0
        self.world.ClearForces()

class Screen :

    def __init__( self, game, shake_magnitude = 20 ) :
        self.game = game
        self.shake_offset = (0,0)
        self.shake_magnitude = shake_magnitude
        self.focus_positions = []
        self.shake_time = 0
        self.current_zoom = -1

    def update_camera_center( self ) :
        center_position = (0,0)
        if len( self.focus_positions ) == 0 :
            self.game.setCenter( (25,25) )
            return
        for position in self.focus_positions :
            if center_position == (0,0) :
                center_position = position
                continue
            center_position = ( center_position[0] + position[0], center_position[1] + position[1] )
        center_position = ( center_position[0] / len( self.focus_positions ), center_position[1] / len( self.focus_positions ) )
        self.game.setCenter( center_position )
        if self.shake_time > 0 :
            self.shake_offset = ( randint(-self.shake_magnitude,self.shake_magnitude), randint(-self.shake_magnitude,self.shake_magnitude) )
            self.game._viewOffset[ 0 ] += self.shake_offset[0]
            self.game._viewOffset[ 1 ] += self.shake_offset[1]
            self.shake_time -= 1

class Update :

    def __init__( self, owner, function, interval = 1, burst = 1, burst_interval = 1, looping = True ) :
        #This game_objects update function runs when interval is at 0, must be a GameObject
        self.owner = owner
        self.function = function

        #The function runs these many times when interval is at 0
        self.max_burst = burst
        self.burst = burst

        #Each consecutive run when interval is at 0 will be delayed be this much
        self.max_burst_interval = burst_interval
        self.burst_interval = 0

        #Before running the function waits this long
        self.max_interval = interval
        self.interval = interval

        #If this is true the update resets after burst and interval are both at 0
        self.looping = looping

    def run( self ) :
        if self.interval > 0 :
            self.interval = self.interval - 1
            return True
        if self.burst > 0 :
            if self.burst_interval > 0 :
                self.burst_interval = self.burst_interval - 1
                return True
            self.burst_interval = self.max_burst_interval
            self.burst = self.burst - 1
            self.function( self )
            return True
        if self.looping == True :
            self.interval = self.max_interval
            self.burst = self.max_burst
            self.burst_interval = 0
            return True
        return False

class Hud :

    def __init__( self, scene ) :
        self.player_list = []
        self.hud_positions = [ (0,0),(0,1),(1,0),(1,1) ]
        self.scene = scene
        self.huds = []
        self.sprite_group = pygame.sprite.LayeredDirty()

    def add_player( self, player ) :
        if player in self.player_list :
            return False
        if len( self.player_list ) == 4 :
            return False
        self.player_list += [ player ]
        self.huds += [ PlayerHud( self.sprite_group ) ]
        return True

    def remove_player( self, player ) :
        if player in self.player_list :
            self.player_list.remove( player )
            return True
        return False

    def update( self, settings ) :
        for index, player in enumerate( self.player_list ) :
            pos = ( self.hud_positions[ index ][0] * ( settings.screenSize[0] - 120 ), self.hud_positions[ index ][1] * ( settings.screenSize[1] - 40 ) )
            hud = self.huds[ index ]
            self.draw_player( player, hud, pos )

    def draw_player( self, player, hud, pos ) :
        self.draw_health_bar( pos, hud, float( player.character.health ) / float( player.character.max_health ) )

    def draw_health_bar( self, pos, hud, percentage ) :
        max_width = 100
        width = max_width * percentage
        bar = pygame.Surface( ( int(width), 6 ) )
        bar.fill( (255,0,0) )
        hud.health_bar.image = bar
        hud.health_bar.dirty = 1
        hud.health_bar.rect = bar.get_rect()
        hud.health_bar.rect.x = pos[0] + 10
        hud.health_bar.rect.y = pos[1] + 10

    def destroy( self ) :
        while len( self.player_list ) != 0 :
            self.player_list.remove( self.player_list[0] )
        while len( self.huds ) != 0 :
            self.huds.remove( self.huds[0] )

class PlayerHud :

    def __init__( self, sprite_group ) :
        self.sprite_group = sprite_group
        self.health_bar = pygame.sprite.DirtySprite()
        self.sprite_group.add( self.health_bar )
