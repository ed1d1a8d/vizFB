import smtplib

def nextbutton(req):
	req.content_type = 'text/html'
	return "Hello, this is a test."
#return '<form><button type="submit" formaction="button.py/nextbutton" formmethod="post" formtarget="_parent">You will regret this.</button></form>'