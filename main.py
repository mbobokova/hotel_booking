import pandas


df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        pass

    def book(self):
        """Book a hotel by changing its availability to 'no'"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object
        pass

    def generate(self):
        content = f"""
        Dear {self.customer_name},
        Thank you for your reservation at {self.hotel.name}
        There are details of your reservation:
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        """
        return content


class ReservationSpaTicket(ReservationTicket):
    def generate(self):
        content = f"""
        Dear {self.customer_name},
        Thank you for your SPA reservation at hotel {self.hotel.name}
        There are details of your reservation:
        Name: {self.customer_name}
        Spa location: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True


# Main functionality
print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="5678")
    if credit_card.validate(expiration="12/28", holder="JANE SMITH", cvc="456"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
            add_spa = input("Do you want to book a spa package? yes / no")
            if add_spa == "yes":
                spa_ticket = ReservationSpaTicket(customer_name=name, hotel_object=hotel)
                print(spa_ticket.generate())

            elif add_spa == "no":
                print("Your reservation is without SPA extension")
            else:
                print("Your answer was not recognize")
        else:
            print("Credit card authentication failed")
    else:
        print("There is some problems with payment")

else:
    print("Hotel is not available")
