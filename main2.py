import pandas
from abc import ABC, abstractmethod

df = pandas.read_csv("hotels.csv", dtype={"id": str})


class Hotel:
    watermark = "The Real Estate Company"
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    @classmethodabc
    def get_hotel_count(cls, data):
        return len(data)

    def __eq__(self, other):
        if self.hotel_id == other.hotel_id:
            return True


# Must use generate method for every class using Ticket
class Ticket(ABC):

    @abstractmethod
    def generate(self):
        pass


class ReservationTicket(Ticket):
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are you booking data:
        Name: {self.the_customer_name}
        Hotel name: {self.hotel.name}
        """
        return content

    @property
    def the_customer_name(self):
        name = self.customer_name
        name = name.title()
        return name

    @staticmethod
    def convert(amount):
        amount = amount * 1.2
        return amount



hotel1 = Hotel(hotel_id="134")
print(Hotel.get_hotel_count(data=df))

ticket = ReservationTicket(customer_name=" gustavo lopez ", hotel_object=hotel1)
print(ticket.generate())

converted = ReservationTicket.convert(10)
print(converted)