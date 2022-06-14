class Room(object):

    def __init__(self, room_id, name):
        self.id = room_id
        self.name = name
        self.students = []

    def __str__(self):
        return f"{self.id} {self.name}"
