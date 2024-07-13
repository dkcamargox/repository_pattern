from flask import Flask, request, make_response
from models.client import Client
from models.source import Source
import json
import uuid
from src.services import SqlAlchemyModels

app = Flask(__name__)
engine_string = "sqlite:///database.sqlite"
models = SqlAlchemyModels()
models.base.set_engine(engine_string)

@app.route("/clients", methods=["GET", "POST"])
def client_controller():
    if request.method == 'GET':
        id = request.args.get("id")
        id_as_uuid = uuid.UUID(id)

        if id:
            return json.dumps(Client.fetch_by_id(id=id_as_uuid).as_dict())
        else:
            return json.dumps([])
    if request.method == 'POST':
        Client(
            code=request.form.get('code'),
            name=request.form.get('name'),
            status=request.form.get('status')    
        ).register()
        return "ok"

@app.route("/sources", methods=["GET", "POST"])
def source_controller():
    if request.method == 'GET':
        id = request.args.get("id")
        id_as_uuid = uuid.UUID(id)

        if id:
            return json.dumps(Source.fetch_by_id(id=id_as_uuid).as_dict())
        else:
            return json.dumps([])
    if request.method == 'POST':
        Source(
            type=request.form.get("type"),
            name=request.form.get("name"),
            status=request.form.get("status"),
            frequency=request.form.get("frequency"),
            notes=request.form.get("notes")
        ).register()
        return "ok"
            
    


if __name__ == "__main__":
    app.run(
        host="localhost",
        port=3000
    )