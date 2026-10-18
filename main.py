from pathlib import Path
from collections import Counter
import concurrent.futures
import time
import matplotlib.pyplot as plt




folder = Path("texts")
files = list(folder.glob("*.txt"))

print(f"Znaleziono {len(files)} plików")

key_words = ["love", "family", "war", "peace", "time", "woman", "women", "man", "men"]

def analyze_file(file):
    start = time.time()
    words = file.read_text(encoding="utf-8").split()
    words_lower = [word.lower().strip(" .,/!?") for word in words]
    count_words = Counter(words_lower)
    finish_time = time.time()
    return count_words, len(words_lower), round(finish_time - start, 10)

total_keywords = Counter()

start = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(analyze_file, files)

for file, results in zip(files, results):

    counter_words= results[0]
    len_words = results[1]
    key_words_counted = {}
    for word in key_words:
        if word in counter_words:
            key_words_counted[word] = counter_words[word]
        total_keywords[word] += counter_words[word]
    print(f"{file.name}: {len_words}, {key_words_counted}")
print(f"Łącznie: {total_keywords}")

finish_time = time.perf_counter()
print(f"Czas: {round(finish_time - start, 7)}")


'''--------------------- wykres śtednich czasów dla 3 wątków---------'''
threds = [1, 2, 3]
av_time = [0.3828, 0.3758, 0.3781]
total_keywords = {'man': 3276, 'time': 2133, 'men': 1498, 'love': 1161, 'woman': 682, 'war': 421, 'women': 384, 'family': 328, 'peace': 253}
karenina_keys = {'love': 395, 'family': 104, 'war': 24, 'peace': 69, 'time': 533, 'woman': 161, 'women': 115, 'man': 492, 'men': 186}
miserables_keys = {'love': 345, 'family': 90, 'war': 120, 'peace': 77, 'time': 727, 'woman': 367, 'women': 146, 'man': 1775, 'men': 564}
war_peace_keys = {'love': 421, 'family': 134, 'war': 277, 'peace': 107, 'time': 873, 'woman': 154, 'women': 123, 'man': 1009, 'men': 748}



plt.figure(figsize=(16, 9))

plt.subplot(2, 3, 1)
plt.bar(threds, av_time)
plt.xticks(threds)
plt.xlabel("Liczba wątków")
plt.ylabel("Średni czas [s]")
plt.title("Czas przetwarzania")

plt.subplot(2, 3, 2)
plt.bar(key_words, [total_keywords[word] for word in key_words])
plt.xticks(rotation=45, ha="right")
plt.title("Słowa kluczowe — łącznie")

plt.subplot(2, 3, 3)
plt.bar(key_words, [karenina_keys[word] for word in key_words])
plt.xticks(rotation=45, ha="right")
plt.title("Anna Karenina")

plt.subplot(2, 3, 4)
plt.bar(key_words, [miserables_keys[word] for word in key_words])
plt.xticks(rotation=45, ha="right")
plt.title("Les Misérables")

plt.subplot(2, 3, 5)
plt.bar(key_words, [war_peace_keys[word] for word in key_words])
plt.xticks(rotation=45, ha="right")
plt.title("Wojna i pokój")

plt.subplot(2, 3, 6).axis("off")

plt.tight_layout()
plt.show()
