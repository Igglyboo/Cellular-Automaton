Simple Cellular Automaton simulator written in Python with Pyglet

Pyglet is used for the drawing and Numpy for fast arrays

User Modifiable variables:
	width: window width
	height: window height
	cell_size: size of each cell
		width % cell_size and height % cell_size should equal 0
	born and survives, rules for the game in form B../S.. 
		B3/S23 is the classic game of life

Controls:
	Game can be paused with Enter
	While paused:
		Key I will clear the entire board
		Key O will fill the entire board
		Key P will randomize the board
		Right Arrow Key will advance the board one generation
		Left Mouse click/drag will turn a cell on
		Right Mouse click/drag will turn a cell off
		
	