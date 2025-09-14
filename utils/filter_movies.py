def clean_year(year_value):
    """Take only the first 4 digits if year looks like '1997–' """
    year_str = str(year_value)
    if year_str[:4].isdigit():
        return int(year_str[:4])


def min_rating():
    while True:
        min_rating = input("Enter min rating (leave blank if you want None): ")
        if not min_rating:
            return None
        try:
            min_rating = float(min_rating)
            if min_rating < 0 or min_rating > 10:  # keine negativen Ratings
                print("Rating cannot be negative or greater than 10.")
                continue
            return min_rating

        except ValueError:
            print("Please enter a valid number for rating.")

def start_year():
    while True:
        start_year = input("Enter start year (leave blank if you want None): ")
        if not start_year:
            return None

        try:
            start_year = int(start_year)
            if start_year < 0:  # keine negativen Jahreszahlen
                print("Year cannot be negative.")
                continue
            return start_year

        except ValueError:
            print("Please enter a valid year.")

def end_year():
    while True:
        end_year = input("Enter end year (leave blank if you want None): ")
        if not end_year:
            return None

        try:
            end_year = int(end_year)
            if end_year < 0:
                print("Year cannot be negative.")
                continue
            return end_year
        except ValueError:
            print("Please enter a valid year.")



