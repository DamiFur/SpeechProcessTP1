import sys
import wave
from pydub import AudioSegment
from pydub.playback import play

data= []

inputWord = sys.argv[1]
outputFile = sys.argv[2]
ans = ["-" + inputWord[0]]

for i in range(len(inputWord) - 1):
    ans.append(inputWord[i] + inputWord[i + 1])

ans.append(inputWord[-1] + "-")

diphones_to_wav = {
    "ka" : "wav/jmp/diphones/ka_kasAka.wav"
}

resp = AudioSegment.silent()

for phono in ans:
    #w = wave.open(phono, 'rb')
    #data.append( [w.getparams(), w.readframes(w.getnframes())] )
    diphone = AudioSegment.from_wav(diphones_to_wav["ka"])
    resp = resp + diphone
    
play(resp)

print(ans)
