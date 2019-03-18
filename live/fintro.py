import ftexttospeech
from time import sleep


Text0= "Hi everyone"
Text1= "welcome to the department of electronic and telecommunication engineering"
Text2 = "I m deyvi"
Text3= "the first ever robot receptionist in Sri Lanka."
Text4= "I can show you directions around the department."
Text5 = "It's my pleasure to know you all"
Text6 ="and please feel free to have a chat with me"
Text7 = "Thank you."

def intros():
    sleep(4)
    ftexttospeech.texttospeech(Text0)
    sleep(1.5)
    ftexttospeech.texttospeech(Text1)
    sleep(1)
    ftexttospeech.texttospeech(Text2)
    sleep(1.5)
    ftexttospeech.texttospeech(Text3)
    sleep(1)
    ftexttospeech.texttospeech(Text4)
    sleep(1.5)
    ftexttospeech.texttospeech(Text5)
    sleep(1)
    ftexttospeech.texttospeech(Text6)
