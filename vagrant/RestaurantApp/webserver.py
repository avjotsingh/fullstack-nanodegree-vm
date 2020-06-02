from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

class WebServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurants = session.query(Restaurant).all()
				output = ""
				output += "<html><body>"
				output += "<h2><a href = '/restaurants/new'>Make a New Restaurant</a></h2>"
				for restaurant in restaurants:
					output += '%s' %restaurant.name
					output += "<br/>"
					output += "<a href = '/restaurant/%s/edit'>Edit</a>" %restaurant.id
					output += "<br/>"
					output += "<a href = '/restaurant/%s/delete'>Delete</a>" %restaurant.id
					output += "<br/>"
					output += "<br/>"
				output += "</body></html>"
				self.wfile.write(output)
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurants = session.query(Restaurant).all()
				output = ""
				output += "<html><body>"
				output += "<h2>Make a New Restaurant</h2>"
				output += "<form method = 'POST' action = '/restaurants/new' enctype = 'multipart/form-data'>"
				output += "<input type = 'text' name = 'restaurant_name' placeholder = 'New Restaurant name'>"
				output += "<button type = 'submit value = 'Submit'>Create</button>"
				output += "</form>"
				output += "</body></html>"
				self.wfile.write(output)
				return

			if self.path.startswith("/restaurant") and self.path.endswith("/edit"):
				restaurant_id = self.path.split('/')[2]
				restaurant = session.query(Restaurant).filter_by(id = int(restaurant_id)).one()

				output = ""
				output += "<html><body>"
				output += "<h2>%s</h2>" %restaurant.name
				output += "<form method = 'POST' action = '/restaurant/%s/edit' enctype = 'multipart/form-data'>" %restaurant.id
				output += "<input type = 'text' name = 'restaurant_name' placeholder = 'Enter new name'>"
				output += "<button type = 'submit' value = 'Submit'>Rename</button>"
				output += "</form>"
				output += "</body></html>"

				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write(output)
				return

			if self.path.startswith("/restaurant") and self.path.endswith("/delete"):
				restaurant_id = self.path.split('/')[2]
				restaurant = session.query(Restaurant).filter_by(id = int(restaurant_id)).one()

				output = ""
				output += "<html><body>"
				output += "<h2>Are you sure you want to delete %s?</h2>" %restaurant.name
				output += "<br/>"
				output += "<form method = 'POST' action = '/restaurant/%s/delete' enctype = 'multipart/form-data'>" %restaurant.id
				output += "<input type = 'submit' value = 'Confirm'>"
				output += "</form>"
				output += "</body></html>"

				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write(output)
				return

			if self.path.endswith("/hello"):
				self.send_response(200);
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h2>Hello!</h2>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				return
			
			if self.path.endswith("/hola"):
				self.send_response(200);
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h2>&#161Hola!</h2>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				return
		except Exception as e:
			print e

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
				if ctype == 'multipart/form-data':
					message = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = message.get('restaurant_name')

				restaurant = Restaurant(name = messagecontent[0])
				session.add(restaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return

			if self.path.startswith("/restaurant") and self.path.endswith("/edit"):
				restaurant_id = self.path.split('/')[2]
				restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('restaurant_name')

				restaurant.name = messagecontent[0]
				session.add(restaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return

			if self.path.startswith("/restaurant") and self.path.endswith("/delete"):
				restaurant_id = self.path.split('/')[2]
				restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
				session.delete(restaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return

			if self.path.endswith("/hello"):
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				print ctype
				print pdict
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				output = ""
				output += "<html><body>"
				output += "<h2>Okay, how about this?</h2>"
				output += "<h1>%s</h1>" %messagecontent[0]
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				return

		except Exception as e:
			print e
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', 8080), WebServerHandler)
		print "Web server running on port %s" %port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C pressed, shutting down the server"
		server.socket.close()

if __name__ == "__main__":
	main()