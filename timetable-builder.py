from ics import Calendar
import sys
from arrow import Arrow

InputFilename = sys.argv[1]
StartDate = Arrow.strptime(sys.argv[2], '%Y-%m-%d') # See here (https://arrow.readthedocs.io/en/latest/) for correct date format
UpdatedCalendar = Calendar()

def RelocateEvent (initialEvent, offset):
	updatedEvent = initialEvent
	
	if (offset.days < 0):
		updatedEvent.begin = initialEvent.begin + offset
		updatedEvent.end = initialEvent.end + offset
	
	if (offset.days > 0):
		updatedEvent.end = initialEvent.end + offset
		updatedEvent.begin = initialEvent.begin + offset
	
	return updatedEvent
	

with open(InputFilename, "r") as f:
	originalCalendar = Calendar(f.read())
	originalEvents = originalCalendar.events
	
	earliestDate = None
	
	for event in originalEvents:
		if (not earliestDate):
			earliestDate = event.begin
			continue
		
		if (event.begin < earliestDate):
			earliestDate = event.begin
	
	offset = StartDate - earliestDate
	
	print(StartDate, earliestDate, offset)
	
	for event in originalEvents:
		updatedEvent = RelocateEvent(event, offset)
		UpdatedCalendar.events.add(updatedEvent)

with open('out.ics', 'w') as f:
    f.writelines(UpdatedCalendar.serialize_iter())
