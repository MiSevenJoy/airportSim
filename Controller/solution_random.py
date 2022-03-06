import random


def schedule_vehicle(vehicle_avai_group):
    vehicle = random.choice(vehicle_avai_group.sprites())
    return vehicle

def train(reward):
    return 0