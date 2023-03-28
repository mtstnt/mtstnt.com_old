.PHONY = serve
serve:
	source ./local/bin/activate && \
	waitress-serve --port 8080 main:app