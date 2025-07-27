#!/usr/bin/env python3
import http.server
import socketserver

httpd = ""

#here you create a new handler, you had a new way to handle get request
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
       #this code execute when a GET request happen, then you have to check if the request happenned because the user pressed the button
        if self.path.find("StartRound=true") != -1:
            print("Button clicked")
            exit()
            #do whatever you want
        return super().do_GET()

PORT = 8000
myHandler = Handler

def exit():
    global httpd
    httpd.shutdown()
    print("shutting down")
    sys.exit()

def main():
    global httpd
    httpd = socketserver.TCPServer(("", PORT), myHandler)
    print("serving at port", PORT)
    httpd.serve_forever()

if __name__ == "__main__":
    main()




#with socketserver.TCPServer(("", PORT), myHandler) as httpd:

