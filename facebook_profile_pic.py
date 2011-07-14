#!/usr/bin/env python
import cgi
import urllib
import base64
import re
print "Content-type: text/html"
print

print '<title>Facebook profile picture</title>'
print '<h1>Facebook profile picture</h1>'
print '<p>A simple way to get your friend profile picture</p>'
print '<hr />'

form = cgi.FieldStorage()
fbid = ''
if 'facebook_id' in form.keys():
	fbid = form['facebook_id'].value

print '<p>'
print '<form action="facebook_profile_pic.py" method="post">'
print '<label for="facebook_id">Username/Id/Url</label>'
print '<input type="text" name="facebook_id" id="facebook_id" value="' + fbid + '" />'
print '<label for="size">Size</label>'
print '<select name="size" id="size">'
print '<option value="small">Small</option>'
print '<option value="normal">Normal</option>'
print '<option selected="selected" value="large">Large</option>'
print '</select>'
print '<input type="submit" value="Get profile pic" />'
print '<form>'
print '</p>'

if fbid:
	if fbid.find('://') != -1:
		fbid = fbid[fbid.rfind('/') + 1:]
		if fbid.find('profile.php?id=') != -1:
			fbid = fbid[15:]
	respond = urllib.urlopen('https://graph.facebook.com/' + fbid)
	data = respond.read()
	respond.close()
	match = re.search('"name":"(.*?)"', data)
	print '<p>'
	if match:
		print '<h3>' + eval('u"' + match.group(1) + '"').encode('utf-8') + '</h3>'
		print '<p>'
		respond = urllib.urlopen('https://graph.facebook.com/' + fbid + '/picture?type=' + form['size'].value)
		print '<img alt="' + fbid + '" src="data:' + respond.info()['Content-Type'] +';base64,' + base64.b64encode(respond.read()) + '" />'
		respond.close()
	else:
		print 'Profile not found!'
	print '</p>'
	
	