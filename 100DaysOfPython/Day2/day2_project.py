print("Welcome to the tip calculator!")
print("What was the total bill?")
total_bill = float(input("$"))
print("What percentage tip would you like to give?")
tip_percentage = int(input("%"))
print("How many people to split the bill?")
people = int(input())
tip = total_bill * (tip_percentage / 100)
total_bill_with_tip = total_bill + tip
total_bill_with_tip_pp = total_bill_with_tip / people
print("Bill amount: {bill}".format(bill=total_bill_with_tip_pp))