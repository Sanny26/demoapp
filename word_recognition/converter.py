f = open("hindi_final_lookup.txt", 'r')
answer = {}
count = 1
for line in f:
    k= int(line.strip())
    answer[count] = k
    count+=1

f.close()

infile = "input.txt"
outfile = "output.txt"

words = []
with open(infile, 'r') as f:
   for line in f:
        string = ""
        line = line.split()
        for ch in line[2:]:
            if ch!='0':
                string += chr(answer[int(ch)])
        words.append(string)

for word in words:
        print(word)
