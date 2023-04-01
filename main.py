#Project breakdown:
#- plant growth simulation
#	- randomly generated field
#		-water sources, nutrient density
#	-plants will grow towards nutrients
#	-will grow depending on the amount of nutrients they can get
#
#- seed dispursal simulation
#

#TREE RULES:
# F->FF
# X->F[+X]F[-X]+X
# axiom = X
# angle = 20
import sys
import turtle
import random

SYSRULES = {}  # generator system rules for l-system

def derivation(axiom, steps):
    derived = [axiom]  # seed
    for _ in range(steps):
        next_seq = derived[-1]
        next_axiom = [rule(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived


def rule(cmd):
    if cmd in SYSRULES:
        return SYSRULES[cmd]
    return cmd


def draw_l_system(turtle, SYSRULES, seg_length, angle):
    stack = []
    baseangle= angle
    baselen = seg_length
    for command in SYSRULES:
        angle = random.randint(baseangle-10,baseangle+10)
        seg_length = random.randint(baselen-2,baselen+2)
        print ("new angle, ",angle," new seglen: ",seg_length)
        #print(SYSRULES)
        turtle.pd()
        if command in ["F", "G", "R", "L"]:
            turtle.forward(seg_length)
        elif command == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(seg_length)
        elif command == "+":
            turtle.right(angle)
        elif command == "-":
            turtle.left(angle)
        elif command == "[":
            print("new branch: ",turtle.pos())
            stack.append((turtle.position(), turtle.heading()))
        elif command == "]":
            turtle.pu()  # pen up - not drawing
            position, heading = stack.pop()
            turtle.goto(position)
            turtle.setheading(heading)
            print("end branch: ",turtle.pos())


def set_turtle(alpha_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    r_turtle.screen.title("L-System Derivation")
    r_turtle.speed(0)  # adjust as needed (0 = fastest)
    r_turtle.setheading(alpha_zero)  # initial heading
    return r_turtle


def main():
    Growangle = 90#
    seglen = random.randint(5,10)
    # while True:
    #     rule = input("Enter rule: ")
    #     if rule == '0':
    #         break
    #     key, value = rule.split("->")
    #     SYSRULES[key] = value
    rule = "F->FF"
    key, value = rule.split("->")
    SYSRULES[key] = value
    #rule = "X->F[+X]F[-X]+X"
    rule = "X->F[+X]F[-FX]FX"
    key, value = rule.split("->")
    SYSRULES[key] = value
    axiom = input("Enter axiom: ")


    iterations = int(input("num of iterations: "))

    model = derivation(axiom, iterations)  # axiom (initial string), nth iterations
    #print(model)
    angle = float(input("Enter angle: "))

    # Set turtle parameters and draw L-System
    r_turtle = set_turtle(Growangle)  # create turtle object
    turtle_screen = turtle.Screen()  # create graphics window
    turtle_screen.screensize(1500, 1500)
    draw_l_system(r_turtle, model[-1], seglen, angle)  # draw model
    turtle_screen.exitonclick()



if __name__ == "__main__":
    try:
        main()
    except BaseException:
        sys.exit(0)
