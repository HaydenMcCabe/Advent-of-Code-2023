import re

# Create a lookup table that take an ASCII value
# representing a card (A, K, Q, J, T, 9, 8, etc.) 
# and returns a value for the card in the range 0 --> 12
card_value_lookup = [0] * 128
card_value_lookup[65] = 12
card_value_lookup[75] = 11
card_value_lookup[81] = 10
card_value_lookup[74] = 9
card_value_lookup[84] = 8
card_value_lookup[57] = 7
card_value_lookup[56] = 6
card_value_lookup[55] = 5
card_value_lookup[54] = 4
card_value_lookup[53] = 3
card_value_lookup[52] = 2
card_value_lookup[51] = 1

# Create another lookup table used to count the cards
# seen in a hand.
card_count_lookup = [0] * 128
card_count_lookup[65] = 1 << 0
card_count_lookup[75] = 1 << 3
card_count_lookup[81] = 1 << 6
card_count_lookup[74] = 1 << 9
card_count_lookup[84] = 1 << 12
card_count_lookup[57] = 1 << 15
card_count_lookup[56] = 1 << 18
card_count_lookup[55] = 1 << 21
card_count_lookup[54] = 1 << 24
card_count_lookup[53] = 1 << 27
card_count_lookup[52] = 1 << 30
card_count_lookup[51] = 1 << 33
card_count_lookup[50] = 1 << 36

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

    broken = False
    has_seen_three = False
    has_seen_two = False
    for i in range(13):
        card_count = (count >> 3 * i) & 0x7
        if card_count == 5:
            # Five of a kind: Value 6
            key = 6 << 20
            broken = True
            break
        elif card_count == 4:
            # Four of a kind: Value 5
            key = 5 << 20
            broken = True
            break
        elif card_count == 3:
            if has_seen_two:
                # Full house: Value 4
                key = 4 << 20
                broken = True
                break
            has_seen_three = True
        elif card_count == 2:
            if has_seen_two:
                # Two pair: Value 2
                key = 2 << 20
                broken = True
                break
            if has_seen_three:
                # Also a full house: Value 4
                key = 4 << 20
                broken = True
                break
            has_seen_two = True

    # Handle the cases where the loop wasn't
    # broken early.
    if not broken:
        if has_seen_three:
            # Three of a kind: Value 3
            key = 3 << 20
        elif has_seen_two:
            # One pair: Value 1
            key = 1 << 20
            

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
