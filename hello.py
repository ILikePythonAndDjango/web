#!/usr/bin/env python
# -*- coding: utf-8 -*-

def wsgi_application(environ, start_response):
    body = [bytes(i + '\n','utf-8') for i in environ['QUERY_STRING'].split('&')]
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(body)))
    ]
    start_response(status, response_headers)
    
    return body

    #return map(
    #    #Encoding strings in unicode
    #    lambda string: string.encode("utf-8"),
    #    map(
    #        #make array with properties
    #        lambda string: string + "\n",
    #        environ["QUERY_STRING"].split("&")
    #    )
    #)
