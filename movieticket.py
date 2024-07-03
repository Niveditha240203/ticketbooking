import mysql.connector
import datetime
import smtplib

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="besantmoviebooking_db"
)
mycursor = mydb.cursor()

class MovieBooking:
    def __init__(self):
        self.tickets_booked = 0

    def book_tickets(self):
        self.tickets_booked += 1
        print("Ticket booked successfully!")
        print(f"Total tickets booked: {self.tickets_booked}")

    def book_ticket(self, movie_name, name, seat_availability, show_time):
        sql = "INSERT INTO Bookings (movie_name, name, seat_availability, show_time) VALUES (%s, %s, %s, %s)"
        values = (movie_name, name, seat_availability, show_time)
        mycursor.execute(sql, values)
        mydb.commit()
        print(f"Booking confirmed for {name} for movie {movie_name}.")

    def send_email(self, recipient_email):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("niveditha240203@gmail.com", "ksdq fjuf pzbv nmkx")
            message = "Your ticket has been booked successfully"
            s.sendmail("niveditha240203@gmail.com", recipient_email, message)
            s.quit()
            print("Mail sent successfully")
        except Exception as e:
            print(f"Your mail was not sent! Error: {e}")

    def view_bookings(self):
        mycursor.execute("SELECT * FROM Bookings")
        result = mycursor.fetchall()
        for booking in result:
            print(booking)

    def cancel_booking(self, booking_id):
        sql = "DELETE FROM Bookings WHERE id = %s"
        mycursor.execute(sql, (booking_id,))
        mydb.commit()
        print(f"Booking with ID {booking_id} has been cancelled.")

    
    def check_seat_availability(self, movie_name, show_time):
        sql = "SELECT SUM(seat_availability) FROM Bookings WHERE movie_name = %s AND show_time = %s"
        mycursor.execute(sql, (movie_name, show_time))
        result = mycursor.fetchone()
        return result

    def search_booking(self, search):
        sql = "SELECT * FROM Bookings WHERE name LIKE %s OR movie_name LIKE %s"
        search = f"%{search}%"
        mycursor.execute(sql, (search, search))
        result = mycursor.fetchall()
        for booking in result:
            print(booking)

def main():
    mb = MovieBooking()
    print("Movie Ticket Booking")
    print("1. Book a Movie")
    print("2. View All Bookings")
    print("3. Cancel Booking")
    print("4. Search Booking")
    choice = input("Enter your choice: ")

    if choice == '1':
        print("Available Movies")
        print("1. Star")
        print("2. Kalki")
        print("3. Garudan")
        movie_choice = input("Enter your movie choice: ")
        movies = {'1': 'Star', '2': 'Kalki', '3': 'Garudan'}

        if movie_choice in movies:
            movie_name = movies[movie_choice]
            print(f"Yes! {movie_name} is available")
            name = input("Enter your name: ")
            seat_availability = int(input("Enter number of seats: "))
            show_time = input("Enter show time (HH:MM:SS): ")
            current_seats = mb.check_seat_availability(movie_name, show_time)
            if current_seats + seat_availability <= 100:  # Assuming 100 seats per show
                current_time = datetime.datetime.now()
                print(f"You booked the movie at this time: {current_time}")
                mb.book_ticket(movie_name, name, seat_availability, show_time)
                recipient_email = input("Enter your email: ")
                mb.send_email(recipient_email)
                mb.book_tickets()
            else:
                print("Not enough seats available for this show time.")
        else:
            print(f"This movie '{movie_choice}' is unavailable")
    elif choice == '2':
        mb.view_bookings()
    elif choice == '3':
        booking_id = int(input("Enter booking ID to cancel: "))
        mb.cancel_booking(booking_id)
    elif choice == '4':
        search = input("Enter name or movie to search for: ")
        mb.search_booking(search)
    else:
        print("Enter a valid number!")

main()
mycursor.close()
mydb.close()



