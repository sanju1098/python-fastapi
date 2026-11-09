# python3 variables.py -> to start

print("Hello")

count=10
tax=0.25
taxAmt = count + (count * tax)
print("Total Price with Tax is ", taxAmt)


amount=50
itemPrice = 15
tax=3
taxAmout = itemPrice * (tax / 100)
balance=amount - itemPrice - taxAmout
print("Balance left is ", balance)


# name  = input("What is your name: ")
# print(f"Your name is {name}")

"""
Multi
Line 
comments 
can be written 
in 
this
way
"""

'''
Multi
Line 
comments 
can 
also be 
written 
in 
this
way 
also
'''


sentence = "Hello {} {}"
fname="Sanjay"
lname="Kumar"
print(sentence.format(fname,lname))


# days = int(input("how many days until their birthday: "))
# typeof = type(days)
# print(typeof)
# print(f"{days/7} weeks left for your birthday")


myList = [80,96,72, 100,8]
print(myList)

myList.append(1000)
print(myList)

myList.insert(2,199)
print(myList)

myList.remove(72)
print(myList)

myList.pop(0)
print(myList)

myList.sort()
print(myList)

# List of 5 animals
zoo = ["lion", "tiger", "elephant", "giraffe", "zebra"]
print("List:", zoo)


# Delete the animal at the 3rd index (fourth animal, zero-based index)
zoo.pop(3)
print("After delete the animal at the 3rd index:", zoo)

# Append a new animal at the end of the list
zoo.append("panda")
print("Append:", zoo)


# Delete the animal at the beginning of the list
zoo.pop(0)
print("Delete the animal at the beginning of the list:", zoo)


# Print all the animals
print("All animals in the zoo:", zoo)

# Print only the first 3 animals
print("First 3 animals:", zoo[:3])



like_coffe = True
like_Cake = False

print(like_Cake)
print(like_coffe)

print(type(like_Cake))
print(type(like_coffe))

print(1 == 2)
print(1 == "1")
# No === in python


# Logical Operator
print (1 > 3 and 5 < 7)
print (1 > 3 or 5 < 7)
print (not(1 == 1))


# Grade Classification System
grade = 87  # Integer between 0-100

if grade >= 90 and grade <= 100:
    print('A')
elif grade >= 80 and grade < 90:
    print('B')
elif grade >= 70 and grade < 80:
    print('C')
elif grade >= 60 and grade < 70:
    print('D')
elif grade >= 0 and grade < 60:
    print('F')
else:
    print('Invalid grade')



my_list = [1,2,3,4,5]
for x in my_list:
    print(x, "Loop")

for x in range (3,6):
    print(x, "Range")


# While loop with for loop inside - Print list 3 times, skip Monday
my_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

count = 0
while count < 3:
    print(f"\n--- Iteration {count + 1} ---")
    for day in my_list:
        if day == "Monday":
            continue  # Skip printing Monday
        print(day)
    count += 1


# Dictionary Operations
my_vehicle = {
    "model": "Ford",
    "make": "Explorer",
    "year": 2018,
    "mileage": 40000
}

# Print all keys and values using a for loop
print("\n--- All keys and values from my_vehicle ---")
for key, value in my_vehicle.items():
    print(f"{key}: {value}")

# Create a copy of my_vehicle
vehicle2 = my_vehicle.copy()

# Add new key 'number_of_tires' with value 4
vehicle2["number_of_tires"] = 4

# Delete the mileage key and value
del vehicle2["mileage"]

# Print just the keys from vehicle2
print("\n--- Keys from vehicle2 ---")
for x in vehicle2.keys():
    print(x)


"""
Create a function that takes in 3 parameters(firstname, lastname, age) and
returns a dictionary based on those values
"""

def create_person(firstname, lastname, age):
    """Returns a dictionary with person information"""
    person_dict = {
        "firstname": firstname,
        "lastname": lastname,
        "age": age
    }
    return person_dict

# Test the function
result = create_person("Sanjay", "Kumar", 27)
print("\n--- Person Dictionary ---")
print(result)
print(f"Full Name: {result['firstname']} {result['lastname']}, Age: {result['age']}")