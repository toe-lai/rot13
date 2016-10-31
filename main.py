#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
				autoescape = True)

def rot(c, encrypt_key):
	A = 65
	Z = 90
	a = 97
	z = 122

	c = ord(c)
	if(c >= A and c <= Z):
		c += encrypt_key
		if(c > Z):
			c = (c - Z - 1) + A
	elif(c >= a and c <= z):
		c += encrypt_key
		if(c > z):
			c = (c - z - 1) + a
	return chr(c)
    	
def get_action_label(s):
	rot = "ROT"
	unrot = "UNROOT"
        label = ""
	if (s == rot):
                return unrot;
	else:
                return rot;    

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		self.render("roter.html", action_label = get_action_label(""))

	def post(self):
                action_label = self.request.get("action_label")
                q = self.request.get("text")
                encrypt_key = 13
                output_result = ""
                for c in q:
                        output_result += rot(c, encrypt_key)
                self.render("roter.html", output = output_result, action_label = get_action_label(action_label))

 
app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
