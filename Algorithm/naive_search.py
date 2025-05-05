def naive_search(text, pattern):
    positions = [] # To store indices where pattern is found
    n = len(text)
    m = len(pattern)

    # Loop through all possible starting positions
    for i in range(n - m + 1):
        match = True
        for j in range(m): # Compare each character
            if text[i + j] != pattern[j]:
                match = False # Mismatch found
                break
        if match:
            positions.append(i) # Store the index of the match
    return positions