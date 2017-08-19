#! /usr/bin/env python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

html = """
<html>
    <body>
        <form method="get" action="">
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
        </from>
        <p>
            Age: %(age)s
            <br>
            Hobbies: %(hobbies)s
        </p>
    </body>
</html>
"""


def application(environ, start_response):
    
    # 解析 QUERY_STRING
    d= parse_qs(environ['QUERY_STRING'])
    
    age = d.get('age', [''])[0] # 返回 age 對應的值
    hobbies = d.get('hobbies', [])# 以 list 形式返回所有的 hobbies
    
    # 防止腳本輸入
    age = escape(age)
    hobbies = [escape(hobby) for hobby in hobbies]

    response_body = html % {
        'checked-software': ('', 'checked')['software' in hobbies],
        'checked-tunning': ('', 'checked')['tunning' in hobbies],
        'age': age or 'Empty',
        'hobbies': ', '.join(hobbies or ['No Hobbies?'])
    }

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length',str(len(response_body)))
    ]    

    start_response(status, response_headers)
    return [response_body]

httpd = make_server('localhost', 8051, application)

# 能夠一直處理請求
httpd.serve_forever()
print 'end'



