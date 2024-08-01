from jmunja import smssend

uid = "vini0420"
upw = "097affdae04ad0a9357177454f4d8a"

def send_sms(subject, content, hpno, callback):
    jphone = smssend.JmunjaPhone(uid, upw)
    presult = jphone.send(subject, content, hpno)

    jweb = smssend.JmunjaWeb(uid, upw)
    wresult = jweb.send(subject, content, hpno, callback)

    return presult, wresult
