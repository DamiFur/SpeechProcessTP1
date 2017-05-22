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
    "-k" : "wav/jmp/diphones/_k_kasAka.wav", 
    "ka" : "wav/jmp/diphones/ka_kasAka.wav",
    "ak" : "wav/jmp/diphones/ak_kasAka.wav",
    "a-" : "wav/jmp/diphones/a__kasAka.wav",
    "as" : "wav/jmp/diphones/as_kasAka.wav",
    "sA" : "wav/jmp/diphones/sA_kasAka.wav",
    "Ak" : "wav/jmp/diphones/Ak_kasAka.wav"
}

resp = AudioSegment.silent()

for phono in ans:
    #w = wave.open(phono, 'rb')
    #data.append( [w.getparams(), w.readframes(w.getnframes())] )
    diphone = AudioSegment.from_wav(diphones_to_wav[phono])
    resp = resp + diphone
    
play(resp)

print(ans)
