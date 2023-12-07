# Yahtzee Game in Python
import random
from collections import Counter

scorecard = [
    ["Ones", 0],
    ["Twos", 0],
    ["Threes", 0],
    ["Fours", 0],
    ["Fives", 0],
    ["Sixes", 0],
    ["3 of a Kind", 0],
    ["4 of a Kind", 0],
    ["Full House", 0],
    ["Small Straight", 0],
    ["Large Straight", 0],
    ["Yahtzee", 0],
    ["Chance", 0]
]
scorecard_index_tracker = []  # prevents the player from filling a slot on the scorecard more than once
def index_tracker(index, tracker_list):
    for items in tracker_list:
        if index == items:
            print("You already filled in that slot. Please try again.")
            return False
    return True

#  displays the updated scorecard
def scorecard_display():
    for i in range(6):
        print(str(i + 1) + ") " + str(scorecard[i][0]) + " " + str(scorecard[i][1]))
    print("\n")
    for y in range(7):
        print(str(y + 7) + ") " + str(scorecard[y + 6][0]) + " " + str(scorecard[y + 6][1]))

#  function to roll dice
def roll_dice(number_of_dice):
    dice = []
    for i in range(number_of_dice):
        nums = random.randint(1, 6)
        dice.append(nums)
    dice.sort()
    return dice


#  In phase 1, the user rolls 5 dice then decides which ones to keep then keeps rolling until 3 rolls or until the
#  user keeps them all. Returns list of 5 kept dice on the table as final_dice.
def phase_one():
    temp = []
    roll_count = 3
    dice_to_roll = 5
    dice_on_table = []
    turn_finish = False

    while not turn_finish:
        dice_on_table = roll_dice(dice_to_roll)
        italic = ("\x1B[3m" + "rolls dice" + "\x1B[0m")
        if roll_count == 3:
            print("\nLet's begin your turn. " + italic)
            print(dice_on_table)
        elif roll_count == 2:
            print("Second roll: " + italic)
            print(dice_on_table)
        elif roll_count == 1:
            print("Last roll! Here we go: " + italic)
            print(dice_on_table)
            break

        #  just recently learned it can be effective to debug user input error by using a basic while loop
        while True:
            if roll_count == 1:
                break
            k = input("How many dice do you want to keep? (1-" + str(len(dice_on_table)) + ") ")

            if k.isdigit():
                k = int(k)
                test = [None] * k
                dice_to_roll = dice_to_roll - k
                if 0 <= k <= 5:
                    break
                else:
                    print("Please enter a value from 1 to 5")
            else:
                print("Please enter a number")

        if k == 5:
            print("Here are your dice:")
            print(dice_on_table)  # final dice now
            break
        elif k > 0:
            if k == len(dice_on_table):
                break

        end_input = False
        while not end_input:
            if k == 0:
                break
            kept_dice = [int(x) for x in input("Enter the values to keep separated by a comma: ").split(",")]

            for i in range(len(kept_dice)):
                if 1 <= kept_dice[i] <= 6:
                    end_input = True
                else:
                    print("The values must be between 1 and 6. Try again")
                    end_input = False
            print("You kept these values:")
            print(kept_dice)
            for dice in kept_dice:
                temp.append(dice)

        roll_count -= 1
        if roll_count == 0:
            for dice in dice_on_table:
                temp.append(dice)
            break
    if len(temp) == 5:
        final_dice = temp
    else:
        final_dice = temp + dice_on_table
        final_dice.sort()
    return final_dice

# Phase 2 is after the user finishes rolling the dice and the 5 final_dice are on the table and are processed
# according to user input for the index of the scorecard
def phase_two(dice_list):
    print("It is now the end of your turn. Here are your dice:")
    print(dice_list)
    print("Here is your current scorecard:")
    scorecard_display()
    print("\nScore index tracker: Don't enter any of these values:")
    print(scorecard_index_tracker)
    while True:
        while True:
            score_index = input("\nWhat score do you want to put? Enter 1-13 ")
            if score_index.isdigit():
                score_index = int(score_index)
                index_check = index_tracker(score_index, scorecard_index_tracker)
                if index_check:
                    break
        if 1 <= score_index <= 13:
            break
        else:
            print("Please enter a valid number 1-13")

    scorecard_index_tracker.append(score_index)
    scorecard_index_tracker.sort()

    if 1 <= score_index <= 6:
        top_scorecard(dice_list, score_index)
    else:
        bottom_scorecard(dice_list, score_index)

#  For use in phase 2 of the turn. Returns the sum of all the indicated number of values (sum of all 1's, 2's etc.)
def top_scorecard(dice_list, index):
    sum_dice = 0
    for items in dice_list:
        if items == index:
            sum_dice += items
    scorecard[index - 1][1] = sum_dice
    scorecard_display()

#  For use in phase 2. It runs different functions depending on user input. For many cases, if the conditions aren't
#  met, the score for that slot stays as 0
def bottom_scorecard(dice_list, index):
    i = index - 1
    if index == 7:
        scorecard[i][1] = sum(dice_list)
        if not three_of_a_kind(dice_list):
            scorecard[i][1] = 0
    if index == 8:
        scorecard[i][1] = sum(dice_list)
        if not four_of_a_kind(dice_list):
            scorecard[i][1] = 0
    if index == 9:
        scorecard[i][1] = 25
        if not full_house(dice_list):
            scorecard[i][1] = 0
    if index == 10:
        scorecard[i][1] = 30
        if not small_straight(dice_list):
            scorecard[i][1] = 0
    if index == 11:
        scorecard[i][1] = 40
        if not large_straight(dice_list):
            scorecard[i][1] = 0
    if index == 12:
        scorecard[i][1] = 50
        if not yahtzee(dice_list):
            scorecard[i][1] = 0
        else:
            print("Congrats! You got a yahtzee!\n")
    if index == 13:
        scorecard[i][1] = sum(dice_list)  # Chance slot is extra space for a bad set of dice.

    scorecard_display()

# checks if the final_dice has a 3-of-a-kind and fills the slot with the sum of all the dice
def three_of_a_kind(dice_list):
    counter = Counter(dice_list)
    check = max(counter.values())
    if check >= 3:
        return True
    else:
        return False


#  checks if there is a 4-of-a-kind and fills the slot with sum of all the dice
def four_of_a_kind(dice_list):
    counter = Counter(dice_list)
    check = max(counter.values())
    if check >= 4:
        return True
    else:
        return False


#  full house is 2 of a kind plus 3 of a kind. uses counter module to check for the conditions
def full_house(dice_list):
    counter = Counter(dice_list)
    check2 = min(counter.values())
    check3 = max(counter.values())
    if check2 == 2 and check3 == 3:
        return True
    else:
        return False

# Small straight is 4 numbers in a row. This function makes things very simple by first converting the list of numbers
# into a set and then back into a list again. This is because a set cannot have any duplicates. So it removes any
# duplicate values and then turns back into a list, sorts them, then does a simple check if there are 4 numbers in a row
def small_straight(dice_list):
    unique_numbers = list(set(dice_list))
    sorted_numbers = sorted(unique_numbers)

    for i in range(len(sorted_numbers) - 3):
        if sorted_numbers[i] + 1 == sorted_numbers[i + 1] and \
                sorted_numbers[i + 1] + 1 == sorted_numbers[i + 2] and \
                sorted_numbers[i + 2] + 1 == sorted_numbers[i + 3]:
            return dice_list, True

    return dice_list, False


#  Large straight is 5 in a row. There are only 2 possible combos for this so this function simply compares the dice
#  to the conditions and returns
def large_straight(dice_list):
    case1 = [1, 2, 3, 4, 5]
    case2 = [2, 3, 4, 5, 6]
    if dice_list == case1 or dice_list == case2:
        return True
    else:
        return False


# Yahtzee is 5 of a kind. Truly a wonder to behold, and it's always really hype if you get it
def yahtzee(dice_list):
    y = dice_list[0]
    check = [y] * 5
    if dice_list == check:
        return True
    else:
        return False

#  After 13 turns, the two scorecard totals and the total sum is displayed, with a prompt for the user to play again
def end_of_game(scores):
    top_sum = 0
    bottom_sum = 0
    for i in range(6):
        top_sum += scores[i][1]
    for i in range(6, 13):
        bottom_sum += scores[i][1]

    total = top_sum + bottom_sum
    print("\nIt is now the end of the game. Here are your totals:")
    #  Bonus condition in the top scorecard
    if top_sum >= 63:
        better_top_sum = top_sum + 35
        print("Top Sum = " + str(top_sum) + " + 35 = " + str(better_top_sum))
        total = better_top_sum + bottom_sum
    else:
        print("Top Sum = " + str(top_sum))

    print("Bottom Sum = " + str(bottom_sum))
    print("Total Sum = " + str(total))
    print("Good game!")


def main():
    print("Welcome! Let's play some Yahtzee.")
    play_again = True
    while play_again:
        turn_count = 13
        end_game = False

        while not end_game:
            dice = phase_one()
            phase_two(dice)

            turn_count -= 1
            if turn_count == 0:
                end_game = True

        end_of_game(scorecard)
        reply = input("Want to play again? (yes/no) ")
        if reply == "no":
            play_again = False


main()
