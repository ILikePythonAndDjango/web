#!/usr/bin/env python
# -*- coding: utf-8 -*-

def wsgi_application(environ, start_response):
    data = b"It's worked!"
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return map(
        #Encoding strings in unicode
        lambda string: string.encode("utf-8"),
        map(
            #make array with properties
            lambda string: string + "\n",
            environ["QUERY_STRING"].split("&")
        )
    )
