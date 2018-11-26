import tkinter, time, math, os

w = 1000
h = 300
oW = 30
oH = 60
running = False


def cleanup():
    window.quit()
    os._exit(0)

def run():
    global running, w, h, oW, oH
    if (running):
        running = False
        print("RESETING!")
        return
    
    print("RUN!")
    
    #Object 1
    u1 = 300
    x1 = 1 / 3 *  w

    #Object 2
    u2 = -150
    x2 = 2 / 3 * w
    
    accumalator = 0
    last = time.time() 
    delta = 1/128

    running = True
    
    while running:
        
        multiplier = timeMultiplier.get()
        e = restitution.get()
        m1 = objectAMass.get()
        m2 = objectBMass.get()

        window.update()
        window.update_idletasks()

        while accumalator > delta:
            x1 += delta * u1 * multiplier
            x2 += delta * u2 * multiplier

            if (abs(x1 - x2) < oW * 2):

                overlap = x1 - x2 + (oW * 2)
                x1 -= overlap / 2
                x2 += overlap / 2

                v1 = ( (m1 * u1) + (m2 * u2) - (e * m2 * (u1 - u2)) ) / (m1 + m2)
                v2 = ( (e * m1 * (u1 - u2)) + (m1 * u1) + (m2 * u2) )  / (m1 + m2)

                print("--------------------------")
                print("Collision!")
                print("ObjectA initial velocity = ", format(u1, '.2f'), ", ObjectA final velocity = ", format(v1, '.2f'))
                print("ObjectB initial velocity = ", format(u2, '.2f'), ", ObjectB final velocity = ", format(v2, '.2f'))
                print("Total momentum = ", format((u1*m1) + (u2*m2), '.2f'))
                print("Coefficient of restitution = ", e)
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

                v1 = ( (m1 * u1) - (e * 999999999999 * (u1 - 0)) ) / (m1 + 999999999999)
                print("--------------------------")
                print("ObjectA collision with wall!")
                print("ObjectA initial velocity = ", format(u1, '.2f'), ", ObjectA final velocity = ", format(v1, '.2f'))
                print("Total momentum = ", format((u1*m1) + (u2*m2), '.2f'))
                print("Coefficient of restitution = ", e)
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
                v2 = ( (e * 999999999999 * (0 - u2)) + (m2 * u2) )  / (999999999999 + m2)
                print("--------------------------")
                print("ObjectB collision with wall!")
                print("ObjectB initial velocity = ", format(u2, '.2f'), ", ObjectB final velocity = ", format(v2, '.2f'))
                print("Total momentum = ", format((u1*m1) + (u2*m2), '.2f'))
                print("Coefficient of restitution = ", e)
                print("--------------------------")
                u2 = v2
                break

            accumalator -= delta

        canvas.delete("all")
        canvas.create_rectangle(x1 - oW, h/2 - oH , x1 + oW, h/2 + oH, fill="red")
        canvas.create_rectangle(x2 - oW, h/2 - oH , x2 + oW, h/2 + oH, fill="blue")

        accumalator += time.time()  - last
        last = time.time()
    return




window = tkinter.Tk()
window.protocol("WM_DELETE_WINDOW", cleanup)

run = tkinter.Button(window, text ="Run", command = run)
run.grid(row = 0, column=4)

AMass = tkinter.Label(window, text="Object A mass:")
AMass.grid(row = 0, column=0)

objectAMass = tkinter.Scale(window, from_=10, to=1000, resolution = 10, orient="vertical", length=200)
objectAMass.grid(row = 1, column=0)
objectAMass.set(100)

BMass = tkinter.Label(window, text="Object B mass:")
BMass.grid(row = 0, column=9)

objectBMass = tkinter.Scale(window, from_=10, to=1000, resolution = 10, orient="vertical", length=200)
objectBMass.grid(row = 1, column=9)
objectBMass.set(100)

canvas = tkinter.Canvas(window, bg="black", height=h, width=w)
canvas.grid(row = 1, column=2, columnspan = 5)

label1 = tkinter.Label(window, text="Coefficient of restitution:")
label1.grid(row = 2, column=3)

restitution = tkinter.Scale(window, from_=0, to=1, resolution = 0.01, orient="horizontal", length=200)
restitution.grid(row = 2, column=5)
restitution.set(0.5)

label2 = tkinter.Label(window, text="Timer mutiplier:")
label2.grid(row = 3, column=3)

timeMultiplier = tkinter.Scale(window, from_=0, to=10, resolution = 0.1, orient="horizontal", length=200)
timeMultiplier.grid(row = 3, column=5)
timeMultiplier.set(1)



