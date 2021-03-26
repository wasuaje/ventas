from menuapp.models import *



def is_in_menu_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Menu').count() == 1        
    return False     