# Tabla de Contenidos
- [Reto Hackerrank - Time in Words](#Time-in-Words)
- [Conexión con Base de Datos - CRUD](#REST-API-con-Python-Flask-y-MySQL)

# Time in Words
Enunciado del problema:

[Problem Time in Words]  

Solución del problema:



[Solution Time in Words]

## Explicación del código

La función main se ejecuta por defecto, lo primero que se hace es leer 2 números y convertirlos a enteros, estos serán la hora y los minutos.
```python
if __name__ == '__main__':
    h: int = int(input())
    m: int = int(input())
    timeInWords(h=h, m=m)
```

Se llama a la función principal que recibe como parámetros las 2 variables leídas por teclado.
```python
timeInWords(h=h, m=m)
```

Lo primero que hace la función es crear un diccionario, este contiene los números del 1 al 19 y las decenas  20 a 50. Las Llaves del diccionario son los números arábigos y lo valores del diccionario son las letras.
```python
def timeInWords(h: int, m: int) -> str:
    dict = crear_listas()
```


```python
def crear_listas() -> dict[str, str]:

    my_dict_0_19: dict[str, str] = {
        "0": "zero",
        "1": "one",
        "2": "two",     
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",    
        "10": "ten",
        "11": "eleven",  
        "12": "twelve", 
        "13": "thirteen",
        "14": "fourteen",
        "15": "fifteen",
        "16": "sixteen",
        "17": "seventeen",
        "18": "eighteen",
        "19": "nineteen",                                            
    }

    my_dict_decades: dict[str, str] = {
        "20": "twenty",
        "30": "thirty",
        "40": "fourty",
        "50": "fifty",
    }

    return lista_completa(my_dict_decades, my_dict_0_19)
```

La función lista_completa() rellena el resto de Llaves-Valor necesarios.

```python
def lista_completa(my_dict_decades, my_dict_0_19) -> dict[str, str]:    
    dict_0_60: dict[str, str] = {}
    dict_0_60 = dict(dict_0_60, **my_dict_0_19)
    dict_0_60 = dict(dict_0_60, **{"20": "twenty"})

    for j in range(2,6):
        dict_10s = {str(j)+str(i) : my_dict_decades[str(j*10)]+" "+my_dict_0_19[str(i)] for i in range(1,10)}
        dict_0_60 = dict(dict_0_60, **dict_10s)

        if j == 2:
            dict_0_60 = dict(dict_0_60, **{"30": "thirty"})
        elif j == 3:
            dict_0_60 = dict(dict_0_60, **{"40": "fourty"})
        elif j == 4:
            dict_0_60 = dict(dict_0_60, **{"50": "fifty"})
        elif j == 5:
            dict_0_60 = dict(dict_0_60, **{"60": "o\' clock"})        
        else:
            pass

    return dict_0_60
```

Retomando la función principal, se realizan un serie de validaciones para saber cómo imprimir la hora en pantalla:

```python
def timeInWords(h: int, m: int) -> str:
    dict = crear_listas()

    hour: str = dict[str(h)]
    minute: str = dict[str(m)]
    next_hour: str = dict[str(h+1)]
    rest: str = dict[str(60-m)]

    if m == 0:
        print(f'{hour} o\' clock')
    elif m == 1:
        print(f'{minute} minute past {hour}')
    elif m == 15:
        print(f'quarter past {hour}')
    elif m == 45:
        print(f'quarter to {next_hour}')
    elif m < 30:
        print(f'{minute} minutes past {hour}')
    elif m > 30:
        print(f'{rest} minutes to {next_hour}')
    elif m == 30:
        print(f'half past {hour}')
```

[Problem Time in Words]: https://www.hackerrank.com/challenges/the-time-in-words/problem?isFullScreen=true
[Solution Time in Words]: https://github.com/CarlosAlfredoMarin/Problem_Solutions_Hackerrank/blob/main/Time_in_Words.py








# REST API con Python, Flask y MySQL

## Creando el Servidor
Creación del ambiente virtual:
```python
py -m venv venv
.\venv\Scripts\activate
```

Actualizar pip
```python
python.exe -m pip install --upgrade pip
```
En el archivo <a href="https://github.com/CarlosAlfredoMarin/Retos_Cobercy/blob/master/API_flask_MySQL/config.py" target="_blank">config.py</a> se configura que el servidor se actualice por defecto automáticamente, indicamos que somos el usuario raíz, indicamos el nombre de la base de datos creada.

```python
class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_DB = 'api_flaks'

 
config = {
    'development': DevelopmentConfig
}
```

Activar servidor
```python
py .\src\app.py
```

Hasta el momento no hay ninguna respuesta para mostrar al cliente, por eso, se muestra el error 404 (Recurso no encontrado).

Para que el servidor se actualice automáticamente
```python
DEBUG = True
```

En el archivo <a href="https://github.com/CarlosAlfredoMarin/Retos_Cobercy/blob/master/API_flask_MySQL/app.py" target="_blank">app.py</a>

Importamos las librerías necesarias
```python
from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL
```

La función principal lanza el servidor
```python
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
```

Ya tenemos un servidor creado con Python y con Flask. 

Creamos los EndPoints y las funciones del CRUD (Create, Read, Update, Delete)
```python
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
```

Adicionalmente, se crea otra función que utiliza el método GET para listar todos los cursos
```python
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
```





<br>
<br>
<br>

## Instalación XAMPP
Instalé XAMPP como normalmente se instala cualquier programa en Windows.

**Nota:** Apagar el puerto 3306, dado que ya tenía instalado MySQL.





<br>
<br>
<br>

## Creando la Base de Datos
Escribimos en el navegador:
~~~
localhost/phpmyadmin
~~~

**Thunder Client:** Extensión de VS Code para realizar peticiones HTTP. Es equivalente a Postman o Insomnia.

**200:** Código de respuesta cuando todo ha ido bien.


PHPMyAdmin en Opera no permite escribir código SQL.



<br>
<br>
<br>
