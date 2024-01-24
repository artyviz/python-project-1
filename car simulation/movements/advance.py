class Car:
    def _init_(self):
        self.engine_on = False
        self.velocity = 0
        self.acceleration = 0
        self.friction_coefficient = 0.1
        self.steering_angle = 0 
        self.position = 0
        self.max_velocity = 120
        self.min_velocity = -50
        self.gear = 0
        self.gear_ratios = [0, 10, 15, 20]
        self.current_gear_ratio = self.gear_ratios[self.gear]
        self.gear_change_rate = 1
        self.max_acceleration = 5
        self.max_deceleration = -10

    def start_engine(self):
        self.engine_on = True

    def stop_engine(self):
        self.engine_on = False
        self.velocity = 0
        self.acceleration = 0

    def accelerate(self):
        if self.engine_on:
            if self.velocity < self.max_velocity:
                self.acceleration = min(self.acceleration + 0.2, self.max_acceleration)
            else:
                self.acceleration = 0

    def brake(self):
        if self.engine_on:
            if self.velocity > self.min_velocity:
                self.acceleration = max(self.acceleration - 0.2, self.max_deceleration)
            else:
                self.acceleration = 0

    def change_gear(self, direction):
        if direction == 'up':
            if self.gear < len(self.gear_ratios) - 1:
                self.gear += 1
        elif direction == 'down':
            if self.gear > 0:
                self.gear -= 1

        self.current_gear_ratio = self.gear_ratios[self.gear]

    def update(self, time_interval):
        self.velocity += (self.acceleration - self.friction_coefficient * self.velocity) * time_interval
        self.position += self.velocity * time_interval

        if self.velocity != 0:
            turning_radius = 1 / self.steering_angle if self.steering_angle != 0 else float('inf')
            turning_angle = (self.velocity * time_interval) / turning_radius
            self.position += turning_angle

    def steer(self, direction):
        if direction == 'left':
            self.steering_angle = -0.1
        elif direction == 'right':
            self.steering_angle = 0.1

    def release_steer(self):
        self.steering_angle = 0