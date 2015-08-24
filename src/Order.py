import random
from Constants import *
from Enemy import *

class Order :
    
    def __init__( self, unit_list ) :
        self.interruptable = True
        for unit in unit_list :
            if unit.set_order( self ) == False :
                unit_list.remove( unit )
        self.unit_list = unit_list
        
    def add_unit( self, unit ) :
        if self.unit_list.__contains__( unit ) :
            return False
        self.unit_list.append( unit )
        return True
        
    def remove_unit( self, unit ) :
        if self.interruptable == True :
            return False
        if self.unit_list.__contains__( unit ) :
            self.unit_list.remove( unit )
            return True
        return False
        
    def destroy( self ) :
        for unit in self.unit_list :
            unit.current_order = 0
        self.unit_list = 0
        
    def Step( self ) :
        pass
        
class MoveOrder( Order ) :
    
    def __init__( self, unit_list, goal ) :
        Order.__init__( self, unit_list )
        self.goal = goal
    
    def Step( self ) :
        Order.Step( self )
        for unit in self.unit_list :
            unit.move( self.goal )
          
class AttackOrder( Order ) :
    
    def __init__( self, unit_list, target ) :
        for unit in unit_list :
            if unit.set_current_item( 'weapon' ) :
                continue
            unit_list.remove( unit )
        Order.__init__( self, unit_list )
        self.target = target
    
    def Step( self ) :
        Order.Step( self )
        if self.target.alive == False :
            self.unit_list = []
        for unit in self.unit_list :
            if unit.aim( self.target.body.transform.position ) :
                if unit.use_current_item( self.target ) :
                    unit.stop()
                    continue
                unit.move( self.target.body.transform.position )
                continue
            unit.move( self.target.body.transform.position )
            continue
    
class PatrolOrder( Order ) :
    
    def __init__( self, unit_list, start, goal ) :
        Order.__init__( self, unit_list )
        self.start = start
        self.goal = goal
    
    def Step( self ) :
        Order.Step( self )
        for unit in self.unit_list :
            if unit.current_tile == self.start :
                unit.move( self.goal )
            else :
                unit.move( self.start )

class AI :
    
    def __init__( self, scene, game, level = 0 ) :
        self.scene = scene
        self.game = game
        self.spawn_list = []
        self.waves = []
        self.players = len( self.game.player_handler.player_list ) + 1
        for int in range( 0, 2 + level ) :
            self.waves += [ Wave( self, self.spawn_list, int + 1 ) ]
        self.minions = []
        self.frames_per_action = 200 - ( level * 10 )
        self.spawn_rate = 300 - ( level * 10 )
        self.max_enemies = 5 + ( level * 2 )

    def order_attack( self, minion, target ) :
        self.scene.orders.append( AttackOrder( [ minion ], target ) )
        
    def update( self ) :
        self.sort_dead_minions()
        self.control_minions()
        if len( self.waves ) == 0 :
            self.scene.defeat( DEFEAT_GROUP_AI )
            return
        wave = self.waves[0]
        if wave.running == False :
            print "STARTING WAVE", wave.index
            wave.start()
        if wave.wave_start_pause() == 0 :
            return
        if self.game.time % ( self.spawn_rate - ( wave.index * 10 ) ) == 0 and len( self.minions ) < self.max_enemies :
            for i in range( 0, self.players ) :
                spawn = wave.get_spawn()
                if spawn == 0 :
                    if len( self.minions ) == 0 :
                        self.waves.pop(0)
                    return
                self.add_entity( wave, spawn )
            
    def control_minions( self ) :
        if len( self.game.player_handler.player_list ) == 0 :
            return 0
        if len( self.minions ) == 0 : 
            return 0
        if self.game.time % self.frames_per_action == 0 :
            for i in range( 0, self.players ) :
                player_list = self.game.player_handler.player_list
                minion = random.choice( self.minions )
                target = self.pick_vulnerable_target( minion, player_list )
                if target == 0 :
                    target = random.choice( self.game.player_handler.player_list )
                target = target.character
                self.order_attack( minion, target )
        else :
            for minion in self.minions :
                if minion.current_order == 0 :
                    for player in self.game.player_handler.player_list :
                        if get_distance_between_points( minion.body.transform.position, player.character.body.transform.position) < 8 :
                            self.order_attack( minion, player.character )
                            
    def pick_vulnerable_target( self, minion, player_list ) :
        max_tries = 10
        while max_tries > 0 :
            max_tries -= 0
            player = random.choice( player_list )
            if len( player.character.immunities ) == 0 :
                return player
            if player.character.immunities[0] != minion.immunities[0] :
                return player
            return 0
    
    def add_entity( self, wave, spawn ) :
        entity = wave.get_entity()
        entity = entity( self.scene, spawn.position )
        self.entity = entity
        self.scene.add_entity( entity )
        self.minions += [ entity ]
        
    def sort_dead_minions( self ) :
        for minion in self.minions :
            if minion.alive == False :
                self.minions.remove( minion )
        
    def add_spawn( self, spawn ) :
        self.spawn_list += [ spawn ]
        
    def remove_spawn( self, spawn ) :
        if spawn in self.spawn_list :
            self.spawn_list.remove( spawn )
            
class Wave :
    
    def __init__( self, ai, spawns, index ) :
        self.spawns = spawns
        self.ai = ai
        self.running = False
        self.index = index
        self.wave_pause = 300
        self.spawn_resets = index + ai.players - 3
        self.entities_available = [FireMage,IceMage,BoltMage,FireMage,IceMage,BoltMage,ColorMage]
        if self.index == 2 :
            self.entities_available = [FireMage,IceMage,BoltMage,FireMage,IceMage,BoltMage,FireMage,IceMage,BoltMage,FireMage,IceMage,BoltMage,ColorMage,ColorMage,WhiteMage]
        if self.index == 3 :
            self.entities_available = [FireMage,IceMage,BoltMage,ColorMage,ColorMage,ColorMage,ColorMage,WhiteMage,WhiteMage]
        self.reset_entities()
        
    def get_entity( self ) :
        if len( self.current_entity_list ) == 0 :
            self.reset_entities()
        entity = self.current_entity_list.pop()
        return entity 
        
    def reset_entities( self ) :
        self.current_entity_list = self.entities_available[:]
        
    def start( self ) :
        self.running = True
        for spawn in self.spawns :
            spawn.empty = False
            
    def wave_start_pause( self ) :
        if self.wave_pause == 0 :
            return 1
        self.wave_pause -= 1
        return 0
        
    def spawn_reset( self ) :
        if self.spawn_resets == 0 :
            return 0 
        for spawn in self.spawns :
            spawn.empty = False
        self.spawn_resets -= 1
        return self.get_spawn()
        
    def get_spawn( self ) :
        random.shuffle( self.spawns )
        for spawn in self.spawns :
            if spawn.empty == True :
                continue
            spawn.empty = True
            return spawn
        return self.spawn_reset()
        
        