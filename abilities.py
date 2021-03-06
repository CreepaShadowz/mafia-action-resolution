class Ability:
	def __init__(self):
		self.caster = None
		self.executed = True
		self.success = None
		self.resolved = False
		self.modifiable = True
		self.modified_by = []
		self.actions = []
		self.return_message = ""
		self.priority = 0

	def get_components(self):
		actions = []
		modified_by = []

		for action in self.actions:
			actions.append(action.get_components())

		for action in self.modified_by:
		 	modified_by.append((action.__class__.__name__, action))

		components = {
			"caster": (self.caster.__name__(), self.caster),
			"executed": self.executed,
			"success": self.success,
			"resolved": self.resolved,
			"modifiable": self.modifiable,
			"modified_by": modified_by,
			"actions": actions,
			"return_message": self.return_message,
			"priority": self.priority
		}

		return components

	def connect_to_targets(self):
		for action in self.actions:
			action.target.targetted_by.append(self)
			if (action.target_ability == "*"):
				action.target_ability = []
				for target_ability in action.target.cast_abilities:
					action.target_ability.append(target_ability)
					target_ability.modified_by.append(self)


	def resolve(self, *ability_chain):
		print("Resolving ability: " + str(self))

		if (not ability_chain):
			ability_chain = [self]
			print("No ability chain, start of ability chain: " + str(ability_chain))
		else:
			print("Ability chain: " + str(ability_chain))

		# Resolve abilities that directly affect this ability
		for action in self.actions:
			print("Resolving action: " + str(action))
			if (self.modified_by):
				for ability in self.modified_by:
					if (ability not in ability_chain):
						print("APPENDING ABILITY TO CHAIN")
						ability_chain.append(ability)
						print("RESOLVING ABILITY")
						ability.resolve(ability_chain)
						print("POPPING ABILITY FROM CHAIN")
						ability_chain.pop()
		
		# Resolve this ability
		if (self.executed == True):
			print("Executing ability: " + str(self))
			for action in self.actions:
				print("Executing action: " + str(action))
				if (action.type == "get"):
					action.returned_value = getattr(action.target, action.component)
					self.return_message += str(self.interpret_results(action))
					self.success = True
					self.resolved = True
				elif (action.type == "alter"):
					execute = "action.target.target_ability[1][0] = " + str(action.target.new_value)
					print(execute)
					exec(execute)
					# exec("print(action.target." + action.component + ")")
					# print(action.new_value)
					# action.target.component = action.new_value
					pass
		else:
			self.return_message = "No Result"
			self.success = False
			self.resolved = True

	def interpret_results(self):
		NotImplemented


class Action:
	def __init__(self, type, target, component, *new_value):
		self.type = type

		if (isinstance(target, tuple)):
			self.target = target[0]
			self.target_ability= target[1]
		else:
			self.target = target
			self.target_ability = None

		self.component = component

		if new_value:
			self.new_value = new_value
		else:
			self.new_value = None
		self.returned_value = None

	def get_components(self):
		components = {
			"action": (self.__class__.__name__, self),
			"type": self.type,
			"target": (self.target.__name__(), self.target),
			"target_ability": self.target_ability,
			"component": self.component,
			"new_value": self.new_value,
			"returned_value": self.returned_value
		}
		return components