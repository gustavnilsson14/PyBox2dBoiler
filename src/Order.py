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
