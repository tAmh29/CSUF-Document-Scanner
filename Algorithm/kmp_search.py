def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0 # Length of previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[1] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

# Main KMP function to search pattern in text
def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern) # Preprocess the pattern
    i = j = 0
    positions = []

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j) # Match found
            j = lps[j - 1] # Continue searching here
        elif i < n and pattern[j] != text[i]:
            j = lps[j - 1] if j != 0 else 0
            if j == 0:
                i += 1
    return positions

text = "Hello World, this is Computer Science !!!"
pattern = "Computer"

# Output
print("KMP Pattern found at: ", kmp_search(text, pattern))