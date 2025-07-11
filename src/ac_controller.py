class ACController:
    def __init__(self, outlet, thermometer, min_temp, max_temp):
        self.outlet = outlet
        self.thermometer = thermometer
        self.min_temp = min_temp
        self.max_temp = max_temp

    def turn_on(self):
        self.outlet.power_on()

    def turn_off(self):
        self.outlet.power_off()

    def check_temperature(self):
        current_temp = self.thermometer.get_temperature()
        if current_temp < self.min_temp:
            self.turn_off()
        elif current_temp > self.max_temp:
            self.turn_on()