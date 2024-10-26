from collections import defaultdict, Counter


def byte_pair_encoding(corpus, k):
    # Initialize vocabulary with all unique characters in the corpus
    vocab = set(char for word in corpus for char in word)

    # Convert the corpus to a list of tuples (sequence of characters)
    corpus = {tuple(word): count for word, count in corpus.items()}

    for _ in range(k):
        # Step 1: Count pairs of adjacent tokens
        pair_counts = defaultdict(int)
        print("init_paircounts: ",  pair_counts)
        print("corpus_items: ", corpus.items())
        for word, count in corpus.items():
            print("word, count: ", word, count)
            for i in range(len(word) - 1):
                print(f"Before pair_counts[({word[i]}, {word[i + 1]})]: ", pair_counts[(word[i], word[i + 1])])
                print("count: ", count)
                pair_counts[(word[i], word[i + 1])] += count
                print(f"After pair_counts[({word[i]}, {word[i + 1]})]: ", pair_counts[(word[i], word[i + 1])])
                print("pair_counts: ", pair_counts)

        # If no pairs left, break early
        if not pair_counts:
            print("not pair counts")
            break

        # Step 2: Find the most frequent pair of adjacent tokens
        tL, tR = max(pair_counts, key=pair_counts.get)
        print("tL, tR: ", tL, tR)
        print(f"tL, tR:( {tL}, {tR} ) - Count: {pair_counts[(tL, tR)]}")

        # Step 3: Create a new token by concatenating the most frequent pair
        tNEW = tL + tR
        vocab.add(tNEW)

        # Step 4: Replace occurrences of tL, tR with tNEW in the corpus
        new_corpus = {}
        for word, count in corpus.items():
            new_word = []
            i = 0
            while i < len(word):
                if i < len(word) - 1 and (word[i], word[i + 1]) == (tL, tR):
                    new_word.append(tNEW)
                    i += 2  # Skip the next character since it's part of the merged token
                else:
                    new_word.append(word[i])
                    i += 1
            new_corpus[tuple(new_word)] = count

        # Update the corpus
        corpus = new_corpus

    # Return the updated vocabulary
    return vocab


# Given corpus with counts
corpus = {
    "low_": 5,
    "lowest_": 2,
    "newer_": 6,
    "wider_": 3,
    "new_": 2
}

# Number of merges to perform
k = 8

ground_truth = ["_", "d", "e", "i", "l", "n", "o", "r", "s", "t", "w", "er", "er_", "ne", "new", "lo", "low", "newer_", "low_"]
# Run the Byte Pair Encoding algorithm
final_vocab = byte_pair_encoding(corpus, k)
all_exist = all(item in ground_truth for item in final_vocab)
len_same = len(ground_truth) == len(final_vocab)

print("All elements of final_vocab exist in match:", all_exist, len_same)
# Display the final vocabulary
print("Final Vocabulary:", sorted(final_vocab))
