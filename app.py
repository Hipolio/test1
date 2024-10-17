from flask import Flask
from flask import render_template, request, jsonify, make_response
import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    con.close()
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

@app.route("/experiencias/guardar", methods=["POST"])
def experienciasGuardar():
    if not con.is_connected():
        con.reconnect()
    
    nombreapellido = request.form["txtNombreApellidoFA"]
    comentario = request.form["txtComentarioFA"]
    calificacion = request.form["txtCalificacionFA"]

    cursor = con.cursor()
    sql = """
        INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion)
        VALUES (%s, %s, %s)
    """
    val = (nombreapellido, comentario, calificacion)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    return f"Nombre y Apellido: {nombreapellido}, Comentario: {comentario}, Calificación: {calificacion}"

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Log, Temperatura, Humedad, DATE_FORMAT(Fecha_Hora, '%d/%m/%Y') AS Fecha, DATE_FORMAT(Fecha_Hora, '%H:%i:%s') AS Hora FROM sensor_log
    ORDER BY Id_Log DESC
    LIMIT 10 OFFSET 0
    """)
    registros = cursor.fetchall()

    con.close()
    return make_response(jsonify(registros))

@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]

    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT Id_Log, Temperatura, Humedad FROM sensor_log
    WHERE Id_Log = %s
    """
    val = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]
    temperatura = request.form["temperatura"]
    humedad = request.form["humedad"]
    fechahora = datetime.datetime.now(pytz.timezone("America/Matamoros"))
    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE sensor_log SET
        Temperatura = %s,
        Humedad = %s
        WHERE Id_Log = %s
        """
        val = (temperatura, humedad, id)
    else:
        sql = """
        INSERT INTO sensor_log (Temperatura, Humedad, Fecha_Hora)
        VALUES (%s, %s, %s)
        """
        val = (temperatura, humedad, fechahora)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    return jsonify({})
