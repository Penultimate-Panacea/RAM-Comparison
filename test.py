name = input("Name: ")
cas = input("CAS Timing: ")
speed = int(input("RAM Speed in MHz: "))
speed *= 1000000  # Convert to hertz
val1 = speed / 2  # DDR
val2 = 1/val1  # Invert of DDR
time = float(cas) * val2  # Convert clock speed to time Source: https://www.wepc.com/tips/ram-speed/
time *= 1000000000  # Convert to ns
print("%s's Real Speed is %.2f nanoseconds" % (name, time))