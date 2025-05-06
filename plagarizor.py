from Algorithm import rabin_karp, kmp_search, naive_search

def split_into_phrases(text, length=3):
    words = text.split()
    phrases = []

    for i in range(len(words) - length + 1):
        phrase = ' '.join(words[i:i + length])
        phrases.append(phrase)
    return phrases

def generate_ngrams(text, min_len=2, max_len=4):
    words = text.split()
    ngrams = []
    for n in range(min_len, max_len + 1):
        for i in range(len(words) - n + 1):
            ngrams.append(' '.join(words[i:i + n]))
    return ngrams

def detect_plagiarism(reference_text, target_text, method="rabin-karp"):
    match_fn = {
        "rabin-karp": rabin_karp.rabin_karp,
        "kmp": kmp_search.kmp_search,
        "naive": naive_search.naive_search
    }.get(method.lower(), rabin_karp.rabin_karp)

    phrases = generate_ngrams(reference_text, min_len=2, max_len=4)
    matches = []

    for phrase in phrases:
        if match_fn(target_text, phrase):
            matches.append(phrase)

    return sorted(set(matches))

def calculate_similarity(reference_text, target_text, phrase_len=3):
    phrases_ref = set([' '.join(reference_text.split()[i:i+phrase_len]) 
                       for i in range(len(reference_text.split()) - phrase_len + 1)])
    phrases_target = set([' '.join(target_text.split()[i:i+phrase_len]) 
                          for i in range(len(target_text.split()) - phrase_len + 1)])
    
    union = phrases_ref.union(phrases_target)
    intersection = phrases_ref.intersection(phrases_target)

    if not union:
        return 0.0
    return (len(intersection) / len(union)) * 100