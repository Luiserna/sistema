from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistemahospital'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Esto devuelve los resultados como diccionarios

mysql = MySQL(app)


@app.route('/')
def index():

    sql="SELECT * FROM `registro_paciente`;"
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql)
    registro_paciente=cursor.fetchall()
    print(registro_paciente)
    conn.commit()
    return render_template('empleados/index.html', registro_paciente=registro_paciente)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registro_paciente WHERE id=%s", (id,)) 
    conn.commit()
    return redirect('/') #cuando hace el borrado de redirecciona

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registro_paciente WHERE id=%s", (id,))
    registro_paciente = cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', registro_paciente=registro_paciente)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _ci=request.form['txtCi']
    _edad=request.form['txtEdad']
    _diagnostico=request.form['txtDiagnostico']
    id=request.form['txtID']

    sql="UPDATE registro_paciente SET nombre=%s, ci=%s, edad=%s, diagnostico=%s WHERE id=%s"
    datos=(_nombre, _ci, _edad, _diagnostico, id)
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _ci=request.form['txtCi']
    _edad=request.form['txtEdad']
    _diagnostico=request.form['txtDiagnostico']
    
    sql="INSERT INTO `registro_paciente` (`id`, `nombre`, `ci`, `edad`, `diagnostico`) VALUES (NULL, %s, %s, %s, %s);" #introduce los datos a create

    datos=(_nombre, _ci, _edad, _diagnostico)
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return render_template('empleados/index.html')

if __name__ == '__main__':
    app.run(debug=True)