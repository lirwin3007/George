class menu:

	def __init__(self, description, options):
		self.options = options
		self.description = description

	def display(self):
		print()
		print(self.description)
		print()
		print("~~~ Menu ~~~")
		counter = 1
		for option in self.options:
			print(str(counter) + "\t" + option)
			counter += 1
		print()
		print("Q\tQuit")

		selectionNotValid = True

		while selectionNotValid:
			selection = input()
			if not (selection.isdigit() or (selection != "Q" or selection != "q")):
				print("Please input a number or Q to quit")
			elif selection == "Q" or selection == "q":
				return "Quit"
			elif selection.isdigit():
				if int(selection) > len(self.options):
					print("Please input a valid number")
				else:
					return self.options[int(selection) - 1]
