import re

# Create a lookup table that take an ASCII value
# representing a card (A, K, Q, J, T, 9, 8, etc.) 
# and returns a value for the card in the range 0 --> 12
card_value_lookup = [0] * 128
card_value_lookup[65] = 12
card_value_lookup[75] = 11
card_value_lookup[81] = 10
# card_value_lookup[74] = 0 # J keeps the default value of 0
card_value_lookup[84] = 9
card_value_lookup[57] = 8
card_value_lookup[56] = 7
card_value_lookup[55] = 6
card_value_lookup[54] = 5
card_value_lookup[53] = 4
card_value_lookup[52] = 3
card_value_lookup[51] = 2
card_value_lookup[50] = 1

# Create another lookup table used to count the cards
# seen in a hand.
card_count_lookup = [0] * 128
card_count_lookup[65] = 1 << 0
card_count_lookup[75] = 1 << 3
card_count_lookup[81] = 1 << 6
card_count_lookup[74] = 1 << 36 # J is shifted to the highest position
card_count_lookup[84] = 1 << 9
card_count_lookup[57] = 1 << 12
card_count_lookup[56] = 1 << 15
card_count_lookup[55] = 1 << 18
card_count_lookup[54] = 1 << 21
card_count_lookup[53] = 1 << 24
card_count_lookup[52] = 1 << 27
card_count_lookup[51] = 1 << 30
card_count_lookup[50] = 1 << 33

# Make a function to return a key for a hand that can be used
# to sort it
def key_for_card(card: str) -> int:
    key = 0
    count = 0
    bytes = list(card.encode("ascii"))
    # The most significant bits represent the type of hand,
    # with high card as the lowest and five-of-a-kind as the
    # highest.
    count += card_count_lookup[bytes[0]]
    count += card_count_lookup[bytes[1]]
    count += card_count_lookup[bytes[2]]
    count += card_count_lookup[bytes[3]]
    count += card_count_lookup[bytes[4]]

    joker_count = count >> 36

    if joker_count > 3:
        # 4 or 5 jokers counts as 5 of a kind
        # Five of a kind: Value 6
        key = 6 << 20
    else:
        broken = False
        has_seen_three = False
        has_seen_two = False

        # Iterate through the remaining 12 card counts
        for i in range(12):
            card_count = (count >> 3 * i) & 0x7
            if card_count == 5:
                # Five of a kind: Value 6
                key = 6 << 20
                broken = True
                break
            elif card_count == 4:
                # Either four of a kind: Value 5
                # or five of a kind: Value 6 with a joker
                key = (5 + joker_count) << 20
                broken = True
                break
            elif card_count == 3:
                if joker_count > 0:
                    # With jokers, the hand is either
                    # Five of a kind: Value 6 (2 jokers) or
                    # Four of a kind: Value 5 (1 joker)
                    key = (4 + joker_count) << 20
                    broken = True
                    break
                elif has_seen_two:
                    # Full house: Value 4
                    key = 4 << 20
                    broken = True
                    break
                has_seen_three = True
            elif card_count == 2:
                if joker_count > 1:
                    # With more than 1 joker, the hand is either
                    # Five of a kind: Value 6 (3 jokers) or
                    # Four of a kind: Value 5 (2 jokers)
                    key = (3 + joker_count) << 20
                    broken = True
                    break
                elif has_seen_two:
                    # Either two pair: Value 2
                    # of Full house: Value 4 with a joker
                    key = (2 + 2 * joker_count) << 20
                    broken = True
                    break
                if has_seen_three:
                    # Also a full house: Value 4
                    key = 4 << 20
                    broken = True
                    break
                has_seen_two = True

        # # Handle the cases where the loop wasn't
        # # broken early.
        if not broken:
            if has_seen_three:
                # The cases with jokers were handled above.
                # Three of a kind: Value 3
                key = 3 << 20
            elif has_seen_two:
                # The remaining cases for holding a pair
                # are with or without 1 joker for either
                # Three of a kind: Value 3 (1 joker)
                # One pair: Value 1 (0 jokers)
                key = (1 + 2 * joker_count) << 20
            elif joker_count > 0:
                # If there were no natural 2, 3, 4, or 5
                # card sets, the hand's value is determined
                # by the number of jokers, with could be
                # 0, 1, 2, or 3 for hands:
                # One pair: Value 1 (1 Joker)
                # Three of a kind: Value 3 (2 Jokers)
                # Four of a kind: Value 5 (3 Jokers)
                key = (2 * joker_count - 1) << 20
            
    # The lowest 20 bits represent the cards' face values.
    key |= card_value_lookup[bytes[0]] << 16
    key |= card_value_lookup[bytes[1]] << 12
    key |= card_value_lookup[bytes[2]] << 8
    key |= card_value_lookup[bytes[3]] << 4
    key |= card_value_lookup[bytes[4]]

    return key

# Make a line parsing regex
parser = re.compile(r"([2-9AKQJT]{5})\s(\d+)")

# Create an array of tuples for each hand, with
# the hand as a string, and the bet as an int.
hands = []

data_lines = open("data.txt").read().splitlines()
for line in data_lines:
    parts = parser.match(line)
    hands.append( (key_for_card(parts.group(1)), int(parts.group(2))) )

# Sort based on the hand
hands.sort()

# Find the total
sum = 0
for i in range(len(hands)):
    sum += (i + 1) * hands[i][1]

print(sum)
