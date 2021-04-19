class LightTracker(object):

    def __init__(self):
        self.tracked_light_uuids = set()
        self.light_information_map = dict() # uuid to database object

    def check_is_tracked(self, uuid):
        return uuid in self.tracked_light_uuids
    
    def add_as_tracked(self, uuid: str, info)