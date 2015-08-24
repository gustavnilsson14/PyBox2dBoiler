from Map import *
from Unit import *
from Enemy import *
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

    def __init__( self, game ) :
        self.game = game

    def draw( self, view_zoom, view_offset, settings ) :
        pass

    def Step( self ) :
        pass

    def destroy( self ) :
        pass

    def defeat( self, type ) :
        pass

class MenuScene(Scene) :

    def __init__( self, game) :
        Scene.__init__(self, game)

    def run_top( self ) :
        surface = pygame.display.set_mode((1280,720))
        surface.fill((51,51,51))
        img = pygame.image.load('./res/img/bg.jpg')
        surface.blit(img,(0,0))
        menu = Menu()
        menu.init(['Start','Help','Options','Quit'], surface)
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
                            self.run_howtoplay()
                            self.running = 0
                        elif menu.get_position() == 2:
                            self.run_option()
                            self.running = 0
                        elif menu.get_position() == 3:#here is the Menu class function
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
        img = pygame.image.load('res/img/selectbg.jpg')
        surface.blit(img,(0,0))
        myfont = pygame.font.SysFont("monospace", 25)
        keynotset = 1
        for x in range(0, 4):
            if x < len(self.game.player_handler.player_to_join_list):
                player = myfont.render("Joined", 1, (255,255,255))
                surface.blit(player, (65+(320*x), 100))
            elif self.game.player_handler.player_to_join_keyboard == 1 and keynotset == 1:
                player = myfont.render("Joined", 1, (255,255,255))
                surface.blit(player, (65+(320*x), 100))
                keynotset = 0
            else:
                player = myfont.render("Press Start", 1, (255,255,255))
                surface.blit(player, (65+(320*x), 100))

        myfont = pygame.font.SysFont("monospace", 40)
        player = myfont.render("Press Y to Start", 1, (0,0,0))
        surface.blit(player, (500, 500))

        pygame.key.set_repeat(199,69)#(delay,interval)
        pygame.display.update()
        self.running = 1
        while self.running:
            for event in pygame.event.get():
                for joystick in self.game.player_handler.joystick_list :

                    if joystick.get_name() == "Controller (XBOX 360 For Windows)" or joystick.get_name() == "Microsoft X-Box 360 pad" :
                        start = joystick.get_button( XBOX_KEY_MAP[JOYSTICK_BUTTON_START] )
                    else :
                        start = joystick.get_button( GENERIC_KEY_MAP[JOYSTICK_BUTTON_START] )
                    if start == 1 and self.joystick_player_exists( joystick.get_id() ) == False :
                        self.game.player_handler.player_to_join_list += [ joystick.get_id() ]
                        self.run_select()
                        self.running = 0
                    if joystick.get_button( JOYSTICK_BUTTON_PICKUP ) == 1 :
                        if len(self.game.player_handler.player_to_join_list) > 0 or self.game.player_handler.player_to_join_keyboard == 1:
                            self.game.change_scene(SCENE_TYPE_GAME, 'res/maps/compiled_tutorial.js')
                            self.running = 0
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.game.player_handler.player_to_join_keyboard = 1
                        self.run_select()
                        self.running = 0
                    if event.key == K_y:
                        if len(self.game.player_handler.player_to_join_list) > 0 or self.game.player_handler.player_to_join_keyboard == 1:
                            self.game.change_scene(SCENE_TYPE_GAME, 'res/maps/compiled_tutorial.js')
                            self.running = 0
                    pygame.display.update()
                elif event.type == QUIT:
                    pygame.display.quit()
                    sys.exit()
            pygame.time.wait(8)

    def run_help( self ) :
        surface = pygame.display.set_mode((1280,720))
        surface.fill((0,0,0))
        img = pygame.image.load('res/img/help.png')
        surface.blit(img,(0,0))
        pygame.key.set_repeat(199,69)#(delay,interval)
        pygame.display.update()
        self.running = 1
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.run_top()
                    self.running = 0
                elif event.type == QUIT:
                    pygame.display.quit()
                    sys.exit()
            pygame.time.wait(8)

    def run_howtoplay( self ) :
        surface = pygame.display.set_mode((1280,720))
        surface.fill((0,0,0))
        img = pygame.image.load('res/img/howtoplay.png')
        surface.blit(img,(0,0))
        pygame.key.set_repeat(199,69)#(delay,interval)
        pygame.display.update()
        self.running = 1
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.run_help()
                    self.running = 0
                elif event.type == QUIT:
                    pygame.display.quit()
                    sys.exit()
            pygame.time.wait(8)

    def run_defeated( self ) :
        surface = pygame.display.set_mode((1280,720))
        surface.fill((0,0,0))
        img = pygame.image.load('res/img/defeated.png')
        surface.blit(img,(0,0))
        pygame.key.set_repeat(199,69)#(delay,interval)
        pygame.display.update()
        self.running = 1
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.run_top()
                    self.running = 0
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
        self.ai = AI( self, game )
        self.drawn_images = 0
        self.game.sound_handler.play_music('default')
        self.entity_list = []
        self.orders = []
        self.world = world
        self.update_list = []
        self.screen = Screen( game )
        self.sprite_group = pygame.sprite.LayeredDirty()
        self.map = Map( self, world, scene_data.get( 'grid' ) )
        self.meta_data = scene_data.get('metadata').get('meta')

        image = Image( "res/img/environment/default.png", game.image_handler, ALIGN_BOTTOM_CENTER )
        self.sprite_group.add( image )
        self.hud = Hud( self )
        self.game.player_handler.add_player_characters( self )

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
        #print self.drawn_images
        self.drawn_images = 0
        pygame.display.update( rects )
        return

    def add_entity( self, entity ) :
        if self.entity_list.__contains__( entity ) :
            return False
        self.entity_list.append( entity )
        for update in self.update_list :
            if update.owner == entity :
                return
        self.add_update( Update( entity, entity.update ) )

    def remove_entity( self, entity ) :
        if self.entity_list.__contains__( entity ) == False :
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
        self.ai.update()

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

    def defeat( self, type ) :
        if type == DEFEAT_GROUP_AI :
            self.hud.huds[0].sprite_group.add( self.hud.huds[0].victory_text )
            width = 180
            bar = pygame.Surface( ( int(width), 50 ) )
            bar.fill( (255,255,255) )
            myfont = pygame.font.SysFont("monospace", 35)
            victory = myfont.render("VICTORY!", 1, (0,0,0))
            bar.blit(victory, (0,0))
            self.hud.huds[0].victory_text.image = bar
            self.hud.huds[0].victory_text.dirty = 1
            self.hud.huds[0].victory_text.rect = bar.get_rect()
            self.hud.huds[0].victory_text.rect.x = 550
            self.hud.huds[0].victory_text.rect.y = 200

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if self.game.change_scene( SCENE_TYPE_GAME, self.meta_data.get('next') ) == False :
                        print "VICTORY"
                        self.game.change_scene( SCENE_TYPE_MENU )

            for joystick in self.game.player_handler.joystick_list :
                next_level = 0
                if joystick.get_name() == "Controller (XBOX 360 For Windows)" or joystick.get_name() == "Microsoft X-Box 360 pad" :
                    next_level = joystick.get_button( XBOX_KEY_MAP[JOYSTICK_BUTTON_PICKUP] )
                else :
                    next_level = joystick.get_button( GENERIC_KEY_MAP[JOYSTICK_BUTTON_PICKUP] )
                if  next_level == 1:
                    if self.game.change_scene( SCENE_TYPE_GAME, self.meta_data.get('next') ) == False :
                        print "VICTORY"
                        self.game.change_scene( SCENE_TYPE_MENU )
            return False
        elif type == DEFEAT_GROUP_PLAYERS :
            for player in self.game.player_handler.player_list :
                if player.character.alive == True :
                    return
            print "DEFEAT"
            self.game.change_scene( SCENE_TYPE_DEFETED )

class Screen :

    def __init__( self, game, shake_magnitude = 0 ) :
        self.game = game
        self.shake_offset = (0,0)
        self.shake_magnitude = shake_magnitude
        self.focus_positions = []
        self.players_focus = []
        self.shake_time = 0
        self.current_zoom = -1

    def update_camera_center( self ) :
        index = 0
        for player in self.players_focus :
            if player.character.health <= 0:
                self.players_focus.pop(index)
            index += 1

        center_position = (0,0)
        distance = 0
        if len( self.players_focus ) == 0 :
            self.game.setCenter( (25,25) )
            return
        for player in self.players_focus :
            if center_position == (0,0) :
                center_position = player.character.body.transform.position
                continue
            center_position = ( center_position[0] + player.character.body.transform.position[0], center_position[1] + player.character.body.transform.position[1] )

        center_position = ( center_position[0] / len( self.players_focus ), center_position[1] / len( self.players_focus ) )

        for player in self.players_focus :
            tempdistance = numpy.sqrt(numpy.power(center_position[0]-player.character.body.transform.position[0],2)+numpy.power(center_position[1]-player.character.body.transform.position[1],2))
            if tempdistance > distance :
                distance = numpy.absolute(tempdistance)

        if distance != 0 :
            self.game.viewZoom = 75-distance*2.5
            if self.game.viewZoom < 30 :
                self.game.viewZoom = 30
            if self.game.viewZoom > 90 :
                self.game.viewZoom = 90

        self.game.setCenter( center_position )
        '''if self.shake_time > 0 :
            self.shake_offset = ( randint(-self.shake_magnitude,self.shake_magnitude), randint(-self.shake_magnitude,self.shake_magnitude) )
            self.game._viewOffset[ 0 ] += self.shake_offset[0]
            self.game._viewOffset[ 1 ] += self.shake_offset[1]
            self.shake_time -= 1'''

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
        self.huds += [ PlayerHud( player, self.sprite_group ) ]
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
            hud.update(self.scene, settings)
            self.draw_player( player, hud, pos )

    def draw_player( self, player, hud, pos ) :
        if player.character != 0 :
            if player.character.alive == False :
                return
        self.draw_health_bar_bg( pos, hud )
        self.draw_health_bar( pos, hud, float( player.character.health ) / float( player.max_health ) )
        self.draw_power_bar_bg( pos, hud)
        self.draw_power_bar( pos, hud, float( player.character.power ) / float( player.max_power ) )
        self.draw_orb_bar( pos, hud )
        #self.draw_orb_bar( pos, hud, float( player.character.power ) / float( player.character.max_power ) )

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

    def draw_health_bar_bg( self, pos, hud ) :
        width = 102
        bar = pygame.Surface( ( int(width), 8 ) )
        bar.fill( (0,0,0) )
        hud.health_bar_bg.image = bar
        hud.health_bar_bg.dirty = 1
        hud.health_bar_bg.rect = bar.get_rect()
        hud.health_bar_bg.rect.x = pos[0] + 9
        hud.health_bar_bg.rect.y = pos[1] + 9

    def draw_power_bar( self, pos, hud, percentage ) :
        max_width = 100
        width = max_width * percentage
        bar = pygame.Surface( ( int(width), 6 ) )
        bar.fill( (0,255,0) )
        hud.power_bar.image = bar
        hud.power_bar.dirty = 1
        hud.power_bar.rect = bar.get_rect()
        hud.power_bar.rect.x = pos[0] + 10
        hud.power_bar.rect.y = pos[1] + 20

    def draw_power_bar_bg( self, pos, hud ) :
        width = 102
        bar = pygame.Surface( ( int(width), 8 ) )
        bar.fill( (0,0,0) )
        hud.power_bar_bg.image = bar
        hud.power_bar_bg.dirty = 1
        hud.power_bar_bg.rect = bar.get_rect()
        hud.power_bar_bg.rect.x = pos[0] + 9
        hud.power_bar_bg.rect.y = pos[1] + 19

    def draw_orb_bar( self, pos, hud ) :
        width = 100
        bar = pygame.Surface( ( int(width), 16 ) )
        bar.fill( (0,0,0) )
        color = (0,0,0)
        for item in hud.player.character.body_handler.find_items("SpellOrb"):
            if item.types[5] == "FireOrb":
                color = (255,0,0)
            if item.types[5] == "IceOrb":
                color = (0,0,255)
            if item.types[5] == "BoltOrb":
                color = (255,255,0)

        for orb in range(1,  hud.player.character.orbs+1 ):
            pygame.draw.circle(bar, color, ((16*orb)+1,8), 8)

        hud.orb_bar.image = bar
        hud.orb_bar.dirty = 1
        hud.orb_bar.rect = bar.get_rect()
        hud.orb_bar.rect.x = pos[0] + 10
        hud.orb_bar.rect.y = pos[1] + 30

    def destroy( self ) :
        while len( self.player_list ) != 0 :
            self.player_list.remove( self.player_list[0] )
        while len( self.huds ) != 0 :
            self.huds.remove( self.huds[0] )

class PlayerHud :

    def __init__( self, player, sprite_group ) :
        self.sprite_group = sprite_group
        self.player = player
        self.orb_bar = pygame.sprite.DirtySprite()
        self.health_bar = pygame.sprite.DirtySprite()
        self.health_bar_bg = pygame.sprite.DirtySprite()
        self.power_bar = pygame.sprite.DirtySprite()
        self.power_bar_bg = pygame.sprite.DirtySprite()
        self.level_icons = pygame.sprite.DirtySprite()
        self.victory_text = pygame.sprite.DirtySprite()
        self.sprite_group.add( self.health_bar_bg )
        self.sprite_group.add( self.health_bar )
        self.sprite_group.add( self.power_bar_bg )
        self.sprite_group.add( self.power_bar )
        self.sprite_group.add( self.orb_bar )

    def update( self, scene, settings ) :

        for joystick in scene.game.player_handler.joystick_list :
            if joystick.get_name() == "Controller (XBOX 360 For Windows)" or joystick.get_name() == "Microsoft X-Box 360 pad" :
                levelup = joystick.get_button( 4 )
            else :
                levelup = joystick.get_button( 4)
            if  levelup == 1:
                index = 0
                for p in scene.game.player_handler.player_to_join_list:
                    if joystick.get_id() == p :
                        pos = ( scene.hud.hud_positions[ index ][0] * ( settings.screenSize[0] - 120 ), scene.hud.hud_positions[ index ][1] * ( settings.screenSize[1] - 40 ) )
                        bar = pygame.Surface( (220, 50 ) )
                        bar.fill( (0,255,0) )
                        img = pygame.image.load('res/img/level_up.png')
                        bar.blit(img,(0,0))
                        self.level_icons.image = bar
                        self.level_icons.dirty = 1
                        self.level_icons.rect = bar.get_rect()
                        self.level_icons.rect.x = pos[0] + 10
                        self.level_icons.rect.y = pos[1] + 50
                        self.sprite_group.add( self.level_icons )
                    index += 1
