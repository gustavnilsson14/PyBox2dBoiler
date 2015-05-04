class Order :
    
    def __init__( self, units ) :
        self.interruptable = True
        for unit in units :
            if unit.set_order( self ) == False :
                units.remove( unit )
        self.units = units
        
        
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
        for unit in self.units :
            unit.current_order = 0
        self.units = 0
        
    def Step( self ) :
        pass
        
class MoveOrder( Order ) :
    
    def __init__( self, units, goal ) :
        Order.__init__( self, units )
        self.goal = goal
    
    def Step( self ) :
        Order.Step( self )
        for unit in self.units :
            unit.move( self.goal )
