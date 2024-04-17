import random
import heapq
import statistics

class Device:
    def __init__(self, name, failure_rate, repair_time):
        self.name = name
        self.failure_rate = failure_rate
        self.repair_time = repair_time
        self.is_working = True
        self.failure_time = 0
    
    def __lt__(self, other):
        return self.failure_time < other.failure_time
    
    def simulate_failure(self, current_time):
        self.is_working = False
        self.failure_time = current_time + random.expovariate(self.failure_rate)
    
    def simulate_repair(self, current_time):
        self.is_working = True
        self.failure_time = 0
        return current_time + random.expovariate(1 / self.repair_time)

class Person:
    def __init__(self, name, sadness_rate, recovery_time):
        self.name = name
        self.sadness_rate = sadness_rate
        self.recovery_time = recovery_time
        self.is_sad = False
        self.sadness_time = 0
    
    def __lt__(self, other):
        return self.sadness_time < other.sadness_time
    
    def simulate_sadness(self, current_time):
        self.is_sad = True
        self.sadness_time = current_time + random.expovariate(self.sadness_rate)
    
    def simulate_recovery(self, current_time):
        self.is_sad = False
        self.sadness_time = 0
        return current_time + random.expovariate(1 / self.recovery_time)

class Simulation:
    def __init__(self, devices, persons, duration):
        self.devices = devices
        self.persons = persons
        self.duration = duration
        self.current_time = 0
        self.events = []

    def initialize(self):
        for device in self.devices:
            device.simulate_failure(0)
            heapq.heappush(self.events, (device.failure_time, device))
        for person in self.persons:
            person.simulate_sadness(0)
            heapq.heappush(self.events, (person.sadness_time, person))

    def run(self):
        while self.current_time < self.duration:
            if not self.events:
                break
            
            event_time, entity = heapq.heappop(self.events)
            self.current_time = event_time
            
            if isinstance(entity, Device):
                if entity.is_working:
                    repair_time = entity.simulate_repair(self.current_time)
                    heapq.heappush(self.events, (repair_time, entity))
                else:
                    entity.simulate_failure(self.current_time)
                    heapq.heappush(self.events, (entity.failure_time, entity))
            elif isinstance(entity, Person):
                if entity.is_sad:
                    recovery_time = entity.simulate_recovery(self.current_time)
                    heapq.heappush(self.events, (recovery_time, entity))
                else:
                    entity.simulate_sadness(self.current_time)
                    heapq.heappush(self.events, (entity.sadness_time, entity))

    def calculate_failure_stats(self):
        failure_times = [device.failure_time for device in self.devices if not device.is_working]
        if failure_times:
            mean_failure_time = statistics.mean(failure_times)
            max_failure_time = max(failure_times)
            return mean_failure_time, max_failure_time
        else:
            return 0, 0

    def calculate_sadness_stats(self):
        sadness_times = [person.sadness_time for person in self.persons if person.is_sad]
        if sadness_times:
            mean_sadness_time = statistics.mean(sadness_times)
            max_sadness_time = max(sadness_times)
            return mean_sadness_time, max_sadness_time
        else:
            return 0, 0

device_parameters = [
    {"name": "Device 1", "failure_rate": 0.1, "repair_time": 5},
    {"name": "Device 2", "failure_rate": 0.05, "repair_time": 8},
    {"name": "Device 3", "failure_rate": 0.07, "repair_time": 6}
]
person_parameters = [
    {"name": "Person 1", "sadness_rate": 0.05, "recovery_time": 10},
    {"name": "Person 2", "sadness_rate": 0.03, "recovery_time": 12}
]
simulation_duration = 100

devices = [Device(**params) for params in device_parameters]
persons = [Person(**params) for params in person_parameters]

sim = Simulation(devices, persons, simulation_duration)
sim.initialize()
sim.run()

mean_failure_time, max_failure_time = sim.calculate_failure_stats()
print(f"Mean failure time: {mean_failure_time:.2f}")
print(f"Max failure time: {max_failure_time:.2f}")

mean_sadness_time, max_sadness_time = sim.calculate_sadness_stats()
print(f"Mean sadness time: {mean_sadness_time:.2f}")
print(f"Max sadness time: {max_sadness_time:.2f}")
