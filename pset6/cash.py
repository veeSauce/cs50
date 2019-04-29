import cs50



while True:
    x = cs50.get_float("Change amount: ")
    if x != 0 and x > 0:
        break

# convert the dollar amount to pennies
Cents = x * 100
TotalCoins = 0

print(f"these many pennies {Cents:.2f}")

# check for how many quarters
check = Cents % 25

if check != 0:
    QuartersNeeded = Cents // 25
elif check == 0:
    TotalCoins = Cents/25

# check if dimes are needed
Remainder = Cents - (QuartersNeeded * 25)

check = Remainder % 10
if check != 0:
    DimesNeeded = Remainder // 10
elif check == 0:
    TotalCoins = (Remainder/10) + QuartersNeeded

# check if nickels are needed
Remainder = Remainder - (DimesNeeded * 10)

check = Remainder % 5
if check != 0:
    NickelsNeeded = Remainder // 5
elif check == 0:
    TotalCoins = (Remainder/5) + DimesNeeded + QuartersNeeded

# pennies needed
print(round(Remainder + NickelsNeeded + DimesNeeded + QuartersNeeded + TotalCoins))