from jmunja import smssend

uid = "vini0420"
upw = "097affdae04ad0a9357177454f4d8a"
subject = "강근우"
content = "바보"
hpno = "01042757895"
callback = "01083562203"

jphone = smssend.JmunjaPhone(uid, upw)
presult = jphone.send(subject, content, hpno)

jweb = smssend.JmunjaWeb(uid, upw)
wresult = jweb.send(subject, content, hpno, callback)

if presult or wresult:
    print("폰문자 %s건, 웹문자 %s건 발송 성공" % (presult, wresult))
else:
    print("발송 실패")