def texttospeech(nlp_output):
    print nlp_output
    import pyttsx
    engine= pyttsx.init()
    print "after init"
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')

    engine.setProperty('rate', rate-40)
    engine.setProperty('voice', voices[5].id)
    engine.setProperty('voice', 'english+f2')
    print "before say"
    engine.say(nlp_output)
    engine.runAndWait()
    print "done"
