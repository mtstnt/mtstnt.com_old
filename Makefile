.PHONY = serve
serve:
	waitress-serve --host 0.0.0.0 --port 8080 main:app