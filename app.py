from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL



app = Flask(__name__)
conexion = MySQL(app)



@app.route('/cursos', methods=["GET"])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM cursos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []
        for fila in datos:
            curso = {"codigo": fila[0],
                    "nombre": fila[1],
                    "creditos": fila[2]}
            cursos.append(curso)
        return jsonify({"cursos":cursos,"mensaje":"Cursos Listados"})
    except Exception as ex:
        return "Error"



@app.route("/cursos/<codigo>", methods=["GET"])
def leer_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM cursos WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {"codigo": datos[0],
                    "nombre": datos[1],
                    "creditos": datos[2]}
            return jsonify({"curso":curso,"mensaje":"Curso Encontrado"})
        else:
            return jsonify({"mensaje":"Curso NO Encontrado"})
    except Exception as ex:
        return jsonify({"mensaje":"Error"})



@app.route( '/cursos', methods=['POST'])
def registrar_curso():
    try:
        cursor = conexion.connection.cursor()
        
        sql = """INSERT INTO cursos (Codigo, Nombre, Creditos) 
        VALUES ('{0}', '{1}', {2})""".format(
            request.json['Codigo'], 
            request.json['Nombre'], 
            request.json['Creditos'])
        
        cursor.execute(sql)
        conexion.connection.commit() # Confirma la acción de Inserción
        return jsonify({"mensaje":"Curso Registrado"})

    except Exception as ex:
         return jsonify({"mensaje":"Error"})



@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        
        sql = "DELETE FROM cursos WHERE codigo = '{0}'".format(codigo)
        
        cursor.execute(sql)
        conexion.connection.commit() # Confirma la acción de Borrado
        return jsonify({"mensaje":"Curso Eliminado"})

    except Exception as ex:
         return jsonify({"mensaje":"Error"})    



@app.route( '/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        
        sql = """UPDATE cursos SET Nombre='{0}', Creditos = {1}  
        WHERE Codigo = '{2}'""".format(
            request.json['Nombre'],
            request.json['Creditos'],
            codigo)
        
        cursor.execute(sql)
        conexion.connection.commit() # Confirma la acción de Actualización
        return jsonify({"mensaje":"Curso Actualizado"})

    except Exception as ex:
         return jsonify({"mensaje":"Error"})



def pagina_no_encontrada(error):
    return "<h1>La página que buscas no existe parcere.</h1>", 404
    


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
    #app.run(debug=True)