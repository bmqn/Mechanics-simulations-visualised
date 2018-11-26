import tkinter, time, math, os

w = 800
h = 300

#Object 1
u1 = 300
m1 = 1000
x1 = 1 / 4 *  w

#Object 2
u2 = 0
m2 = 500
x2 = 3/4 * w

oW = 30
oH = 60
e = 0

def Cleanup():
    window.quit()
    os._exit(0)

window = tkinter.Tk()
window.protocol("WM_DELETE_WINDOW", Cleanup)
canvas = tkinter.Canvas(window, bg="black", height=h, width=w)
canvas.pack()

restitution = tkinter.Scale(window, from_=0, to=1, resolution = 0.01, orient="horizontal", length=500)
restitution.set(0.5)
restitution.pack(side="right")

label = tkinter.Label(window, text="Coefficient of restitution:")
label.pack(side="right")

delta = 1/256
accumalator = 0
last = 0
while True:
    e = restitution.get()
    
    window.update()
    window.update_idletasks()
    
    while accumalator > delta:
        x1 += delta * u1
        x2 += delta * u2
        
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
                
            v1 = ( (m1 * u1) - (e * 9999999 * (u1 - 0)) ) / (m1 + 9999999)
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
            v2 = ( (e * 9999999 * (0 - u2)) + (m2 * u2) )  / (9999999 + m2)
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
    
    accumalator += time.perf_counter() - last
    last = time.perf_counter()
