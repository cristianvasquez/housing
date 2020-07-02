class Stats:
    def __init__(self):
        self.people_stats = {}
        self.people_stats_last_index = 0

        self.general_stats = {}
        self.general_stats_last_index = 0

        self.example_house_stats = {}
        self.example_house_stats_last_index = 0

    def add_people_stats_record(self, record):
        self.people_stats[self.people_stats_last_index] = record
        self.people_stats_last_index += 1

    def add_general_stats_record(self, record):
        self.general_stats[self.general_stats_last_index] = record
        self.general_stats_last_index += 1

    def add_example_house_stats_record(self, record):
        self.example_house_stats[self.example_house_stats_last_index] = record
        self.example_house_stats_last_index += 1