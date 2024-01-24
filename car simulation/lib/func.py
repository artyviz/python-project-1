import tkinter as tk
import math
from alert_system import AlertSystem
class CarSimulationUI:
    def __init__(self, master):
        self.master = master
        master.title('Car Simulation Prototype')

        self.max_speed = 10
        self.acceleration = 0
        self.velocity = 0
        self.friction = 0.1
        self.steering_angle = 0
        self.car_x = 100
        self.car_y = 180
        self.engine_on = False
        self.alert_system = AlertSystem()
        self.canvas = tk.Canvas(master, width=600, height=300, bg='lightgray')
        self.canvas.pack()


        self.car_front = self.canvas.create_polygon(self.car_x + 30, self.car_y + 20, self.car_x + 30, self.car_y, self.car_x + 40, self.car_y + 10, fill='blue')
        self.car_rear = self.canvas.create_polygon(self.car_x, self.car_y, self.car_x, self.car_y + 20, self.car_x - 10, self.car_y + 10, fill='blue')
        self.car_body = self.canvas.create_rectangle(self.car_x, self.car_y, self.car_x + 30, self.car_y + 20, fill='blue')
        self.wheel1 = self.canvas.create_oval(self.car_x + 5, self.car_y + 15, self.car_x + 15, self.car_y + 25, fill='black')
        self.wheel2 = self.canvas.create_oval(self.car_x + 20, self.car_y + 15, self.car_x + 30, self.car_y + 25, fill='black')


        self.obstacle_left = self.canvas.create_rectangle(50, 50, 60, 250, fill='red')
        self.obstacle_right = self.canvas.create_rectangle(540, 50, 550, 250, fill='red')


        tk.Button(master, text="Start Engine", command=self.start_engine).pack(side=tk.LEFT)
        tk.Button(master, text="Stop Engine", command=self.stop_engine).pack(side=tk.LEFT)
        tk.Button(master, text="Accelerate", command=self.accelerate).pack(side=tk.LEFT)
        tk.Button(master, text="Brake", command=self.brake).pack(side=tk.LEFT)
        tk.Button(master, text="Left", command=lambda: self.steer('left')).pack(side=tk.LEFT)
        tk.Button(master, text="Right", command=lambda: self.steer('right')).pack(side=tk.LEFT)
        tk.Button(master, text="Release Steering", command=self.release_steer).pack(side=tk.LEFT)
        tk.Button(master, text="Reverse", command=self.reverse).pack(side=tk.LEFT)


        tk.Scale(master, from_=0, to=self.max_speed, orient=tk.HORIZONTAL, command=self.set_speed).pack()


        self.status_label = tk.Label(master, text='Status: Stopped, No Collision')
        self.status_label.pack()
        self.warning_label = tk.Label(master, text='No collision warning')
        self.warning_label.pack()
        self.gps_label = tk.Label(master, text='GPS Coordinates: (100, 180)')
        self.gps_label.pack()


        self.update_simulation()

    def start_engine(self):
        self.engine_on = True

    def stop_engine(self):
        self.engine_on = False
        self.velocity = 0

    def accelerate(self):
        self.acceleration += 0.2

    def brake(self):
        self.acceleration -= 0.2

    def steer(self, direction):
        if direction == 'left':
            self.steering_angle = -5
        else:
            self.steering_angle = 5

    def release_steer(self):
        self.steering_angle = 0

    def reverse(self):
        self.acceleration -= 0.2

    def set_speed(self, speed):
        self.max_speed = float(speed)

    def update_simulation(self):
        if self.engine_on:
            self.velocity += self.acceleration


            if self.velocity > 0:
                self.velocity -= self.friction
            elif self.velocity < 0:
                self.velocity += self.friction


            self.car_x += self.velocity * math.cos(math.radians(self.steering_angle))
            self.car_y -= self.velocity * math.sin(math.radians(self.steering_angle))


            if self.car_x < 50:
                self.car_x = 50
                self.velocity = 0
            elif self.car_x > 520:
                self.car_x = 520
                self.velocity = 0
            if self.car_y < 50:
                self.car_y = 50
                self.velocity = 0
            elif self.car_y > 220:
                self.car_y = 220
                self.velocity = 0


            self.canvas.coords(self.car_body, self.car_x, self.car_y, self.car_x + 30, self.car_y + 20)
            self.canvas.coords(self.car_front, self.car_x + 30, self.car_y + 20, self.car_x + 30, self.car_y, self.car_x + 40, self.car_y + 10)
            self.canvas.coords(self.car_rear, self.car_x, self.car_y, self.car_x, self.car_y + 20, self.car_x - 10, self.car_y + 10)
            self.canvas.coords(self.wheel1, self.car_x + 5, self.car_y + 15, self.car_x + 15, self.car_y + 25)
            self.canvas.coords(self.wheel2, self.car_x + 20, self.car_y + 15, self.car_x + 30, self.car_y + 25)


            self.gps_label.config(text=f"GPS Coordinates: ({self.car_x}, {self.car_y})")


            if self.check_collision():
                self.display_warning()
            else:
                self.hide_warning()


        self.master.after(100, self.update_simulation)

    def check_collision(self):
        car_coords = self.canvas.coords(self.car_body)
        obstacle_left_coords = self.canvas.coords(self.obstacle_left)
        obstacle_right_coords = self.canvas.coords(self.obstacle_right)



        return (car_coords[2] > obstacle_left_coords[0] and car_coords[0] < obstacle_left_coords[2] and car_coords[3] > obstacle_left_coords[1] and car_coords[1] < obstacle_left_coords[3]) or \
               (car_coords[2] > obstacle_right_coords[0] and car_coords[0] < obstacle_right_coords[2] and car_coords[3] > obstacle_right_coords[1] and car_coords[1] < obstacle_right_coords[3])



    def display_warning(self):
        self.warning_label.config(text='Collision Warning: High probability')

    def hide_warning(self):
        self.warning_label.config(text='No collision warning')

def main():
    root = tk.Tk()
    app = CarSimulationUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()