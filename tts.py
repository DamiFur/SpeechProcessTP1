import sys
import wave

data= []
for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()

output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
output.writeframes(data[0][1])
output.writeframes(data[1][1])
output.close()

inputWord = sys.argv[1]
outputFile = sys.argv[2]
ans = ["-" + inputWord[0]]

for i in range(len(inputWord) - 1):
    ans.append(inputWord[i] + inputWord[i + 1])

ans.append(inputWord[-1] + "-")

for phono in ans:
    w = wave.open(phono, 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()

output = wave.open(outputFile)

print ans
