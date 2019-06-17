VER=$(shell python3 -c 'import nstools; print(nstools.version)')
TARGET=nstools-$(VER)-py3-none-any.whl

all:clean
	python3 setup.py sdist bdist_wheel || true

install:all
	pip3 install -I --no-deps dist/$(TARGET)

clean:
	python3 setup.py clean --all
