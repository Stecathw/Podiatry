from datetime import datetime, date, time


def get_slots(hours, appointments, pause, duration):
    """
    Return a list of available slots
    """
    available = []
    slots = sorted([(hours[0], hours[0])] + appointments + pause + [(hours[1], hours[1])])
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        assert start <= end, "Cannot attend all appointments"
        while start + duration <= end:
            available.append("{:%H:%M} - {:%H:%M}".format(start, start + duration))
            start += duration
    return available
    
    
def day_hours(dt, start, end):    
    dt= dt.split('-')
    day = int(dt[0])
    month = int(dt[1])
    year = int(dt[2])
    #print(year, month, day)
    hours = (datetime.combine(date(year, month, day), time(start)), datetime.combine(date(year, month, day), time(end)))    
    return hours

def day_pause(dt, start, end):
    dt = dt.split('-')
    day = int(dt[0])
    month = int(dt[1])
    year = int(dt[2])
    #print(year, month, day)
    pause = [(datetime.combine(date(year, month, day), time(start)), datetime.combine(date(year, month, day), time(end)))]    
    return pause


