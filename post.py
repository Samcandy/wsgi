#! /usr/bin/env python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

# html 中 from 的 method 是 post

html = """
<html>
<body>
    <form method="post" action="/">
        <p>
            Age: <input type="text" name="age" value="%(age)s">
        </p>
        <p>
            Hobbies:
            <input
                name="hobbies" type="checkbox" value="software"
                %(checked-software)s
            > Software
            <input
                name="hobbies" type="checkbox" value="tunning"
                %(checked-tunning)s
            > Auto Tunning
        </p>
        <p>
            <input type="submit" value="Submit">
        </p>
    </form>
    <p>
        Age: %(age)s<br>
        Hobbies: %(hobbies)s
    </p>
</body>
</html>
"""

def application(environ, start_response):
    
    # CONTENT_LENGTH 可能為空，或者沒有
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)

    # 或取數據
    age = d.get('age',[''])[0]
    hobbies = d.get('hobbies',[])

    # 轉意，防止腳本導入
    age = escape(age)
    hobbies = [escape(hobby) for hobby in hobbies]

    response_body = html % {
        'checked-software': ('','checked')['software' in hobbies],
        'checked-tunning': ('','checked')['tunning' in hobbies],
        'age': age or 'Empty',
        'hobbies': ', '.join(hobbies or ['No Hobbies?'])
    }
    
    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]
    
    start_response(status, response_headers)
    return [response_body]

httpd = make_server('localhost',8051, application)

httpd.serve_forever()

print 'end'

