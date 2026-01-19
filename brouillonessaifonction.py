from queue import PriorityQueue

a = PriorityQueue()
a.put((0, "deux"))
a.put((0, "un"))

print(a.get())
a.put((1, "trois"))
print(a.get())
print(a.get())
a.put((0, "quatre"))
print("ex:", a.get()[0])
#print("ex2:", a.get()[1])
#print(a.empty())

