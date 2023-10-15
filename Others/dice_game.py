import random

def roll_die(sides = 6):
    roll = random.randrange(1, int(sides+1))
    return roll

def main():
    sides = input("How many sides on the dice? ")  
    sides = int(sides)  

    number_of_rolls = 0
    results_total = 0

    while(number_of_rolls < 3):
        result = roll_die(sides)
        results_total += result

        print("You rolled a", result)
        if number_of_rolls == 0:
            print("Total after first roll:", results_total, "\n")
        elif number_of_rolls == 1:
            print("Total after 2 rolls:", results_total, "\n")
        else:
            print("Total after 3 rolls:", results_total, "\n")
        number_of_rolls += 1

    average_roll = results_total/number_of_rolls

    print("Your average roll was", round(average_roll, 2))

main()
