calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]
STOP = {"not", "high"}
def frequencies(texts, stop):
    counts={}
    for text in texts:
        for word in text.split():
            if word not in stop:counts[word]=counts.get(word,0)+1
    return counts
def top(counts, k):
    return sorted(counts.items(),key=lambda pair:(-pair[1],pair[0]))[:k]
print(top(frequencies(calls, STOP), 3))
