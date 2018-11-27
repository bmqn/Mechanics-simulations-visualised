import tkinter, time, math, os

w = 600
h = 300
oW = 30
oH = 60
running = True

#Object 1
u1 = 300
m1 = 200
x1 = 1 / 3 *  w

#Object 2
u2 = 0
m2 = 300
x2 = 2 / 3 * w

Eb = 1/9
Ew = 1/3

def run():
    global running, w, h, oW, oH, u1, u2, x1, x2

    print("RUN!")
    accumalator = 0
    last = time.time() 
    delta = 1/128

    while running:
        
        window.update()
        window.update_idletasks()
    
        multiplier = timeMultiplier.get()
        Eb = restitutionBall.get()
        Ew = restitutionWall.get()

        while accumalator > delta:
            x1 += delta * u1 * multiplier
            x2 += delta * u2 * multiplier

            if (abs(x1 - x2) < oW * 2):

                overlap = x1 - x2 + (oW * 2)
                x1 -= overlap / 2
                x2 += overlap / 2

                v1 = ( (m1 * u1) + (m2 * u2) - (Eb * m2 * (u1 - u2)) ) / (m1 + m2)
                v2 = ( (Eb * m1 * (u1 - u2)) + (m1 * u1) + (m2 * u2) )  / (m1 + m2)

                print("--------------------------")
                print("Collision!")
                print("ObjectA initial velocity = ", format(u1, '.2f'), ", ObjectA final velocity = ", format(v1, '.2f'))
                print("ObjectB initial velocity = ", format(u2, '.2f'), ", ObjectB final velocity = ", format(v2, '.2f'))
                print("Total momentum = ", format((u1*m1) + (u2*m2), '.2f'))
                print("Coefficient of restitution = ", Eb)
                print("--------------------------")

                u1 = v1
                u2 = v2
                break

            if (x1 - oW < 0 or x1 + oW > w):
                if (x1 + 5 > w):
                    overlap = x1 + oW - w
                    x1 -= overlap
                else:
                    overlap = x1 - oW
                    x1 -= overlap

                v1 = ( (m1 * u1) - (Ew * 999999999999 * (u1 - 0)) ) / (m1 + 999999999999)
                print("--------------------------")
                print("ObjectA collision with wall!")
                print("ObjectA initial velocity = ", format(u1, '.2f'), ", ObjectA final velocity = ", format(v1, '.2f'))
                print("Total momentum = ", format((u1*m1) + (u2*m2), '.2f'))
                print("Coefficient of restitution = ", Ew)
                print("--------------------------")
                u1 = v1
                break

            if (x2 - oW < 0 or x2 + oW > w):
                if (x2 + oW > w):
                    overlap = x2 + oW - w
                    x2 -= overlap
                else:
                    overlap = x2 - oW
                    x2 -= overlap
                v2 = ( (Ew * 999999999999 * (0 - u2)) + (m2 * u2) )  / (999999999999 + m2)
                print("--------------------------")
                print("ObjectB collision with wall!")
                print("ObjectB initial velocity = ", format(u2, '.2f'), ", ObjectB final velocity = ", format(v2, '.2f'))
                print("Total momentum = ", format((u1*m1) + (u2*m2), '.2f'))
                print("Coefficient of restitution = ", Ew)
                print("--------------------------")
                u2 = v2
                break

            accumalator -= delta

        canvas.delete("all")
        canvas.create_rectangle(x1 - oW, h/2 - oH , x1 + oW, h/2 + oH, fill="red")
        canvas.create_rectangle(x2 - oW, h/2 - oH , x2 + oW, h/2 + oH, fill="blue")

        accumalator += time.time()  - last
        last = time.time()


def cleanup():
    global running
    running = False
    window.quit()
    os._exit(0)

def reset():
    global w, h, u1, u2, m1, m2, x1, x2
    print("RESETING!")

    Eb = restitutionBall.get()
    Ew = restitutionWall.get()
        
    #Object 1
    u1 = objectAvelocity.get()
    m1 = objectAMass.get()
    x1 = 1 / 3 *  w

    #Object 2
    u2 = objectBvelocity.get()
    m2 = objectBMass.get()
    x2 = 2 / 3 * w


window = tkinter.Tk()
window.configure(bg="#ffe6ff")
window.title("Conservation of Momentum")
window.attributes("-fullscreen", False)
window.protocol("WM_DELETE_WINDOW", cleanup)

#Reset button

resetButton = tkinter.Button(window, text ="Reset", command = reset,bg="#ffe6ff")
resetButton.grid(row = 0, column=4)

#Object A sliders

Avelocity = tkinter.Label(window, text="Object A initial velocity:", wraplength=50, fg="red",bg="#ffe6ff")
Avelocity.grid(row = 0, column=0)

objectAvelocity = tkinter.Scale(window, from_=-500, to=500, resolution = 10, orient="vertical", length=300, fg="red",bg="#ffe6ff")
objectAvelocity.grid(row = 1, column=0, padx=(10,10))
objectAvelocity.set(100)

AMass = tkinter.Label(window, text="Object A mass:", wraplength=50, fg="red",bg="#ffe6ff")
AMass.grid(row = 0, column=1)

objectAMass = tkinter.Scale(window, from_=10, to=1000, resolution = 10, orient="vertical", length=300, fg="red",bg="#ffe6ff")
objectAMass.grid(row = 1, column=1, padx=(10,10))
objectAMass.set(100)

#Object B sliders

Bvelocity = tkinter.Label(window, text="Object B initial velocity:", wraplength=50, fg="blue",bg="#ffe6ff")
Bvelocity.grid(row = 0, column=8)

objectBvelocity = tkinter.Scale(window, from_=-500, to=500, resolution = 10, orient="vertical", length=300, fg="blue",bg="#ffe6ff")
objectBvelocity.grid(row = 1, column=8, padx=(10,10))
objectBvelocity.set(100)

BMass = tkinter.Label(window, text="Object B mass:", wraplength=50, fg="blue",bg="#ffe6ff")
BMass.grid(row = 0, column=7)

objectBMass = tkinter.Scale(window, from_=10, to=1000, resolution = 10, orient="vertical", length=300, fg="blue",bg="#ffe6ff")
objectBMass.grid(row = 1, column=7, padx=(10,10))
objectBMass.set(100)

#Canvas

canvas = tkinter.Canvas(window, bg="black", height=h, width=w)
canvas.grid(row = 1, column=2, columnspan = 5)

#Restitution sliders

label1 = tkinter.Label(window, text="Balls coefficient of restitution:",bg="#ffe6ff")
label1.grid(row = 2, column=3)

restitutionBall = tkinter.Scale(window, from_=0, to=1, resolution = 0.01, orient="horizontal", length=300,bg="#ffe6ff")
restitutionBall.grid(row = 2, column=5)
restitutionBall.set(0.5)

label3 = tkinter.Label(window, text="Walls coefficient of restitution:",bg="#ffe6ff")
label3.grid(row = 3, column=3)

restitutionWall = tkinter.Scale(window, from_=0, to=1, resolution = 0.01, orient="horizontal", length=300,bg="#ffe6ff")
restitutionWall.grid(row = 3, column=5)
restitutionWall.set(0.5)

label2 = tkinter.Label(window, text="Timer mutiplier:",bg="#ffe6ff")
label2.grid(row = 4, column=3)

#Time slider

timeMultiplier = tkinter.Scale(window, from_=0, to=10, resolution = 0.1, orient="horizontal", length=300,bg="#ffe6ff")
timeMultiplier.grid(row = 4, column=5)
timeMultiplier.set(1)

window.grid_columnconfigure(0,weight=1)
window.grid_columnconfigure(1,weight=1)
window.grid_columnconfigure(2,weight=1)
window.grid_columnconfigure(3,weight=1)
window.grid_columnconfigure(4,weight=1)
window.grid_columnconfigure(5,weight=1)
window.grid_columnconfigure(6,weight=1)
window.grid_columnconfigure(7,weight=1)
window.grid_columnconfigure(8,weight=1)
window.grid_columnconfigure(9, weight=1)
window.grid_columnconfigure(10,weight=1)
window.grid_rowconfigure(0,weight=1)
window.grid_rowconfigure(1,weight=1)
window.grid_rowconfigure(2,weight=1)
window.grid_rowconfigure(3,weight=1)
window.grid_rowconfigure(4,weight=1)

run()



