###########################
# 6.0002 Problem Set 1a: Space Cows
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import json

# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    cows = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            name, weight = line.split(',')
            cows[name] = int(weight.strip())
    return cows


cows_data = load_cows('./ps1_cow_data.txt')
# Problem 2


def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    trips = []
    cow_list = sorted(((value, key)
                      for (key, value) in cows.items()), reverse=True)
    for cow in cow_list:
        if (cow[0] > limit):
            cow_list.remove(cow)
    cow_list_copy = cow_list.copy()

    while cow_list_copy:
        current_weight = 0
        trip = []
        for cow in cow_list:
            if cow in cow_list_copy and current_weight + cow[0] <= limit:
                # trip.append(cow)
                trip.append(cow[1])
                current_weight += cow[0]
                cow_list_copy.remove(cow)
        trips.append(trip)
    return trips


#print(greedy_cow_transport(cows_data, 10))
# Problem 3


def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    def is_valid_shipment(trip):
        weight = 0
        for cow in trip:
            weight += cow[1]
            if weight > limit:
                return False
        return True

    def is_valid_partition(partition):
        for trip in partition:
            if not is_valid_shipment(trip):
                return False
        return True
    cow_list = cows.items()
    partitions = get_partitions(cow_list)
    valid_partitions = []
    for partition in partitions:
        if is_valid_partition(partition):
            valid_partitions.append(partition)
    sorted_valid_partitions = sorted(valid_partitions, key=len)
    final_list = []
    for trip in sorted_valid_partitions[0]:
        t = []
        for cow in trip:
            t.append(cow[0])
        final_list.append(t)
    return final_list


# print(brute_force_cow_transport(cows_data))

# Problem 4


def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    start = time.perf_counter()
    # code to be timed
    greedy_cow_transport(cows_data)
    end = time.perf_counter()
    print("greedy_cow_transport(cows1) time")
    greedy_time = end - start
    print(greedy_time)
    start = time.perf_counter()
    # code to be timed
    brute_force_cow_transport(cows_data)
    end = time.perf_counter()
    brute_time = end - start
    print("brute_force_cow_transport(cows1) time")
    print(brute_time)
    if brute_time > greedy_time:
        difference = brute_time - greedy_time
        print("brute force algorithm took longer")
        print("time difference was", difference)
    else:
        difference = greedy_time - brute_time
        print("greedy algorithm took longer")
        print("time difference was", difference)


compare_cow_transport_algorithms()
