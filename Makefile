repo=fractal-explorer

compile:
	emcc src/Fractal.c src/Simd.c -o src/static/fractal.js -pthread -s EXPORTED_FUNCTIONS=_render_julia_double,_render_mandelbrot_double -s EXPORTED_RUNTIME_METHODS=ccall,cwrap

build: compile
	docker build --platform linux/amd64 -t $(repo) src

run: build
	docker run \
	-p 8000:8000 \
	$(repo)