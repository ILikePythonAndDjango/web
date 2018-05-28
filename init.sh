sudo ln -sf $(pwd)/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo unlink /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
source core/bin/activate
gunicorn -c etc/hello.py --pythonpath $(pwd)/ hello:wsgi_application & 
gunicorn -c etc/gunicorn.py --pythonpath $(pwd)/ask/ ask.wsgi:application
