class Package:
    def __init__(self, id, address, city, zip, deadline, mass):
        self.id = id
        self.address = address
        self.city = city
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.delivery_status = "Not Delivered"
        self.time_delivered = None