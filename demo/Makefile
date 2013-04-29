run:
	gunicorn demo:demo  --pid=gunicorn.pid --log-level debug

reloader:
	watchmedo shell-command --patterns="*.py;*.html;*.css;*.js" --recursive --command='echo "${watch_src_path}" && kill -HUP `cat gunicorn.pid`' .

serve_static_files:
	tproxy serve_static_files.py -b 127.0.0.1:8001
