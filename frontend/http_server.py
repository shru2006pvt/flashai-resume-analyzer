from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            # Process the job description and resume
            job_description = data['jobDescription']
            resume = data['resume']

            # Call the function to process the job description and resume
            results = processjobdescriptionandresume(job_description, resume)

            # Send the response back to the client
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode('utf-8'))
        except Exception as e:
            # Handle any errors that occur during processing
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

def processjobdescriptionandresume(job_description, resume):
    # This is where you would put the code to process the job description and resume
    # For now, just return a dummy result
    return [
        {'name': 'John Doe', 'score': 0.8},
        {'name': 'Jane Doe', 'score': 0.7},
        {'name': 'Bob Smith', 'score': 0.6}
    ]

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting httpd on port 8000...')
    httpd.serve_forever()

from server import run_server

if __name__ == "__main__":
    run_server()