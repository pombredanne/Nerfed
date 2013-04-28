run:
	gunicorn demo:demo  --pid=gunicorn.pid --log-level debug

reloader:
	watchmedo shell-command --patterns="*.py;*.html;*.css;*.js" --recursive --command='echo "${watch_src_path}" && kill -HUP `cat gunicorn.pid`' .
