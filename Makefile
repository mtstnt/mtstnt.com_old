.PHONY = serve
serve:
	. ./local/bin/activate && \
	pip install -r requirements.txt && \
	waitress-serve --port 8080 main:app &