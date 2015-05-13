from framework import *

class Body :
	
	def __init__( self ) :
		self.main_body = 0
		self.all_bodies = []
		self.item_slots = []
		self.joints = []
		
	def create_humanoid( self, owner, world, pos, size, filter ) :
		head = world.CreateDynamicBody(
			position=pos,
			userData=owner,
			fixedRotation=True,
			fixtures=[
				b2FixtureDef(
					shape=b2CircleShape(radius=0.3*size),
					density=10,
					filter=b2Filter(
						groupIndex = 0,
						categoryBits = filter[0],
						maskBits = filter[1]
					)
				)
			]
		)
		r_s_pos = ( pos[0], pos[1] + 0.4*size )
		right_shoulder = world.CreateDynamicBody(
			position = r_s_pos,
			fixtures=b2FixtureDef(
				filter=b2Filter(
					groupIndex = 0,
					categoryBits = filter[0],
					maskBits = filter[1]
				),
				shape=b2PolygonShape(
					box=(0.15*size, 0.15*size)
				), 
				density=5 * size
			),
		)
		right_shoulder_joint = world.CreateWeldJoint(
			bodyA=head,
			bodyB=right_shoulder,
			anchor=r_s_pos,
		)
		l_s_pos = ( pos[0], pos[1] - 0.4*size )
		left_shoulder = world.CreateDynamicBody(
			position = l_s_pos,
			fixtures=b2FixtureDef(
				filter=b2Filter(
					groupIndex = 0,
					categoryBits = filter[0],
					maskBits = filter[1]
				),
				shape=b2PolygonShape(
					box=(0.15*size, 0.15*size)
				), 
				density=5 * size
			),
		)
		left_shoulder_joint = world.CreateWeldJoint(
			bodyA=head,
			bodyB=left_shoulder,
			anchor=l_s_pos,
		)
		
		r_a_pos = ( pos[0] + 0.2*size, pos[1] + 0.5*size )
		right_arm = world.CreateDynamicBody(
			position = r_a_pos,
			fixtures=b2FixtureDef(
				filter=b2Filter(
					groupIndex = 0,
					categoryBits = filter[0],
					maskBits = filter[1]
				),
				shape=b2PolygonShape(
					box=(0.2*size, 0.1*size)
				), 
				density=5 * size
			),
		)
		right_arm_joint = world.CreateRevoluteJoint(
			bodyA=right_shoulder,
			bodyB=right_arm,
            localAnchorA=(0,0),
            localAnchorB=(0.15*size,0),
            lowerAngle=210.0 * b2_pi / 180.0,
            upperAngle=150.0 * b2_pi / 180.0,
            enableLimit=True,
		)
		l_a_pos = ( pos[0] + 0.2*size, pos[1] - 0.5*size )
		left_arm = world.CreateDynamicBody(
			position = l_a_pos,
			fixtures=b2FixtureDef(
				filter=b2Filter(
					groupIndex = 0,
					categoryBits = filter[0],
					maskBits = filter[1]
				),
				shape=b2PolygonShape(
					box=(0.2*size, 0.1*size)
				), 
				density=5 * size
			),
		)
		left_arm_joint = world.CreateRevoluteJoint(
			bodyA=left_shoulder,
			bodyB=left_arm,
            localAnchorA=(0,0),
            localAnchorB=(0.15*size,0),
            lowerAngle=210.0 * b2_pi / 180.0,
            upperAngle=150.0 * b2_pi / 180.0,
            enableLimit=True,
		)
		
		self.main_body = head
		self.all_bodies = [ head, right_shoulder, left_shoulder, right_arm, left_arm ]
		self.item_slots = [ 
			ItemSlot( right_arm, ( 0.2*size, 0 ) ), 
			ItemSlot( left_arm, ( 0.2*size, 0 ) ) 
		]
		self.joints = [ right_shoulder_joint, left_shoulder_joint, right_arm_joint, left_arm_joint ]
		return self.main_body
	
	def create_projectile( self, owner, world, pos, size, filter ) :
		head = world.CreateDynamicBody(
			position=pos,
			userData=owner,
			fixtures=[
				b2FixtureDef(
					shape=b2CircleShape(radius=0.3*size),
					density=1,
					filter=b2Filter(
						groupIndex = 0,
						categoryBits = filter[0],
						maskBits = filter[1]
					)
				)
			]
		)
		self.main_body = head
		return self.main_body
		
	def attach_item( self, item ) :
		for slot in self.item_slots :
			if slot.item == 0 :
				slot.attach_item( item )
				return True
		self.item_slots[ 0 ].detach_item()
		self.item_slots[ 0 ].attach_item( weapon )
	
	def use( self ) :
		pass
		
	def update( self, update ) :
		for slot in self.item_slots :
			slot.update( update )
	
class ItemSlot :
	
	def __init__( self, body, local_anchor ) :
		self.body = body
		self.local_anchor = local_anchor
		self.item = 0
		
	def attach_item( self, item ) :
		item.destroy_body()
		item.create_body( self.body.transform.position + self.local_anchor )
		pass
		
	def detach_item( self ) :
		pass

	def update( self, update ) :
		if self.item != 0 :
			self.item.update( update )
