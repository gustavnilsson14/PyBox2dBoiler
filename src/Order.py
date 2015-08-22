import random

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
    
    def __init__( self, scene, game ) :
        self.scene = scene
        self.game = game
        self.spawn_list = []
        self.minions = []
        self.frames_per_action = 1
        self.spawn_rate = 120
        self.max_enemies = 12

    def order_attack( self, minion, target ) :
        self.scene.orders.append( AttackOrder( [ minion ], target ) )
        
    def update( self ) :
        total_enemies = 0
        for spawn in self.spawn_list :
            if len( spawn.entities ) == 0 :
                self.spawn_list.remove( spawn )
                continue
            total_enemies += len( spawn.entities )
        if total_enemies == 0 :
            self.scene.defeat( GROUP_AI )
        self.sort_dead_minions()
        if self.game.time % self.spawn_rate == 0 and len( self.minions ) < self.max_enemies :
            print "TRY TO SPAWN"
            while random.choice( self.spawn_list ).spawn_enemy() == 0 :
                pass
        if len( self.game.player_handler.player_list ) == 0 :
            return 0
        if len( self.minions ) == 0 : 
            return 0
        if self.game.time % self.frames_per_action == 0 :
            minion = random.choice( self.minions )
            target = random.choice( self.game.player_handler.player_list ).character
            self.order_attack( minion, target )
    
    def add_entity( self, entity ) :
        if entity in self.minions :
            return 0
        self.minions += [ entity ]
        
    def sort_dead_minions( self ) :
        for minion in self.minions :
            if minion.alive == False :
                self.minions.remove( minion )
        
    def add_spawn( self, spawn ) :
        self.spawn_list += [ spawn ]
        
        