# Local build with default "/" basepath
python3 src/main.py "/"
cd docs && python3 -m http.server 8888