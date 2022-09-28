from workSpace import BaseWorkSpace
from onlineBooking import Booking
from location import Location
from AIConsult import AI
from edesk import Edesk
from pushMessage import PushMessage

def whichJob(info,event):
    match info["workSpace"]:
        case 1:
            ai = AI(event)
            info = ai.action(info)
        case 2:
            ed = Edesk(event)
            info = ed.action(info)
        case 3:
            booking = Booking(event)
            info = booking.action(info)
        case 4:
            loc = Location(event)
            info =loc.action(info)
        case 5:
            pus = PushMessage(event)
            info = pus.action(info)
    return info