import re
a="1a2b3c4d5a6e7s8w9o10a11b12d13d14e15e"

matches = re.findall(r'(\d)([a-zA-Z])', a)
for i in range(1, len(matches)+1):
    print(f"{i//10 + i if i<10 else i//10+i-1} {matches[i-1][1]}", sep="\n")
# print(matches)
