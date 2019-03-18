def nlpname(name):
    import urllib2
    import urllib
    import json
    from urllib2 import HTTPError
    from urllib2 import URLError

    sentence = 'Face recognition input ' + name
    phrase= urllib.quote(sentence)
    url = "https://api.dialogflow.com/v1/query?v=20150910&contexts=user_name&lang=en&query="+phrase+"&sessionId=12345&timezone=Asia/Almaty"
    headers = {'Authorization' : 'Bearer YOUR_ACCESS_TOKEN'}
    request = urllib2.Request(url, None, headers)

    try:
        response = urllib2.urlopen(request)
        response1 = response.read()
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print ('Error code: ', e.code)
        nlp_out = 'The server couldn\'t fulfill the request.'
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        nlp_out = 'We failed to reach a server.'
    else:
        jsonobj = json.loads(response1)
        print(jsonobj["result"]["fulfillment"]["speech"])
        nlp_out= jsonobj["result"]["fulfillment"]["speech"]

    return nlp_out

def nlpgreet():
    import urllib2
    import urllib
    import json
    from urllib2 import HTTPError
    from urllib2 import URLError

    sentence = 'Hello'
    phrase= urllib.quote(sentence)
    url = "https://api.dialogflow.com/v1/query?v=20150910&contexts=user_name&lang=en&query="+phrase+"&sessionId=12345&timezone=Asia/Almaty"
    headers = {'Authorization' : 'Bearer YOUR_ACCESS_TOKEN'}
    request = urllib2.Request(url, None, headers)

    try:
        response = urllib2.urlopen(request)
        response1 = response.read()
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print ('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        jsonobj = json.loads(response1)
        print(jsonobj["result"]["fulfillment"]["speech"])

def nlpcall(query):
    import urllib2
    import urllib
    import json
    from urllib2 import HTTPError
    from urllib2 import URLError


    phrase= urllib.quote(query)
    url = "https://api.dialogflow.com/v1/query?v=20150910&contexts=user_name&lang=en&query="+phrase+"&sessionId=12345&timezone=Asia/Almaty"
    headers = {'Authorization' : 'Bearer YOUR_ACCESS_TOKEN'}
    request = urllib2.Request(url, None, headers)

    try:
        response = urllib2.urlopen(request)
        response1 = response.read()
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print ('Error code: ', e.code)
        nlp_outt = 'The server couldn\'t fulfill the request.'
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        nlp_outt = 'We failed to reach a server.'
    else:
        jsonobj = json.loads(response1)
        print(jsonobj["result"]["fulfillment"]["speech"])
        nlp_outt= jsonobj["result"]["fulfillment"]["speech"]

    return nlp_outt