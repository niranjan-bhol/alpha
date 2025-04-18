import math

print()

e = math.e
ind_rate = float(input("Enter 1-month Term MIBOR : "))
us_rate = float(input("Enter 1-month Term SOFR : "))
days_remaining = int(input("Enter Number of days remaining to the expiry : "))
usdinr_spot = float(input("Enter USD-INR Spot Price : "))

print("\n--------------------------------------------------\n")

print(f"e : {e}")
print(f"1 Month Term MIBOR Rate : {ind_rate} %")
print(f"1 Month Term SOFR Rate : {us_rate} %")
print(f"Number of days remaining to the expiry : {days_remaining}")
print(f"USD-INR Spot Price : {usdinr_spot}")

T = days_remaining/365
r_f = us_rate/100
r_d = ind_rate/100
S = usdinr_spot

F = S * e ** ((r_d - r_f) * T)

print()

print(f"USD-INR Ideal Future Price : {F:.4f}")

print()
