
from flask import Flask, jsonify, request
import json
import urllib.request
import random

app = Flask(__name__)

disciplinas = [{"id": e, "nome": "Disciplina "+str(e), "ementa":"Ementa "+str(e), "foto":"https://cdn.pixabay.com/photo/2018/01/18/20/42/pencil-3091204_1280.jpg", "professor": "Professor Disciplina "+str(e)} for e in range(1,11)]   

@app.route("/disciplinas", methods=['GET'])
def get():
    return jsonify(disciplinas)

@app.route("/disciplinas/<int:id>", methods=['GET'])
def get_one(id):
    filtro = [e for e in disciplinas if e["id"] == id]
    if filtro:
        return jsonify(filtro[0])
    else:
        return jsonify({})

@app.route("/disciplinas", methods=['POST'])
def post():
    global disciplinas
    try:
        content = request.get_json()

        # gerar id
        ids = [e["id"] for e in disciplinas]
        if ids:
            nid = max(ids) + 1
        else:
            nid = 1
        content["id"] = nid
        disciplinas.append(content)
        return jsonify({"status":"OK", "msg":"disciplina adicionada com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/disciplinas/<int:id>", methods=['DELETE'])
def delete(id):
    global disciplinas
    try:
        disciplinas = [e for e in disciplinas if e["id"] != id]
        return jsonify({"status":"OK", "msg":"disciplina removida com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/push/<string:key>/<string:token>", methods=['GET'])
def push(key, token):
	d = random.choice(disciplinas)
	data = {
		"to": token,
		"notification" : {
			"title":d["nome"],
			"body":"Você tem nova atividade em "+d['nome']
		},
		"data" : {
			"disciplinaId":d['id']
		}
	}
	req = urllib.request.Request('http://fcm.googleapis.com/fcm/send')
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization', 'key='+key)
	jsondata = json.dumps(data)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	response = urllib.request.urlopen(req, jsondataasbytes)
	print(response)
	return jsonify({"status":"OK", "msg":"Push enviado"})


if __name__ == "__main__":
    app.run(host='0.0.0.0')