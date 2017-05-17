import sys

input = sys.argv[1]
ans = ["-" + input[0]]

for i in range(len(input) - 1):
    ans.append(input[i] + input[i + 1])

ans.append(input[-1] + "-")

print ans
