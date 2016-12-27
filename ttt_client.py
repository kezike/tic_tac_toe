import httplib, urllib
import BaseHTTPServer

# server_host = "https://kayode-ezike.chatly.io"
server_host = "/kayode-ezike-ttt.herokuapp.com"
server_port = 8000
verification_token = "OTibeqhO18dvugBdlI3eCNHx"

class TTT_Client(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_POST(self, request, ttt_host):
    params = urllib.urlencode({"response_type": "in_channel"})
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(ttt_host)
    conn.request("POST", "", params, headers)
    response = conn.getresponse()
    print response.output()

client = TTT_Client()
request = {form:{token:"OTibeqhO18dvugBdlI3eCNHx", command:"/ttt", text:"display"}}
if __name__ == "__main__":
  client.do_POST(request, server_host)

