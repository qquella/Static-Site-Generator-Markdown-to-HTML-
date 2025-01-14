# Step-by-step analysis using Python: Count valid strings with specific conditions
from itertools import product


def contains_substring(s, substring):
    return substring in s


def count_valid_strings(length, alphabet, required_substring, forbidden_substring):
    """
    Counts strings of a given length over an alphabet containing the required substring
    and not containing the forbidden substring.
    """
    # Generate all possible strings of the given length
    all_strings = ["".join(p) for p in product(alphabet, repeat=length)]

    print("all string len: ", len(all_strings))

    # Filter strings based on the conditions
    valid_strings = [
        s
        for s in all_strings
        if contains_substring(s, required_substring)
        and not contains_substring(s, forbidden_substring)
    ]

    return len(valid_strings), valid_strings


# Parameters
length = 5
alphabet = ["0", "1"]
required_substring = "11"
forbidden_substring = "00"

# Count the valid strings
valid_count = count_valid_strings(
    length, alphabet, required_substring, forbidden_substring
)
print(valid_count)
