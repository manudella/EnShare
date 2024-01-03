import numpy as np
import random

# Define House class
class House:
    def __init__(self, house_id, solar_panel=False):
        self.house_id = house_id
        self.solar_panel = solar_panel
        self.consumption_model = self.generate_energy_consumption()
        self.consumption_graph = self.consumption_model
        self.type = None
    def generate_energy_consumption(self):
        consumption = []
        for i in range(24*4):
            consumption.append(random.choice((-2, -1, 0, 1, 2)))
        print(consumption)
        return consumption

# Define Neighborhood class
class Neighborhood:
    def __init__(self):
        self.houses = []
        self.distance_matrix = self.calculate_distance_matrix()
        self.timeslots = [i for i in range(24*4)]
        self.distance_price = 0.0001
        self.transfer_agenda = {'0': list(), '1': list(), '2': list(), '3': list(), '4': list(), '5': list(), '6': list(), '7': list(),
                                '8': list(), '9': list(), '10': list(), '11': list(), '12': list(), '13': list(), '14': list(), '15': list(),
                                '16': list(), '17': list(), '18': list(), '19': list(), '20': list(), '21': list(), '22': list(), '23': list(),
                                '24': list(), '25': list(), '26': list(), '27': list(), '28': list(), '29': list(), '30': list(), '31': list(),
                                '32': list(), '33': list(), '34': list(), '35': list(), '36': list(), '37': list(), '38': list(), '39': list(),
                                '40': list(), '41': list(), '42': list(), '43': list(), '44': list(), '45': list(), '46': list(), '47': list(),
                                '48': list(), '49': list(), '50': list(), '51': list(), '52': list(), '53': list(), '54': list(), '55': list(),
                                '56': list(), '57': list(), '58': list(), '59': list(), '60': list(), '61': list(), '62': list(), '63': list(),
                                '64': list(), '65': list(), '66': list(), '67': list(), '68': list(), '69': list(), '70': list(), '71': list(),
                                '72': list(), '73': list(), '74': list(), '75': list(), '76': list(), '77': list(), '78': list(), '79': list(),
                                '80': list(), '81': list(), '82': list(), '83': list(), '84': list(), '85': list(), '86': list(), '87': list(),
                                '88': list(), '89': list(), '90': list(), '91': list(), '92': list(), '93': list(), '94': list(), '95': list()}

    def add_house(self, house):
        self.houses.append(house)

    def calculate_distance_matrix(self):
        # Simulate distances between houses (as an example, random distances)
        num_houses = len(self.houses)
        distance_matrix = np.random.uniform(0.1, 0.9, size=(num_houses, num_houses))
        np.fill_diagonal(distance_matrix, 1000)  # Set diagonal elements to 0
        print(distance_matrix)
        return distance_matrix

    def redistribute_surplus_energy(self):
        for time_slot in self.timeslots:
            print('Time slot: ')
            print(time_slot)
            self.find_senders_and_receivers_at_time_slot(time_slot)
            self.redistribute_surplus_energy_at_time_slot(time_slot)


    def find_senders_and_receivers_at_time_slot(self, time_slot):
        for house in self.houses:
            if house.consumption_graph[time_slot] < 0:
                house.type = 'sender'
            elif house.consumption_graph[time_slot] > 0:
                house.type = 'receiver'
            else:
                house.type = 'complete'

    def redistribute_surplus_energy_at_time_slot(self, time_slot):
        senders = [house for house in self.houses if house.type == 'sender']
        for sender in senders:
            while True:
                surplus = -(sender.consumption_graph[time_slot])
                if surplus <= 0:
                    break
                receivers = [house for house in self.houses if house.type == 'receiver']
                nearest_receiver = self.find_nearest_receiver(sender, receivers, time_slot)
                if nearest_receiver == None:
                    break
                else:
                    self.transfer_energy(sender, nearest_receiver, surplus, time_slot)

    def find_nearest_receiver(self, sender, receivers, time_slot):
        x=len(self.houses)
        sender_index = self.houses.index(sender)
        distances = self.distance_matrix[sender_index]
        dis_copy = distances.copy()
        nearest_receiver = None
        while x > (len(self.houses)-len(receivers)):
            nearest_receiver_index = np.argmin(dis_copy)
            if dis_copy[nearest_receiver_index] == 1000:
                nearest_receiver = None
                break
            else:
                nearest_receiver = self.houses[nearest_receiver_index]
                if nearest_receiver.consumption_graph[time_slot] > 0:
                    break
                else:
                    nearest_receiver = None
                    dis_copy[nearest_receiver_index] = 1000
                    x = x-1

        return nearest_receiver

    def transfer_energy(self, house_sender, house_receiver, surplus, time_slot):
        print('surplus')
        print(surplus)
        needs = house_receiver.consumption_graph[time_slot]
        print('needs')
        print(needs)
        distance = self.distance_matrix[house_sender.house_id][house_receiver.house_id]
        difference = needs - (surplus - (self.distance_price * distance))

        if difference < 0:
            house_receiver.consumption_graph[time_slot] = float(0)
            house_sender.consumption_graph[time_slot] = difference - (self.distance_price * distance)
            tranfered = needs + (self.distance_price * distance)
            time_slot_str = str(time_slot)
            print("diff negativa")
            print((house_sender.house_id, house_receiver.house_id, tranfered))
            self.transfer_agenda[time_slot_str].append((house_sender.house_id, house_receiver.house_id, tranfered))
            print(house_sender.consumption_graph[time_slot])
            print(house_receiver.consumption_graph[time_slot])

        elif difference > 0:
            house_sender.consumption_graph[time_slot] = float(0)
            tranfered = surplus
            house_receiver.consumption_graph[time_slot] = difference
            time_slot_str = str(time_slot)
            print("diff positiva")
            print((house_sender.house_id, house_receiver.house_id, tranfered))
            self.transfer_agenda[time_slot_str].append((house_sender.house_id, house_receiver.house_id, tranfered))
            print(house_sender.consumption_graph[time_slot])
            print(house_receiver.consumption_graph[time_slot])


# Example usage:
# Create houses in the neighborhood
house0 = House(0)
house1 = House(1)
house2 = House(2)
house3 = House(3)
house4 = House(4)
house5 = House(5)
house6 = House(6)
house7 = House(7)
house8 = House(8)
house9 = House(9)

# Add houses to the neighborhood
neighborhood = Neighborhood()
neighborhood.add_house(house0)
neighborhood.add_house(house1)
neighborhood.add_house(house2)
neighborhood.add_house(house3)
neighborhood.add_house(house4)
neighborhood.add_house(house5)
neighborhood.add_house(house6)
neighborhood.add_house(house7)
neighborhood.add_house(house8)
neighborhood.add_house(house9)

# Simulate redistribution of surplus energy
neighborhood.distance_matrix = neighborhood.calculate_distance_matrix()
print(neighborhood.distance_matrix)
neighborhood.redistribute_surplus_energy()
print(neighborhood.transfer_agenda)
