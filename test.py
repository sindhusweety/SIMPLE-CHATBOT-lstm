from numpy import array
aa = [[[1,2],[0,7]],[[0,8],[0]]]
a = array(aa)
print(a[:,1])
from eSpeak import espeak

def hello_world():
    espeak.synth("Hello World")