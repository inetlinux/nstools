VER=$(shell python -c 'import nstools; print(nstools.version)')
TARGET=nstools-$(VER)-py3-none-any.whl

all:clean
	python setup.py sdist bdist_wheel || true

install:all
	pip install -I --no-deps dist/$(TARGET)

clean:
	python setup.py clean --all
