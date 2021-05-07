#
# In this problem, each file describes the weights of vertices in a path graph and has the format:
# [number_of_vertices_in_path_graph]
# [weight of first vertex]
# [weight of second vertex]
# ...
# Test case: (contributed by Logan Travis) What is the value of a maximum-weight independent set of the 10-vertex path graph described in this file, and which vertices belong to the MWIS? (Answer: 2617, and the vertices 2, 4, 7, and 10).
# Challenge data set: Repeat the previous problem for the 1000-vertex path graph described in this file.
#

from functools import lru_cache

def top_down(A):
    N = len(A)
    @lru_cache(maxsize = None)        # 🤔 memo
    def go(i = N - 1):
        if i < 0: return 0            # 🛑 empty set
        if i == 0: return A[0]        # 🛑 single set
        include = go(i - 2) + A[i]    # ✅ include A[i]
        exclude = go(i - 1)           # 🚫 exclude A[i]
        return max(include, exclude)  # 🎯 best
    return go()

def bottom_up(A):
    N = len(A)
    dp = [0] * (N + 1)                  # 🤔 memo
    dp[0] = 0                           # 🛑 empty set
    dp[1] = A[0]                        # 🛑 single set
    for i in range(2, N + 1):
        include = dp[i - 2] + A[i - 1]  # ✅ include A[i] (use A[i - 1] since dp[i] is offset by 1 for explicit 🛑 empty set at index 0, ie. index -1 doesn't exist)
        exclude = dp[i - 1]             # 🚫 exclude A[i]
        dp[i] = max(include, exclude)   # 🎯 best
    return dp[N]

def bottom_up_memopt(A):
    N = len(A)
    a = 0                          # 🤔 memo + 🛑 empty set
    b = A[0]                       # 🤔 memo + 🛑 single set
    c = -1
    for i in range(2, N + 1):
        include = a + A[i - 1]     # ✅ include A[i] (use A[i - 1] since dp[i] is offset by 1 for explicit 🛑 empty set at index 0, ie. index -1 doesn't exist)
        exclude = b                # 🚫 exclude A[i]
        c = max(include, exclude)  # 🎯 best
        a = b; b = c               # 👈 slide window
    return c

def run(filename):
    A = []
    with open(filename) as fin:
        first = True
        while True:
            line = fin.readline()
            if not line:
                break
            x = int(line)
            if not first:
                A.append(x)
            else:
                first = False
                N = x
    a = top_down(A)
    b = bottom_up(A)
    c = bottom_up_memopt(A)
    assert(a == b and b == c) # 💩 sanity check
    print(f'{filename}: {a}')

run('problem16.6test.txt')     # problem16.6test.txt: 2617
run('problem16.6.txt')         # problem16.6.txt: 2955353732
