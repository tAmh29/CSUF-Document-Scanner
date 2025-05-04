import time

def merge_sort(flights):

    if len(flights) > 1:
        mid = len(flights) // 2 # Find the middle index
        left_half = flights[:mid] #Divide list into halves
        right_half = flights[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][1] < right_half[j][1]:
                flights[k] = left_half[i]
                i += 1
            else:
                flights[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            flights[k] = left_half[i]
            i += 1
            k += 1
            
        while j < len(right_half):
            flights[k] = right_half[j]
            j += 1
            k += 1

def merge_sort_name(strings):
    if len(strings) > 1:
        mid = len(strings) // 2
        left_half = strings[:mid]
        right_half = strings[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                strings[k] = left_half[i]
                i += 1
            else:
                strings[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            strings[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            strings[k] = right_half[j]
            j += 1
            k += 1


""" def merge_sort_dict_values(flights):

    if len(flights) > 1:
        mid = len(flights) // 2 # Find the middle index
        left_half = flights[:mid] #Divide list into halves
        right_half = flights[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][1] < right_half[j][1]:
                flights[k] = left_half[i]
                i += 1
            else:
                flights[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            flights[k] = left_half[i]
            i += 1
            k += 1
            
        while j < len(right_half):
            flights[k] = right_half[j]
            j += 1
            k += 1

def sort_dict_by_value(d):
    items = list(d.items())         # Convert dict to list of tuples
    merge_sort(items)   # Sort the list by value
    print(items)
    return dict(items)              # Convert back to dict (ordered since Python 3.7+) """

# Take user input
""" num_flights = int(input("Enter number of flights: "))
flights = []
for _ in range(num_flights):
    flight_no = input("Enter flight number: ")
    dep_time = int(input(f"Enter departure time for {flight_no}: "))
    flights.append((flight_no, dep_time))

merge_sort(flights)
print("Flights sorted by departure time:", flights) """









    

