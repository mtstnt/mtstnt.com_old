.PHONY = serve
serve:
	waitress-serve --host 0.0.0.0 main:app