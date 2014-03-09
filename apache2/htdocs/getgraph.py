import smtplib

def nextbutton(req, token):
	req.content_type = 'text/html'
	return "test"
#return '<form><button type="submit" formaction="button.py/nextbutton" formmethod="post" formtarget="_parent">You will regret this.</button></form>'