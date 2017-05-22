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
    "-k" : "wav/jmp/diphones/_k_kas_aka.wav", 
    "ka" : "wav/jmp/diphones/ka_kas_aka.wav",
    "ak" : "wav/jmp/diphones/ak_p_alaka.wav",
    "a-" : "wav/jmp/diphones/a__kas_aka.wav",
    "as" : "wav/jmp/diphones/as_kas_aka.wav",
    "sA" : "wav/jmp/diphones/sA_kas_aka.wav",
    "Ak" : "wav/jmp/diphones/Ak_kas_aka.wav",
    "-s" : "wav/jmp/diphones/_s_sak_ala.wav",
    "kA" : "wav/jmp/diphones/kA_sak_ala.wav",
    "-m" : "wav/jmp/diphones/_m_map_ala.wav",
    "mA" : "wav/jmp/diphones/mA_m_apala.wav",
    "Ap" : "wav/jmp/diphones/Ap_m_apala.wav",
    "pa" : "wav/jmp/diphones/pa_m_apala.wav",
    "al" : "wav/jmp/diphones/al_m_apala.wav",
    "la" : "wav/jmp/diphones/la_m_apala.wav",
    "ma" : "wav/jmp/diphones/ma_map_ala.wav",
    "ap" : "wav/jmp/diphones/ap_map_ala.wav",
    "pA" : "wav/jmp/diphones/pA_map_ala.wav",
    "Al" : "wav/jmp/diphones/Al_map_ala.wav",
    "-p" : "wav/jmp/diphones/_p_p_alaka.wav",
    "lA" : "wav/jmp/diphones/lA_pal_aka.wav",
    "am" : "wav/jmp/diphones/am_pam_asa.wav",
    "sa" : "wav/jmp/diphones/sa_pam_asa.wav",
    "As" : "wav/jmp/diphones/As_pam_asa.wav",
    "Am" : "wav/jmp/diphones/Am_p_amasa.wav",
    "A-" : "wav/jmp/diphones/A__pamas_a.wav",
    "-l" : "wav/jmp/diphones/_l_lam_asa.wav",

}

resp = AudioSegment.silent()

for phono in ans:
    #w = wave.open(phono, 'rb')
    #data.append( [w.getparams(), w.readframes(w.getnframes())] )
    diphone = AudioSegment.from_wav(diphones_to_wav[phono])
    resp = resp + diphone
    
play(resp)

print(ans)
