#!/usr/bin/env python
# -*- coding: utf-8 -*-

def wsgi_application(environ, start_response):
    data = environ["QUERY_STRING"].replace('&', '\n').encode('utf-8')
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)

    return iter([data])
