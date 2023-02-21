"""Function to classify sensor position"""


def update_loadreading_at_position(location, load, Upper_North, Upper_South, Upper_East,
 Upper_West, Lower_North, Lower_South, Lower_East, Lower_West):
	"""
	Takes: 
	
	'location': string specifying the location of a load sensor, 
	with the first word specifying whether sensor is in the Upper 
	or Lower position in its eyebuckle mount, and the second word
	specifying its cardinal location. E.g., Upper North or Lower West. 

	'load': float value in kilograms specifying load reading from 
	sensor at location. 

	Returns: None, but updates the global variable value corresponding 
	to the load reading from the sensor at location. """
	if location == 'Upper North' or location == 'upper north':
		Upper_North.set(load)
	elif location == 'Upper South' or location == 'upper south':
		Upper_South.set(load)
	elif location == 'Upper East' or location == 'upper east':
		Upper_East.set(load)
	elif location == 'Upper West' or location == 'upper west':
		Upper_West.set(load)
	elif location == 'Lower North' or location == 'lower north':
		Lower_North.set(load)
	elif location == 'Lower South' or location == 'lower south':
		Lower_South.set(load)
	elif location == 'Lower East' or location == 'lower east':
		Lower_East.set(load)
	elif location == 'Lower West' or location == 'lower west':
		Lower_West.set(load)

	return None