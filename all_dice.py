import os
import main
from itertools import combinations_with_replacement

#  This page was originally made for debug reasons and for testing all edge cases of functions in the main file,
#  and also serves as a hub for statistics. Each function here generates a text file and gives some cool information.
#  Check out the text files to see more.



#  Prepares a txt file with all 252 combinations of 5 dice, sorted, with no duplicates
def all_dice_prepare():
    options = list(range(1, 7))
    dice_list = (list(combinations_with_replacement(options, 5)))
    with open("all_dice.txt", 'x') as f:
        for i in range(len(dice_list)):
            f.write(str(dice_list[i]) + "\n")

    return dice_list

#  File handling is annoying but I kinda like the idea of removing and starting fresh every time so there's no issues
def txt_prepare():
    if os.path.exists("all_dice.txt"):
        os.remove("all_dice.txt")
    if os.path.exists("all_three_of_a_kind.txt"):
        os.remove("all_three_of_a_kind.txt")
    if os.path.exists("all_four_of_a_kind.txt"):
        os.remove("all_four_of_a_kind.txt")
    if os.path.exists("all_full_house.txt"):
        os.remove("all_full_house.txt")
    if os.path.exists("all_small_straight.txt"):
        os.remove("all_small_straight.txt")

#  Finds all possible 3-of-a-kind and prints results
def all_three(dice_list):
    count = 0
    three_of_a_kind_list = []
    for i in range(252):
        if main.three_of_a_kind(dice_list[i]):
            count += 1
            three_of_a_kind_list.append(dice_list[i])
    chance = count / 252

    with open("all_three_of_a_kind.txt", 'x') as f:
        f.write("Number of possible 3-of-a-kinds: " + str(count) + "\n")
        f.write("Probability of rolling this: " + str("%.2f" % chance) + "\n")
        f.write("Here are all the possible combinations:" + "\n")
        for i in range(len(three_of_a_kind_list)):
            f.writelines(str(three_of_a_kind_list[i]) + "\n")

#  Finds all 4-of-a-kind and prints results
def all_four(dice_list):
    count = 0
    four_of_a_kind_list = []
    for i in range(252):
        if main.four_of_a_kind(dice_list[i]):
            count += 1
            four_of_a_kind_list.append(dice_list[i])
    chance = count / 252

    with open("all_four_of_a_kind.txt", 'x') as f:
        f.write("Number of possible 4-of-a-kinds: " + str(count) + "\n")
        f.write("Probability of rolling this: " + str("%.2f" % chance) + "\n")
        f.write("Here are the possible combinations:" + "\n")
        for i in range(len(four_of_a_kind_list)):
            f.write(str(four_of_a_kind_list[i]) + "\n")

#  Finds all possible full house and prints results
def all_full_house(dice_list):
    count = 0
    full_house_list = []
    for i in range(252):
        if main.full_house(dice_list[i]):
            count += 1
            full_house_list.append(dice_list[i])
    chance = count / 252

    with open("all_full_house.txt", 'x') as f:
        f.write("Number of possible Full House: " + str(count) + "\n")
        f.write("Probability of rolling this: " + str("%.2f" % chance) + "\n")
        f.write("Here are all the possible combinations:" + "\n")
        for i in range(len(full_house_list)):
            f.writelines(str(full_house_list[i]) + "\n")

# Finds all possible small straights and also includes large straights. This was the most challenging for me but with
# some help I finally found out how to make it work.
def all_small_straight(dice_list):
    count = 0
    list_dice = list(dice_list)
    all_small_straight_list = []
    for i in range(252):
        test_list, test_bool = main.small_straight(list_dice[i])
        if test_bool:
            count += 1
            all_small_straight_list.append(test_list)
    chance = count / 252

    with open("all_small_straight.txt", 'x') as f:
        f.write("Number of possible Small Straight: " + str(count) + "\n")
        f.write("Probability of rolling this: " + str("%.2f" % chance) + "\n")
        f.write("Here are all the possible combinations:" + "\n")
        for i in range(len(all_small_straight_list)):
            f.writelines(str(all_small_straight_list[i]) + "\n")
        f.write("\nThere are only two possible Large Straights. Here they are:" + "\n")
        f.write("(1, 2, 3, 4, 5)" + "\n")
        f.write("(2, 3, 4, 5, 6)" + "\n")


def all_dice_main():
    txt_prepare()
    all_dice_list = all_dice_prepare()

    all_three(all_dice_list)
    all_four(all_dice_list)
    all_full_house(all_dice_list)
    all_small_straight(all_dice_list)


all_dice_main()
