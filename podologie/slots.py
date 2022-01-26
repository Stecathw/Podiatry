from datetime import datetime, date, time


def get_slots(hours, appointments, pause, duration):
    """
    Entries :    
        hours : 
            Opening hours of the day.
            Tuples of datetime -> (starting date+time, ending date+time)
            (datetime.datetime(2022, 1, 27, 9, 0), datetime.datetime(2022, 1, 27, 17, 0))
            
        appointments : 
            existing appointments
            List of datetimes tuples
            [(datetime.datetime(2022, 1, 27, 9, 0), datetime.datetime(2022, 1, 27, 10, 0))]
        
        pause : 
            Mid day pause 
            List of datetime tuples 
            [(datetime.datetime(2022, 1, 27, 12, 0), datetime.datetime(2022, 1, 27, 13, 0))]
            
        duration : 
            duration of the choosen service
            eg: 0:30:00
        
    From entries of tuples, it creates a new TAKEN slot list of datetime tuples 
        slots = [(datetime.datetime(2022, 1, 27, 9, 0), datetime.datetime(2022, 1, 27, 9, 0)), 
                (datetime.datetime(2022, 1, 27, 9, 0), datetime.datetime(2022, 1, 27, 10, 0)), 
                (datetime.datetime(2022, 1, 27, 10, 0), datetime.datetime(2022, 1, 27, 10, 30)), 
                (datetime.datetime(2022, 1, 27, 10, 30), datetime.datetime(2022, 1, 27, 11, 0)), 
                (datetime.datetime(2022, 1, 27, 11, 0), datetime.datetime(2022, 1, 27, 11, 30)), 
                (datetime.datetime(2022, 1, 27, 12, 0), datetime.datetime(2022, 1, 27, 13, 0)), 
                (datetime.datetime(2022, 1, 27, 17, 0), datetime.datetime(2022, 1, 27, 17, 0))]
        These slots are unavailable.
    
    By looping through the unvailable slots it calculate starting and ending time of available slots in the day
        start               end
        2022-01-27 09:00:00 2022-01-27 09:00:00
        2022-01-27 10:00:00 2022-01-27 10:00:00
        2022-01-27 10:30:00 2022-01-27 10:30:00
        2022-01-27 11:00:00 2022-01-27 11:00:00
        2022-01-27 11:30:00 2022-01-27 12:00:00
        2022-01-27 13:00:00 2022-01-27 17:00:00
        
    And while start hour + duration of service <= end hour
        2022-01-27 11:30:00 + 0:30:00 = 2022-01-27 12:00:00
        it generates an available slot, and append the new tuple to available list : [(2022-01-27 11:30:00, 2022-01-27 12:00:00)...]
        
    Returns a list of available slots
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


