from datetime import datetime

class Tools:
    
    def itemAge(self, target):
        now = datetime.utcnow()
        target = datetime.strptime(target, '%Y-%m-%dT%H:%M:%SZ')
        age = now-target
        if age.days > 365:
            return '{} year ago'.format(int(age.days/360))
        elif age.days > 30:
            return '{} months ago'.format(int(age.days/30))
        elif age.days:
            return '{} days ago'.format(age.days)
        elif age.seconds > 3600:
            return '{} hours ago'.format(int(age.seconds/3600))
        elif age.seconds > 60:
            return '{} minutes ago'.format(int(age.seconds/60))
        elif age.seconds:
            return '{} seconds ago'.format(age.seconds)

