from datetime import date

def date_is_yesterday_or_today(dateToCheck):
        today = date.today()
        yesterday = date(today.year, today.month, today.day-1)
        
        print('today is ' + str(today))
        print('yesterday is '+ str(yesterday))

        if dateToCheck.__eq__(str(today)) or dateToCheck.__eq__(str(yesterday)):
            return True
        else:
            return False