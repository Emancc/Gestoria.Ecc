from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = 'mi_super_secreto_12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/gestoria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelos de base de datos
class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    lugar_compra = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    patente = db.Column(db.String(20), unique=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Gestoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    patente = db.Column(db.String(20), nullable=False)
    papeles_recibidos = db.Column(db.Text, nullable=False)
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class EntregaPapeles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    patente = db.Column(db.String(20), nullable=False)
    fecha_entrega = db.Column(db.Date, nullable=False)
    documentacion_entregada = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class PapelesRetirar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    patente = db.Column(db.String(20), nullable=False)
    lugar_registro = db.Column(db.String(100), nullable=False)
    fecha_presentacion = db.Column(db.Date, nullable=False)
    comentarios = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

# Función para verificar conexión a la base de datos
def check_db_connection():
    """Verificar conexión a la base de datos"""
    try:
        with app.app_context():
            # Intentar una consulta simple
            db.session.execute(db.text('SELECT 1'))
            print("✅ Conexión a MySQL exitosa")
            print("🗄️  Base de datos: gestoria")
            print("👤 Usuario: root (sin contraseña)")
            return True
    except Exception as e:
        print(f"❌ Error de conexión a MySQL: {e}")
        print("🔧 Verifica que:")
        print("   - MySQL esté ejecutándose")
        print("   - La base de datos 'gestoria' exista")
        print("   - El usuario 'root' tenga permisos")
        return False

@app.route('/')
def index():
    return redirect(url_for('vehiculos'))

@app.route('/vehiculos')
def vehiculos():
    try:
        # Obtener parámetros de filtro
        cliente_filter = request.args.get('cliente', '')
        patente_filter = request.args.get('patente', '')
        
        # Construir consulta base
        query = Vehiculo.query
        
        # Aplicar filtros si están presentes
        if cliente_filter:
            query = query.filter(Vehiculo.cliente.ilike(f'%{cliente_filter}%'))
        if patente_filter:
            query = query.filter(Vehiculo.patente.ilike(f'%{patente_filter.upper()}%'))
        
        # Ordenar por fecha de creación (más reciente primero)
        vehiculos_list = query.order_by(Vehiculo.fecha_creacion.desc()).all()
        
        return render_template('vehiculos.html', 
                             vehiculos=vehiculos_list, 
                             cliente_filter=cliente_filter, 
                             patente_filter=patente_filter)
    except Exception as e:
        flash(f'Error al cargar vehículos: {str(e)}', 'error')
        return render_template('vehiculos.html', vehiculos=[], cliente_filter='', patente_filter='')

@app.route('/vehiculos/agregar', methods=['POST'])
def agregar_vehiculo():
    if request.method == 'POST':
        try:
            cliente = request.form['cliente']
            modelo = request.form['modelo']
            lugar_compra = request.form['lugar_compra']
            color = request.form['color']
            patente = request.form['patente'].upper()
            
            # Verificar si la patente ya existe
            if Vehiculo.query.filter_by(patente=patente).first():
                flash('La patente ya existe en el sistema', 'error')
            else:
                nuevo_vehiculo = Vehiculo(
                    cliente=cliente,
                    modelo=modelo,
                    lugar_compra=lugar_compra,
                    color=color,
                    patente=patente
                )
                db.session.add(nuevo_vehiculo)
                db.session.commit()
                flash('Vehículo agregado exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar vehículo: {str(e)}', 'error')
        
        return redirect(url_for('vehiculos'))

@app.route('/vehiculos/eliminar/<int:id>')
def eliminar_vehiculo(id):
    try:
        vehiculo = Vehiculo.query.get_or_404(id)
        db.session.delete(vehiculo)
        db.session.commit()
        flash('Vehículo eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar vehículo: {str(e)}', 'error')
    
    return redirect(url_for('vehiculos'))

@app.route('/gestoria')
def gestoria():
    try:
        # Obtener parámetros de filtro
        cliente_filter = request.args.get('cliente', '')
        patente_filter = request.args.get('patente', '')
        
        # Construir consulta base
        query = Gestoria.query
        
        # Aplicar filtros si están presentes
        if cliente_filter:
            query = query.filter(Gestoria.cliente.ilike(f'%{cliente_filter}%'))
        if patente_filter:
            query = query.filter(Gestoria.patente.ilike(f'%{patente_filter.upper()}%'))
        
        # Ordenar por fecha de creación (más reciente primero)
        gestoria_list = query.order_by(Gestoria.fecha_creacion.desc()).all()
        
        return render_template('gestoria.html', 
                             gestoria_list=gestoria_list, 
                             cliente_filter=cliente_filter, 
                             patente_filter=patente_filter)
    except Exception as e:
        flash(f'Error al cargar gestoría: {str(e)}', 'error')
        return render_template('gestoria.html', gestoria_list=[], cliente_filter='', patente_filter='')

@app.route('/gestoria/agregar', methods=['POST'])
def agregar_gestoria():
    if request.method == 'POST':
        try:
            cliente = request.form['cliente']
            patente = request.form['patente'].upper()
            papeles_recibidos = request.form['papeles_recibidos']
            observaciones = request.form['observaciones']
            
            nueva_gestoria = Gestoria(
                cliente=cliente,
                patente=patente,
                papeles_recibidos=papeles_recibidos,
                observaciones=observaciones
            )
            db.session.add(nueva_gestoria)
            db.session.commit()
            flash('Gestoría agregada exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar gestoría: {str(e)}', 'error')
        
        return redirect(url_for('gestoria'))

@app.route('/gestoria/eliminar/<int:id>')
def eliminar_gestoria(id):
    try:
        gestoria = Gestoria.query.get_or_404(id)
        db.session.delete(gestoria)
        db.session.commit()
        flash('Gestoría eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar gestoría: {str(e)}', 'error')
    
    return redirect(url_for('gestoria'))

@app.route('/entrega-papeles')
def entrega_papeles():
    try:
        # Obtener parámetros de filtro
        cliente_filter = request.args.get('cliente', '')
        patente_filter = request.args.get('patente', '')
        
        # Construir consulta base
        query = EntregaPapeles.query
        
        # Aplicar filtros si están presentes
        if cliente_filter:
            query = query.filter(EntregaPapeles.cliente.ilike(f'%{cliente_filter}%'))
        if patente_filter:
            query = query.filter(EntregaPapeles.patente.ilike(f'%{patente_filter.upper()}%'))
        
        # Ordenar por fecha de creación (más reciente primero)
        entrega_list = query.order_by(EntregaPapeles.fecha_creacion.desc()).all()
        
        return render_template('entrega_papeles.html', 
                             entrega_list=entrega_list, 
                             cliente_filter=cliente_filter, 
                             patente_filter=patente_filter)
    except Exception as e:
        flash(f'Error al cargar entregas: {str(e)}', 'error')
        return render_template('entrega_papeles.html', entrega_list=[], cliente_filter='', patente_filter='')

@app.route('/entrega-papeles/agregar', methods=['POST'])
def agregar_entrega():
    if request.method == 'POST':
        try:
            cliente = request.form['cliente']
            patente = request.form['patente'].upper()
            fecha_entrega = datetime.strptime(request.form['fecha_entrega'], '%Y-%m-%d').date()
            documentacion_entregada = request.form['documentacion_entregada']
            
            nueva_entrega = EntregaPapeles(
                cliente=cliente,
                patente=patente,
                fecha_entrega=fecha_entrega,
                documentacion_entregada=documentacion_entregada
            )
            db.session.add(nueva_entrega)
            db.session.commit()
            flash('Entrega de papeles agregada exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar entrega: {str(e)}', 'error')
        
        return redirect(url_for('entrega_papeles'))

@app.route('/entrega-papeles/eliminar/<int:id>')
def eliminar_entrega(id):
    try:
        entrega = EntregaPapeles.query.get_or_404(id)
        db.session.delete(entrega)
        db.session.commit()
        flash('Entrega de papeles eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar entrega: {str(e)}', 'error')
    
    return redirect(url_for('entrega_papeles'))

@app.route('/datos/exportar')
def exportar_datos():
    """Exportar todos los datos a un formato legible"""
    try:
        vehiculos_count = Vehiculo.query.count()
        gestoria_count = Gestoria.query.count()
        entrega_count = EntregaPapeles.query.count()
        total_registros = vehiculos_count + gestoria_count + entrega_count
        
        flash(f'Datos exportados: {total_registros} registros totales (Vehículos: {vehiculos_count}, Gestoría: {gestoria_count}, Entregas: {entrega_count})', 'success')
        return redirect(url_for('vehiculos'))
    except Exception as e:
        flash(f'Error al exportar datos: {str(e)}', 'error')
        return redirect(url_for('vehiculos'))

@app.route('/datos/limpiar')
def limpiar_datos():
    """Limpiar todos los datos (solo para desarrollo)"""
    try:
        # Eliminar todos los registros
        Vehiculo.query.delete()
        Gestoria.query.delete()
        EntregaPapeles.query.delete()
        db.session.commit()
        
        flash('Todos los datos han sido limpiados de la base de datos', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al limpiar datos: {str(e)}', 'error')
    
    return redirect(url_for('vehiculos'))

@app.route('/api/vehiculos')
def api_vehiculos():
    """API para obtener vehículos para autocompletado"""
    try:
        # Obtener todos los vehículos con cliente y patente
        vehiculos = Vehiculo.query.with_entities(
            Vehiculo.cliente, 
            Vehiculo.patente
        ).all()
        
        # Convertir a formato JSON
        vehiculos_data = [
            {
                'cliente': vehiculo.cliente,
                'patente': vehiculo.patente
            }
            for vehiculo in vehiculos
        ]
        
        return {'success': True, 'vehiculos': vehiculos_data}
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500

@app.route('/api/vehiculo/<patente>')
def api_vehiculo_por_patente(patente):
    """API para obtener información de un vehículo por patente"""
    try:
        vehiculo = Vehiculo.query.filter_by(patente=patente.upper()).first()
        
        if vehiculo:
            return {
                'success': True, 
                'vehiculo': {
                    'cliente': vehiculo.cliente,
                    'patente': vehiculo.patente,
                    'modelo': vehiculo.modelo,
                    'color': vehiculo.color
                }
            }
        else:
            return {'success': False, 'error': 'Vehículo no encontrado'}, 404
            
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500

@app.route('/papeles_retirar')
def papeles_retirar():
    # Obtener parámetros de búsqueda
    cliente_filter = request.args.get('cliente', '')
    lugar_filter = request.args.get('lugar', '')
    patente_filter = request.args.get('patente', '')
    
    # Construir consulta con filtros
    query = PapelesRetirar.query.order_by(PapelesRetirar.fecha_presentacion.desc())
    
    if cliente_filter:
        query = query.filter(PapelesRetirar.cliente.ilike(f'%{cliente_filter}%'))
    if lugar_filter:
        query = query.filter(PapelesRetirar.lugar_registro.ilike(f'%{lugar_filter}%'))
    if patente_filter:
        query = query.filter(PapelesRetirar.patente.ilike(f'%{patente_filter}%'))
    
    registros = query.all()
    return render_template('papeles_retirar.html', 
                         registros=registros, 
                         cliente_filter=cliente_filter, 
                         lugar_filter=lugar_filter,
                         patente_filter=patente_filter,
                         now=datetime.utcnow())

@app.route('/agregar_papeles_retirar', methods=['POST'])
def agregar_papeles_retirar():
    try:
        # Obtener datos del formulario
        cliente = request.form['cliente'].strip()
        patente = request.form['patente'].strip().upper()
        lugar_registro = request.form['lugar_registro'].strip()
        fecha_presentacion = datetime.strptime(request.form['fecha_presentacion'], '%Y-%m-%d').date()
        comentarios = request.form.get('comentarios', '').strip()
        
        # Validar campos obligatorios
        if not cliente or not patente or not lugar_registro or not fecha_presentacion:
            flash('Por favor complete todos los campos obligatorios', 'danger')
            return redirect(url_for('papeles_retirar'))
        
        # Crear nuevo registro
        nuevo_registro = PapelesRetirar(
            cliente=cliente,
            patente=patente,
            lugar_registro=lugar_registro,
            fecha_presentacion=fecha_presentacion,
            comentarios=comentarios if comentarios else None
        )
        
        db.session.add(nuevo_registro)
        db.session.commit()
        
        flash('Registro de papeles a retirar agregado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar el registro: {str(e)}', 'danger')
    
    return redirect(url_for('papeles_retirar'))

@app.route('/eliminar_papeles_retirar/<int:id>')
def eliminar_papeles_retirar(id):
    try:
        registro = PapelesRetirar.query.get_or_404(id)
        db.session.delete(registro)
        db.session.commit()
        flash('Registro eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el registro', 'danger')
    
    return redirect(url_for('papeles_retirar'))

if __name__ == '__main__':
    # Verificar conexión antes de ejecutar
    if check_db_connection():
        print("🚗 Iniciando Documentación Vehicular con base de datos MySQL...")
        print("📱 Abre tu navegador en: http://localhost:5000")
        print("🗄️  Base de datos: gestoria")
        print("👤 Usuario: root (sin contraseña)")
        print("-" * 60)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ No se pudo conectar a la base de datos")
        print("💡 Ejecuta 'flask db init' para configurar las migraciones")
