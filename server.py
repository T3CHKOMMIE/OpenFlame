import http.server
import socketserver
import json
import serial
from urllib.parse import urlparse, parse_qs
import subprocess
from w1thermsensor import W1ThermSensor, Sensor, Unit
import board, neopixel
# Data store (in-memory list of dictionaries)



print("Creating Serial Connection to Logs...")

MAC = "98:D3:51:FE:7E:20" # Replace this with the MAC of your LOG SET (BlueTooth)

cmds =[
["sudo", "rfcomm", "bind", "1" , MAC]
]



for cmd in cmds:
    subprocess.run(cmd)



ser = serial.Serial('/dev/rfcomm1', 9600)
print("Toggling Log Power(booting)!")
ser.write(b'logpower\r')
print("Response: "+str(ser.readline()))




class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        # Parse URL and query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        path = parsed_url.path

        if path == "/api/posts":
            self.do_RES(200, {"Nothing":"To See Here"})

        elif path == "/ledOn":
            try:
                print("Turning LED on!")
                pixels1 = neopixel.NeoPixel(board.D18, 188, brightness=1)
                if "color" in query_params:
                    data = query_params['color'][0].split(",")
                    pixels1.fill((int(data[0]), int(data[1]), int(data[2])))
                else:
                    pixels1.fill((255, 200, 100))
                self.do_RES(200, {"Success": True, "Params": query_params})
            except Exception as E:
                self.do_RES(400, {"Error": str(E)})
                print("Error Turning On LED...\n" + str(E))

        elif path == "/ledOff":
            try:
                print("Turning LED Off!")
                pixels1 = neopixel.NeoPixel(board.D18, 188, brightness=1)
                pixels1.fill((0, 0, 0))
                self.do_RES(200, {"Success": True})
            except Exception as E:
                self.do_RES(400, {"Error": str(E)})
                print("Error Turning Off LED...\n" + str(E))

        elif path == "/temp":
            try:
                print("Getting Temp from GPIO!")
                self.do_RES(200, {"Success": True, "Temp":self.get_temp()})
            except Exception as E:
                self.do_RES(400, {"Error":str(E)})
                print("Error getting temp...\n"+str(E))
        elif path == "/toggleLog":
            try:
                print("Toggling Log Power!")
                ser.write(b'logpower\r')
                print("Response: "+str(ser.readline()))
                self.do_RES(200, {"Success": True})
            except Exception as E:
                self.do_RES(400, {"Error":str(E)})
                print("Error with Log Power...\n"+str(E))
        elif path == "/cycleLog":
            try:
                print("Cycling Log Animation!")
                ser.write(b'logplaypause\r')
                print("Response: "+str(ser.readline()))
                self.do_RES(200, {"Success": True})
            except Exception as E:
                self.do_RES(400, {"Error":str(E)})
                print("Error with Logplaypause...\n"+str(E))
        elif path == "/toggleHeat":
            try:
                print("Toggling Log Heat!")
                ser.write(b'logheat\r')
                print("Response: "+str(ser.readline()))
                self.do_RES(200, {"Success": True})
            except Exception as E:
                self.do_RES(400, {"Error":str(E)})
                print("Error with Toggle Heat...\n"+str(E))
        elif path == "/toggleFlame":
            try:
                print("Toggling Log Flame!")
                ser.write(b'logflame\r')
                print("Response: "+str(ser.readline()))
                self.do_RES(200, {"Success": True})
            except Exception as E:
                self.do_RES(400, {"Error":str(E)})
                print("Error with Toggle Flame...\n"+str(E))
        elif path == "/startMagikFlame":
            try:
                print("Turn On MagikFlame!")
                #subprocess, no need for serial Need to reboot so screen is on, flames start automatically, need to start logpower once after BT and Serial are up.
                subprocess.run(["sudo", "reboot", "now"])
                self.do_RES(200, {"Success": True})
            except Exception as E:
                self.do_RES(400, {"Error":str(E)})
                print("Error booting MagikFlame...\n"+str(E))
        elif path == "/stopMagikFlame":
            try:
                print("Turn Off MagikFlame!")
                #Turnoff screen and logs. 
                #subprocess.Popen(["tvservice", "-o"]) # idont liek this maybe we do vcgencmd display_power 0?
                subprocess.Popen(["vcgencmd", "display_power", "0"]) # idont liek this maybe we do vcgencmd display_power 0?
                ser.write(b'logpower\r')
                print("Response: "+str(ser.readline()))
                self.do_RES(200, {"Success": True})
            except Exception as E:
                self.do_RES(400, {"Error":str(E)})
                print("Error shutting down MagikFlame...\n"+str(E))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        # This is a very basic POST handler
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        new_post = json.loads(post_data)
        
        # Assign a new ID (simplistic)
        new_post["id"] = len(posts) + 1
        posts.append(new_post)
        
        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(new_post).encode("utf-8"))


    def do_RES(self, status, msg):
            self.send_response(status)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(msg).encode("utf-8"))

    def get_temp(self):
        sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="0000055a46b9")
        Tf = round(sensor.get_temperature(Unit.DEGREES_F),1)
        print(str(Tf))
        return Tf





# Run the server
PORT = 8000
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
