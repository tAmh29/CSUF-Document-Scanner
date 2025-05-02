  ### Imports

### Imports

## Helpers
def pad(text,expected_length,padding=" "):
    if len(text)>=expected_length:
        print("Redundant call of pad()")
        return text
    padded_text = text
    for i in range(expected_length-len(text)):
        padded_text += padding
    return padded_text

# ## I JUST REALIZED THIS IS USELESS
# ## takes a list and removes duplicates starting from the end
# def backsweepDuplicates(tokenList):
#     for i in range(len(tokenList),0,-1): ## start at end of list, iterate backwards
#         for j in range(i-1,0,-1): ## check the "previous"
#             if tokenList[j] == tokenList[i]:
#                 tokenList.pop(j)

#     ## This should directly modify tokenList so it's two-way


## taken from geeksforgeeks
def removeDuplicates(tokenList):
    res = []
    for val in tokenList:
        if val not in res:
            res.append(val)
    return res
## returns cleaned list, no duplicates, prioritizing left to right.

def butcher(text, choplength):
    butchered = []
    if len(text)<= choplength:
        print("Redundant butcher call.")
        return pad(text,choplength)
    for i in range(0,len(text),choplength):
        butchered.append(text[i:i+choplength])
    butchered[len(butchered)-1] = pad(butchered[len(butchered)-1],choplength)
    return butchered
## Helpers
#### Stolen
# Following program is the python implementation of
# Rabin Karp Algorithm given in CLRS book

# d is the number of characters in the input alphabet
d = 256

# Search the pat string in the txt string
def search(pat, txt, q=101):
    M = len(pat)
    N = len(txt)
    i = 0
    j = 0
    p = 0    # hash value for pattern
    t = 0    # hash value for txt
    h = 1
    found_indexes = []
    # The value of h would be "pow(d, M-1)%q"
    for i in range(M-1):
        h = (h*d) % q

    # Calculate the hash value of pattern and first window
    # of text
    for i in range(M):
        p = (d*p + ord(pat[i])) % q
        t = (d*t + ord(txt[i])) % q

    # Slide the pattern over text one by one
    for i in range(N-M+1):
        # Check the hash values of current window of text and
        # pattern if the hash values match then only check
        # for characters one by one
        if p == t:
            # Check for characters one by one
            for j in range(M):
                if txt[i+j] != pat[j]:
                    break
            
            j += 1
            # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
            if j == M:
                found_indexes.append(i)
                #     print("Pattern found at index " + str(i))

        # Calculate hash value for next window of text: Remove
        # leading digit, add trailing digit
        if i < N-M:
            t = (d*(t-ord(txt[i])*h) + ord(txt[i+M])) % q

            # We might get negative values of t, converting it to
            # positive
            if t < 0:
                t = t
    return found_indexes


# Driver Code

# This code is contributed by Bhavya Jain
####

# with open("cited_work.txt") as src:
#     referencework = str(src.read())
# with open("examine_me.txt") as chk:
#     examinedwork = str(chk.read())

CHOPLENGTH = 10
#print(referencework)
#print(type(referencework))

def detect_plagiarism(referencework, examinedwork, CHOPLENGTH):
    ref_tokens = butcher(referencework,CHOPLENGTH)
    matches = []
    for token in ref_tokens:
        matches.append(search(token,examinedwork))


    ## Check that arrays are parallel
    if (len(ref_tokens)==len(matches)):
        print("Success!")
    print("# of tokens:",len(ref_tokens),"\n# of match sets:",len(matches))
    print(matches)


    sus_sections = [] ## list of (index, length) tuples of suspicious sections text found in examined text.
    for i in range(len(matches)):
        if len(matches[i])==0:
            continue ## skip loop if no matches found
        ## Ok so


        for j in range(len(matches[i])): ## ok so we have a target set of matches, we loop thru them and see if adjacent matches are found.
            k = 1
            while True:
                if matches[i][j]+CHOPLENGTH*k in matches[i+k]:  ## matches[i][j]+CHOPLENGTH*k
                    matches[i+k].remove(matches[i][j]+CHOPLENGTH*k)
                    k += 1
                else:
                    break
            size = CHOPLENGTH*k
            
            start_index = matches[i][j] - 1 ## we need to get the start index of the match, so we subtract 1 from the match index.
            if size >= CHOPLENGTH:
                sus_sections.append((start_index,size))
        matches[i] = []

    print(sus_sections)

    result = []
    for loc in sus_sections:
        a = loc[0] ## start index of the match
        length = loc[1]  ## length of the match
        b = min(len(examinedwork), a + length) ## end index of the match, we need to make sure we don't go out of bounds.
        duplicate_text = examinedwork[a:b] ## get the duplicate text from the examined work.
        print(f"Duplicate Text: {duplicate_text}")

        clean_text = duplicate_text.strip()
        print(f"Trying to find: >>>{clean_text}<<<")
        ## search for duplicate text in cited work now...
        original_loc = search(clean_text,referencework)

        result.append({
            "match_text": duplicate_text,
            "examined_index": a,
            "reference_index": original_loc[0] if original_loc else -1
        })

        # print("Duplicate Text:",duplicate_text,"\n Found at<", loc[0],"> in examined text originally located at <",original_loc[0],"> in reference text.")
    return result



        ## we are now measuring continuous matches, start at choplength (5)
        # for k in range (i+1,len(matches)): ## we loop through the other matches to see if we can extend this match
        #    if 
    #print(ref_tokens)