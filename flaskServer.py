from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from cassandra.cluster import Cluster

app = Flask(__name__)

swagger = Swagger(
    app,
    template={
        "info": {
            "title": "ETL and Streaming Data Pipeline API",
            "description": "This API provides endpoints to interact with the data stored in Cassandra as part of the ETL and streaming data pipeline. It includes operations for counting, retrieving, adding, updating, and deleting user data.",
            "version": "1.0.0",
        }
    },
)


def create_cassandra_session():
    cluster = Cluster(["localhost"])
    session = cluster.connect("spark_streams")
    return session


@app.route("/count", methods=["GET"])
@swag_from(
    {
        "responses": {
            200: {
                "description": "Number of rows in the user_stream table",
                "schema": {
                    "type": "object",
                    "properties": {"count": {"type": "integer"}},
                },
            }
        }
    }
)
def count_rows():
    session = create_cassandra_session()
    count_query = "SELECT COUNT(*) FROM user_stream;"
    count_result = session.execute(count_query)
    count = count_result.one()[0]
    return jsonify(count=count)


@app.route("/first-five", methods=["GET"])
@swag_from(
    {
        "responses": {
            200: {
                "description": "First five rows from the user_stream table",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "gender": {"type": "string"},
                            "dob": {"type": "string"},
                            "address": {"type": "string"},
                            "post_code": {"type": "string"},
                            "email": {"type": "string"},
                            "username": {"type": "string"},
                            "registered_date": {"type": "string"},
                            "phone": {"type": "string"},
                            "picture": {"type": "string"},
                        },
                    },
                },
            }
        }
    }
)
def first_five_rows():
    session = create_cassandra_session()
    select_query = "SELECT * FROM user_stream LIMIT 5;"
    rows = session.execute(select_query)
    result = []
    for row in rows:
        result.append(
            {
                "id": row.id,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "gender": row.gender,
                "dob": row.dob,
                "address": row.address,
                "post_code": row.post_code,
                "email": row.email,
                "username": row.username,
                "registered_date": row.registered_date,
                "phone": row.phone,
                "picture": row.picture,
            }
        )
    return jsonify(result)


@app.route("/add-user", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "gender": {"type": "string"},
                        "dob": {"type": "string"},
                        "address": {"type": "string"},
                        "post_code": {"type": "string"},
                        "email": {"type": "string"},
                        "username": {"type": "string"},
                        "registered_date": {"type": "string"},
                        "phone": {"type": "string"},
                        "picture": {"type": "string"},
                    },
                },
            }
        ],
        "responses": {
            200: {
                "description": "User added successfully",
                "schema": {
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                },
            }
        },
    }
)
def add_user():
    session = create_cassandra_session()
    user_data = request.json
    insert_query = """
    INSERT INTO user_stream (id, first_name, last_name, gender, dob, address, post_code, email, username, registered_date, phone, picture)
    VALUES (%(id)s, %(first_name)s, %(last_name)s, %(gender)s, %(dob)s, %(address)s, %(post_code)s, %(email)s, %(username)s, %(registered_date)s, %(phone)s, %(picture)s)
    """
    session.execute(insert_query, user_data)
    return jsonify(message="User added successfully")


@app.route("/update-user/<user_id>", methods=["PUT"])
@swag_from(
    {
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "type": "string",
                "required": True,
            },
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "gender": {"type": "string"},
                        "dob": {"type": "string"},
                        "address": {"type": "string"},
                        "post_code": {"type": "string"},
                        "email": {"type": "string"},
                        "username": {"type": "string"},
                        "registered_date": {"type": "string"},
                        "phone": {"type": "string"},
                        "picture": {"type": "string"},
                    },
                },
            },
        ],
        "responses": {
            200: {
                "description": "User updated successfully",
                "schema": {
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                },
            }
        },
    }
)
def update_user(user_id):
    session = create_cassandra_session()
    update_data = request.json
    update_query = """
    UPDATE user_stream SET first_name=%(first_name)s, last_name=%(last_name)s, gender=%(gender)s, dob=%(dob)s, address=%(address)s,
    post_code=%(post_code)s, email=%(email)s, username=%(username)s, registered_date=%(registered_date)s, phone=%(phone)s, picture=%(picture)s
    WHERE id=%(id)s
    """
    update_data["id"] = user_id
    session.execute(update_query, update_data)
    return jsonify(message="User updated successfully")


@app.route("/delete-user/<user_id>", methods=["DELETE"])
@swag_from(
    {
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "type": "string",
                "required": True,
            }
        ],
        "responses": {
            200: {
                "description": "User deleted successfully",
                "schema": {
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                },
            }
        },
    }
)
def delete_user(user_id):
    session = create_cassandra_session()
    delete_query = "DELETE FROM user_stream WHERE id=%s"
    session.execute(delete_query, (user_id,))
    return jsonify(message="User deleted successfully")


@app.route("/get-user/<user_id>", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "type": "string",
                "required": True,
                "description": "The ID of the user to retrieve",
            }
        ],
        "responses": {
            200: {
                "description": "Get user details by ID",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "gender": {"type": "string"},
                        "dob": {"type": "string"},
                        "address": {"type": "string"},
                        "post_code": {"type": "string"},
                        "email": {"type": "string"},
                        "username": {"type": "string"},
                        "registered_date": {"type": "string"},
                        "phone": {"type": "string"},
                        "picture": {"type": "string"},
                    },
                },
            },
            404: {
                "description": "User not found",
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"},
                    },
                },
            },
        },
    }
)
def get_user(user_id):
    session = create_cassandra_session()
    select_query = "SELECT * FROM user_stream WHERE id=%s"
    row = session.execute(select_query, (user_id,)).one()
    if row:
        result = {
            "id": row.id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "gender": row.gender,
            "dob": row.dob,
            "address": row.address,
            "post_code": row.post_code,
            "email": row.email,
            "username": row.username,
            "registered_date": row.registered_date,
            "phone": row.phone,
            "picture": row.picture,
        }
        return jsonify(result)
    else:
        return jsonify(message="User not found"), 404


@app.route("/search-user", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "first_name",
                "in": "query",
                "type": "string",
                "required": True,
            }
        ],
        "responses": {
            200: {
                "description": "Search users by first name",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "gender": {"type": "string"},
                            "dob": {"type": "string"},
                            "address": {"type": "string"},
                            "post_code": {"type": "string"},
                            "email": {"type": "string"},
                            "username": {"type": "string"},
                            "registered_date": {"type": "string"},
                            "phone": {"type": "string"},
                            "picture": {"type": "string"},
                        },
                    },
                },
            }
        },
    }
)
def search_user():
    session = create_cassandra_session()
    first_name = request.args.get("first_name")
    select_query = "SELECT * FROM user_stream WHERE first_name=%s ALLOW FILTERING"
    rows = session.execute(select_query, (first_name,))
    result = []
    for row in rows:
        result.append(
            {
                "id": row.id,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "gender": row.gender,
                "dob": row.dob,
                "address": row.address,
                "post_code": row.post_code,
                "email": row.email,
                "username": row.username,
                "registered_date": row.registered_date,
                "phone": row.phone,
                "picture": row.picture,
            }
        )
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
