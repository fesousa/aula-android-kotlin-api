
from flask import Flask, jsonify, request
app = Flask(__name__)

disciplinas = [{"id": e, "nome": "Disciplina "+str(e), "ementa":"Ementa "+str(e), "foto":"https://cdn.pixabay.com/photo/2018/01/18/20/42/pencil-3091204_1280.jpg", "professor": "Professor Disciplina "+str(e)} for e in range(1,11)]   

@app.route("/disciplinas", methods=['GET'])
def get():
    return jsonify(disciplinas)

# @app.route("/disciplinas/<int:id>/")
# def get(id):
#     filtro = [e for e in disciplinas if e["id"] == id]
#     if filtro:
#         return jsonify(filtro[0])
#     else:
#         return jsonify({})

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
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/disciplinas/<int:id>/", methods=['DELETE'])
def delete(id):
    global disciplinas
    try:
        disciplinas = [e for e in disciplinas if e["id"] != id]
        return jsonify({"status":"OK"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})


if __name__ == "__main__":
    app.run(host='0.0.0.0')