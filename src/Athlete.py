from src.DataAcquisition import convert_to_seconds


class Athlete:
    full_name = ""
    swim_time = None
    bike_time = None
    age_group = None
    run_time = None

    def __init__(self, swim_time, bike_time, run_time):
        self.swim_time = convert_to_seconds(swim_time)
        self.bike_time = convert_to_seconds(bike_time)
        self.run_time = convert_to_seconds(run_time)