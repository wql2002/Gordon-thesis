import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class MinimalHTTPServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # 设置文件大小为1MB
        file_size = 1 * 1024 * 1024
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.end_headers()

        # 创建一个1MB的文件内容
        file_content = os.urandom(file_size)

        # 发送文件内容
        self.wfile.write(file_content)

def run(server_class=HTTPServer, handler_class=MinimalHTTPServer, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()