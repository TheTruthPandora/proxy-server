import requests
from flask import Flask, request, Response
from urllib.parse import urlparse, urlunparse

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    # 获取目标URL
    url = request.args.get('url')
    if not url:
        return Response('Missing URL parameter', status=400)

    # 解析目标URL并获取代理URL
    parsed_url = urlparse(url)
    proxy_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))

    # 获取请求头
    headers = dict(request.headers)
    headers['Host'] = parsed_url.netloc

    # 发送代理请求
    response = requests.request(request.method, proxy_url, headers=headers, params=request.args, data=request.get_data())

    # 返回响应
    return Response(response.content, status=response.status_code, headers=response.headers.items())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)