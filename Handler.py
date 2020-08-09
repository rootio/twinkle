#!/usr/bin/python
import sys
from json import loads
import os
import socket


def talk_to_rootio(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))
    s.send(str(message))
    return s.recv(1024)


if "TWINKLE_TRIGGER" not in os.environ:
    print "end"
    sys.exit()

if os.environ["TWINKLE_TRIGGER"] == "in_call":
    try:
        message = {'event_type': 'call_ringing', 'from': os.environ["SIP_FROM_USER"], 'to': os.environ["SIP_TO_USER"], 'key': sys.argv[3]}
        response = talk_to_rootio(message)
        json_response = loads(response)
        if json_response["status"] == "ok":
            print "action=autoanswer"
        else:
            print "action=reject"
    except Exception as e:
        print e
        print "action=reject"
    sys.exit()

elif os.environ["TWINKLE_TRIGGER"] == "in_call_answered":
    try:
        message = {'event_type': 'call_answer', 'from': os.environ["SIP_FROM_USER"], 'to': os.environ["SIP_TO_USER"], 'key': sys.argv[3]}
        response = talk_to_rootio(message)
        json_response = loads(response)
        print "action=continue"
    except:
        print "end"
    sys.exit()

elif os.environ["TWINKLE_TRIGGER"] in ["in_call_failed", "local_release", "remote_release"]:
    try:
        message = {'event_type': 'call_release', 'from': os.environ["SIP_FROM_USER"], 'to': os.environ["SIP_TO_USER"], 'key': sys.argv[3]}
        response = talk_to_rootio(message)
        json_response = loads(response)
        print "end"
    except:  # perhaps log it
        print "end"
    sys.exit()

else:  # Hail Mary
    print "action=reject"
    print "end"
    sys.exit()


