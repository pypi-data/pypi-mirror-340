from wibe import wibe

path = "data\sample_js1on.json"
data = wibe.read_json(path)

path = "data\sample.txt"
data = wibe.read_txt(path)

path = r"data\sample.txt"
data = wibe.read_pdf(path=path, method=True)

