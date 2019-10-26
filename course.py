#print ("Hello world")
#print ("Hello world"*1000)
#print (1235436*574674)
#print (1235436/574674)

#def odd_even(a,b):
#    if  ((a+b)%2) == 0:
#        return 1
#    else:
#        return -1
#if odd_even (2,3) == 1:
#    print ("Even")
#elif odd_even (2,3) == -1:
#    print ("Odd")


#def str_len (str):
#    if len(str) > 10:
#        print ("The length is:", len(str))

#str_len ("Hello wld")

from flask import Flask
from flask import request
app = Flask(import_name=__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'

#@app.route(rule ='/calc',methods= ['post'])
@app.route(rule ='/calc')
def power():
    x = request.args.get('x')
    return x + " blah " + zubi()
def zubi():
    y = request.args.get('y')
    return y + " zubi"

if __name__ == '__main__':
    app.run()
