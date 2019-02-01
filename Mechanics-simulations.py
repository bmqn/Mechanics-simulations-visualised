import tkinter, time, math, os
from tkinter import ttk

w = 600
h = 400

##### Momentum Collisions #####
class Momentum(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)

        #Object 1
        self.u1 = 300
        self.m1 = 200
        self.x1 = 1 / 3 *  w

        #Object 2
        self.u2 = 0
        self.m2 = 300
        self.x2 = 2 / 3 * w

        self.Eb = 1/9
        self.Ew = 1/3

        self.delta = 1/64
        self.oW = 20
        self.oH = 20

        #Canvas

        self.canvas = tkinter.Canvas(self, bg="black", height=h, width=w)
        self.canvas.grid(row = 1, column=2, columnspan = 5)

        #Reset button

        self.resetButton = tkinter.Button(self, text ="Reset", command = self.reset_blocks,bg="#ffffff")
        self.resetButton.grid(row = 0, column=2, columnspan = 5)

        #Object A sliders

        self.Avelocity = tkinter.Label(self, text="Object A initial velocity:", wraplength=50,fg="red",bg="#ffffff")
        self.Avelocity.grid(row = 0, column=0)

        self.objectAvelocity = tkinter.Scale(self, from_=-500, to=500, resolution = 10, orient="vertical", length=300, fg="red",bg="#ffffff")
        self.objectAvelocity.grid(row = 1, column=0, padx=(10,10))
        self.objectAvelocity.set(100)

        self.AMass = tkinter.Label(self, text="Object A mass:", wraplength=50, fg="red",bg="#ffffff")
        self.AMass.grid(row = 0, column=1)

        self.objectAMass = tkinter.Scale(self, from_=10, to=1000, resolution = 10, orient="vertical", length=300, fg="red",bg="#ffffff")
        self.objectAMass.grid(row = 1, column=1, padx=(10,10))
        self.objectAMass.set(100)

        #Object B sliders

        self.Bvelocity = tkinter.Label(self, text="Object B initial velocity:", wraplength=50, fg="blue",bg="#ffffff")
        self.Bvelocity.grid(row = 0, column=8)

        self.objectBvelocity = tkinter.Scale(self, from_=-500, to=500, resolution = 10, orient="vertical", length=300, fg="blue",bg="#ffffff")
        self.objectBvelocity.grid(row = 1, column=8, padx=(10,10))
        self.objectBvelocity.set(100)

        self.BMass = tkinter.Label(self, text="Object B mass:", wraplength=50, fg="blue",bg="#ffffff")
        self.BMass.grid(row = 0, column=7)

        self.objectBMass = tkinter.Scale(self, from_=10, to=1000, resolution = 10, orient="vertical", length=300, fg="blue",bg="#ffffff")
        self.objectBMass.grid(row = 1, column=7, padx=(10,10))
        self.objectBMass.set(100)

        #Restitution sliders

        self.label1 = tkinter.Label(self, text="Balls coefficient of restitution:",bg="#ffffff")
        self.label1.grid(row = 2, column=3)

        self.restitutionBall = tkinter.Scale(self, from_=0, to=1, resolution = 0.01, orient="horizontal", length=300,bg="#ffffff")
        self.restitutionBall.grid(row = 2, column=5)
        self.restitutionBall.set(0.5)

        self.label3 = tkinter.Label(self, text="Walls coefficient of restitution:",bg="#ffffff")
        self.label3.grid(row = 3, column=3)

        self.restitutionWall = tkinter.Scale(self, from_=0, to=1, resolution = 0.01, orient="horizontal", length=300,bg="#ffffff")
        self.restitutionWall.grid(row = 3, column=5)
        self.restitutionWall.set(0.5)

        self.label2 = tkinter.Label(self, text="Timer mutiplier:",bg="#ffffff")
        self.label2.grid(row = 4, column=3)

        #Time slider

        self.timeMultiplier = tkinter.Scale(self, from_=0, to=10, resolution = 0.1, orient="horizontal", length=300,bg="#ffffff")
        self.timeMultiplier.grid(row = 4, column=5)
        self.timeMultiplier.set(1)

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.grid_columnconfigure(3,weight=1)
        self.grid_columnconfigure(4,weight=1)
        self.grid_columnconfigure(5,weight=1)
        self.grid_columnconfigure(6,weight=1)
        self.grid_columnconfigure(7,weight=1)
        self.grid_columnconfigure(8,weight=1)
        self.grid_columnconfigure(9, weight=1)
        self.grid_columnconfigure(10,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=1)
        self.grid_rowconfigure(4,weight=1)

        self.move_blocks()

    def reset_blocks(self):
        Eb = self.restitutionBall.get()
        Ew = self.restitutionWall.get()

        #Object 1
        self.u1 = self.objectAvelocity.get()
        self.m1 = self.objectAMass.get()
        self.x1 = 1 / 3 *  w

        #Object 2
        self.u2 = self.objectBvelocity.get()
        self.m2 = self.objectBMass.get()
        self.x2 = 2 / 3 * w

    def move_blocks(self):
        multiplier = self.timeMultiplier.get()

        Eb = self.restitutionBall.get()
        Ew = self.restitutionWall.get()

        self.x1 += self.delta * self.u1 * multiplier
        self.x2 += self.delta * self.u2 * multiplier

        if (abs(self.x1 - self.x2) < self.oW * 2):

            overlap = self.x1 - self.x2 + (self.oW * 2)
            self.x1 -= overlap / 2
            self.x2 += overlap / 2

            self.v1 = ( (self.m1 * self.u1) + (self.m2 * self.u2) - (Eb * self.m2 * (self.u1 - self.u2)) ) / (self.m1 + self.m2)
            self.v2 = ( (Eb * self.m1 * (self.u1 - self.u2)) + (self.m1 * self.u1) + (self.m2 * self.u2) )  / (self.m1 + self.m2)

            #print("--------------------------")
            #print("Collision!")
            #print("ObjectA initial velocity = ", format(self.u1, '.2f'), ", ObjectA final velocity = ", format(self.v1, '.2f'))
            #print("ObjectB initial velocity = ", format(self.u2, '.2f'), ", ObjectB final velocity = ", format(self.v2, '.2f'))
            #print("Total momentum = ", format((self.u1*self.m1) + (self.u2*self.m2), '.2f'))
            #print("Coefficient of restitution = ", Eb)
            #print("--------------------------")

            self.u1 = self.v1
            self.u2 = self.v2

        if (self.x1 - self.oW < 0 or self.x1 + self.oW > w):
            if (self.x1 + 5 > w):
                overlap = self.x1 + self.oW - w
                self.x1 -= overlap
            else:
                overlap = self.x1 - self.oW
                self.x1 -= overlap

            self.v1 = ( (self.m1 * self.u1) - (Ew * 999999999999 * (self.u1 - 0)) ) / (self.m1 + 999999999999)
            #print("--------------------------")
            #print("ObjectA collision with wall!")
            #print("ObjectA initial velocity = ", format(self.u1, '.2f'), ", ObjectA final velocity = ", format(self.v1, '.2f'))
            #print("Total momentum = ", format((self.u1*self.m1) + (self.u2*self.m2), '.2f'))
            #print("Coefficient of restitution = ", Ew)
            #print("--------------------------")
            self.u1 = self.v1

        if (self.x2 - self.oW < 0 or self.x2 + self.oW > w):
            if (self.x2 + self.oW > w):
                overlap = self.x2 + self.oW - w
                self.x2 -= overlap
            else:
                overlap = self.x2 - self.oW
                self.x2 -= overlap
            self.v2 = ( (Ew * 999999999999 * (0 - self.u2)) + (self.m2 * self.u2) )  / (999999999999 + self.m2)
            #print("--------------------------")
            #print("ObjectB collision with wall!")
            #print("ObjectB initial velocity = ", format(self.u2, '.2f'), ", ObjectB final velocity = ", format(self.v2, '.2f'))
            #print("Total momentum = ", format((self.u1*self.m1) + (self.u2*self.m2), '.2f'))
            #print("Coefficient of restitution = ", Ew)
            #print("--------------------------")
            self.u2 = self.v2

        self.canvas.delete("all")
        self.canvas.create_rectangle(self.x1 - self.oW, h/2 - self.oH , self.x1 + self.oW, h/2 + self.oH, fill="red")
        self.canvas.create_rectangle(self.x2 - self.oW, h/2 - self.oH , self.x2 + self.oW, h/2 + self.oH, fill="blue")

        self.canvas.after(int(self.delta * 1000), self.move_blocks)

##### Pendulum #####
class Pendulum(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)

        self.delta = 1/64
        self.aa = 0
        self.av = 0
        self.theta = math.pi - 0.3
        self.m = 100
        self.r = 200
        self.g = 1000
        self.damping = 0.005

        #Reset button
        self.resetButton = tkinter.Button(self, text ="Reset", command = self.reset_pendulum, bg="#ffffff")
        self.resetButton.grid(row = 0, column=1, columnspan = 2)

        #Canvas
        self.canvas = tkinter.Canvas(self, bg="black", height=h, width=w)
        self.canvas.grid(row = 1, column=1, columnspan = 2)

        # Pendulum intial velocity
        self.initialVelocityLabel = tkinter.Label(self, text="Initial velocity:", wraplength=100,fg="black",bg="#ffffff")
        self.initialVelocityLabel.grid(row = 0, column=0)

        self.initialVelocity = tkinter.Scale(self, from_=-20, to=20, resolution = 1, orient="vertical", length=300, fg="black",bg="#ffffff")
        self.initialVelocity.grid(row = 1, column=0)
        self.initialVelocity.set(self.av)

        # Length of rod
        self.rodLengthLabel = tkinter.Label(self, text="Length of rod:", wraplength=100, fg="black",bg="#ffffff")
        self.rodLengthLabel.grid(row = 0, column=3)

        self.rodLength = tkinter.Scale(self, from_=5, to=150, resolution = 1, orient="vertical", length=300, fg="black",bg="#ffffff")
        self.rodLength.grid(row = 1, column=3)
        self.rodLength.set(self.r)

        #Time slider
        self.timelabel = tkinter.Label(self, text="Timer mutiplier:",bg="#ffffff")
        self.timelabel.grid(row = 2, column=1)

        self.multiplier = tkinter.Scale(self, from_=0, to=10, resolution = 0.1, orient="horizontal", length=300,bg="#ffffff")
        self.multiplier.grid(row = 2, column=2)
        self.multiplier.set(1)
        
        #Pendulum starting angle
        self.angleLabel = tkinter.Label(self, text="Starting angle:",bg="#ffffff")
        self.angleLabel.grid(row = 3, column=1)

        self.initialAngle = tkinter.Scale(self, from_=-180, to=180, resolution = 10, orient="horizontal", length=300,bg="#ffffff")
        self.initialAngle.grid(row = 3, column=2)
        self.initialAngle.set(self.theta * 180 / math.pi)

        #Pendulum damping 
        self.dampingLabel = tkinter.Label(self, text="Damping:",bg="#ffffff")
        self.dampingLabel.grid(row = 4, column=1)

        self.dampingSlider = tkinter.Scale(self, from_=0, to=0.1, resolution = 0.001, orient="horizontal", length=300,bg="#ffffff")
        self.dampingSlider.grid(row = 4, column=2)
        self.dampingSlider.set(self.damping)

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.grid_columnconfigure(3,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=1)
        self.grid_rowconfigure(4,weight=1)

        self.move_pendulum()

    def reset_pendulum(self):
        self.aa = 0
        self.av = self.initialVelocity.get()
        self.r = self.rodLength.get()
        self.damping = self.dampingSlider.get()
        self.theta = self.initialAngle.get() / 180 * math.pi

    def move_pendulum(self):
        self.aa = (self.m * - self.g * math.sin(self.theta)) / self.m / self.r
        self.av += self.aa * self.delta * self.multiplier.get()
        self.theta += self.av * self.delta * self.multiplier.get()

        self.theta %= 2 * math.pi
        
        self.av *= (1 - self.damping)

        x_p = self.r * math.sin(self.theta)
        y_p = self.r * math.cos(self.theta)

        self.canvas.delete("all")
        self.canvas.create_rectangle(x_p - 10 + w / 2, y_p - 10 + h / 2, x_p + 10 + w / 2, y_p+ 10 + h / 2, fill="red")
        self.canvas.create_line(w / 2, h / 2, x_p + w / 2, y_p + h / 2, fill="red")

        if (self.theta < math.pi):
            self.canvas.create_arc(w / 2 - self.r / 2, h/2 - self.r / 2, w / 2 + self.r / 2, h / 2 + self.r / 2, start=-90, extent=self.theta*180/math.pi, width=2, outline='blue')
        else:
            self.canvas.create_arc(w / 2 - self.r / 2, h/2 - self.r / 2, w / 2 + self.r / 2, h / 2 + self.r / 2, start=270, extent=self.theta*180/math.pi - 360, width=2, outline='blue')
        
        self.canvas.after(int(self.delta * 1000), self.move_pendulum)

window = tkinter.Tk()
window.title("Physics Simulations")

tab_control = ttk.Notebook(window)

momentum = Momentum(tab_control)
momentum.configure(bg="#ffffff")
tab_control.add(momentum, text='Momentum')

pendulum = Pendulum(tab_control)
pendulum.configure(bg="#ffffff")
tab_control.add(pendulum, text='Pendulum')

tab_control.pack()

window.mainloop()
