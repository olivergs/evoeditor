# -*- coding: utf-8 -*-
###############################################################################
# (C) 2007 EVO Sistemas Libres <central@evosistemas.com>
# core.py
# Módulo principal de control de EVOEditor
###############################################################################

###############################################################################
# Datos generales de la aplicación
###############################################################################

APP_NAME='EVOEditor'
APP_VERSION='0.1'
APP_DESC='Editor de texto para desarrollo basado en PyGTK'
APP_CREDITS='EVO Sistemas Libres S.L.N.E. <central@evosistemas.com>'

###############################################################################
# Importación de bibliotecas necesarias para la carga de EVOEditor
###############################################################################

# Importación de bibliotecas de Python
import sys,os,shutil

# Importación de PyGTK
try:
	import pygtk,gobject,gtk
	pygtk.require('2.0')
except:
	print 'No se encuentra PyGTK en el sistema. Instale las bibliotecas PyGTK para poder ejecutar esta aplicación'
	sys.exit(1)

# Importación de Glade
try:
	import gtk.glade
except:
	print 'No se encuentra Glade en el sistema. Instale las bibliotecas Glade de python para ejecutar esta aplicación'
	sys.exit(1)

# Importación de GTK SourceView
try:
	import gtksourceview2
except:
	print 'No se encuentra GTKSourceView en el sistema. Instale las bibliotecas el mídulo de GTKSourceview para ejecutar esta aplicación'
	sys.exit(1)

###############################################################################
# Importación de módulos de EVOEditor
###############################################################################

# Importación del módulo de interfaz gráfica de usuario
import gui,editor,plugin

# Clase de carga de configuración de EVOEditor
class Config:
	"""
	Clase de carga de la configuración
	"""
	def __init__(self):
		"""
		Constructor de la clase de configuración
		"""
		# Recoger variables de entorno necesarias
		home=os.environ['HOME']
		# Comprobar si existe el directorio de configuración
		if not os.access(home + '/.evoeditor',os.F_OK):
			os.mkdir(home + '/.evoeditor')
		# Comprobar si existe el fichero principal de preferencias
		if not os.access(home + '/.evoeditor/settings.py',os.F_OK):
			# Escribir configuración por defecto
			self.defaults(home)
		# Añadir la carpeta del usuario como parte de la ruta de python
		sys.path.append(home + '/.evoeditor')
		# Cargar configuración
		import settings
		# Cargar parámetros de la configuración
		settingsdir=dir(settings)
		if 'GUI' not in settingsdir and 'EDITOR' not in settingsdir:
			# Mostrar error de carga de configuración y generar nueva (usar diálogo)
			print 'Error cargando la configuración. Creando configuración por defecto'
			self.defaults(home)
		self.gui=settings.GUI
		self.editor=settings.EDITOR
		if 'PROJECTS' in settingsdir:
			self.projects=settings.PROJECTS
		if 'PLUGINS' in settingsdir:
			self.plugins=settings.PLUGINS

	# Generar una configuración por defecto
	def defaults(self,home):
		"""
		Genera un fichero de configuración por defecto
		"""
		shutil.copyfile('./data/defaults.py', home + '/.evoeditor/settings.py')

	def setprefs(self,preferencesWindow):
		"""
		Carga las preferencias en el diálogo especificado.
		"""
		pass

	def loadconfig(self):
		"""
		Carga de la configuración
		"""
		# Abrir fichero de configuración
		# Cargar configuración
		# Hacer chequeo de la configuración
		pass

	def saveconfig(self):
		"""
		Guardar configuración
		"""
		# Recopilar datos
		# Abrir fichero para escritura
		# Escribir datos
		# Cerrar fichero

###############################################################################
# Inicialización de EVOEditor
###############################################################################

def startup(args):
	"""
	Inicialización de EVOEditor
	"""
	# Carga de la configuración de EVOEditor
	config=Config()
	# Carga de glade
	gladetree=gtk.glade.XML('evoeditor.glade')
	# Clase del GUI
	appgui=gui.EVOEditorGUI(config,gladetree)
	# Inicialización	
	gobject.idle_add(initapp,config,gladetree,appgui,args)
	# Finalizar carga de EVOEditor e iniciar bucle de eventos
	appgui.run()
	# Finalizado el bucle de eventos, guardar configuración
	pass

# Función de carga de EVOEditor
def initapp(config,gladetree,appgui,args):
	"""
	Carga inicial de EVOEditor
	"""
	# Carga de argumentos
	files=[]
	del(args[0])
	garbage=''
	for I in args:
		if I=='-h' or I=='--help':
			# Mostrar ayuda
			showhelp()
		elif I=='-v' or I=='--version':
			# Mostrar versión
			showversion()
		elif I[:1]!='-':
			garbage+=' %s' % I
			print garbage
			try:
				if os.stat(garbage.strip()):
					files.append(garbage.strip())
					garbage=''
			except:
				pass
			del(I)
	# Carga de ventana principal
	mainWindow=gladetree.get_widget('winMain')
	# Comprobar si la ventana principal ha sido cargada correctamente
	if not mainWindow:
		appgui.msgDialog('error','Error al cargar ventana principal del programa')
		sys.exit(1)
	# Carga de pantalla de bienvenida
	progress=gladetree.get_widget('prgSplash')
	splashWindow=gladetree.get_widget('winSplash')
	if config.gui['splash'] and args.count('--nosplash')==0:
		gobject.timeout_add(100,pulse,progress)
		splashWindow.show()
	# Carga de los widgets del GUI
	pulse(progress,'Cargando GUI')
	appgui.getwidgets()
	appgui.connectsignals()
	# Carga del subsistema del editor
	pulse(progress,'Cargando subsistema del editor')
	appgui.editor=editor.EditorHelper()
	# Carga de configuración
	pulse(progress,'Cargando configuración')
	appgui.loadconfig()
	# Carga de lenguajes
	pulse(progress,'Cargando Lenguajes')
	appgui.loadlangs()
	# Carga de la lista de proyectos
	pulse(progress,'Cargando lista de proyectos')
	# Carga de plugins
	pulse(progress,'Cargando plugins')
	appgui.plugins=plugin.PluginHelper(appgui)
	# Activar los plugins que aparezcan como activos en la configuración
	appgui.plugins.enable('tasks')
	appgui.plugins.enable('find')
	appgui.plugins.enable('term')
	appgui.plugins.enable('pyterm')
	#appgui.plugins.enable('browser')
	appgui.loadplugins()
	# Finalizar inicio de EVOEditor
	pulse(progress,'Completada la inicialización de EVOEditor')
	if config.gui['splash'] and args.count('--nosplash')==0:
		gobject.timeout_add(1000,showmainwindow,splashWindow,mainWindow,appgui,files)
	else:
		showmainwindow(splashWindow,mainWindow,appgui,files)

def pulse(progress,message=None):
	"""
	Generar actividad en barra de progreso de la pantalla de bienvenida
	"""
	if message:
		progress.set_text(message)
	else:
		progress.pulse()
		gobject.timeout_add(100,pulse,progress)

def showmainwindow(splashWindow,mainWindow,appgui,files):
	"""
	Mostrar la pantalla principal de la aplicación
	"""
	splashWindow.hide()
	appgui.openFile(filenames=files)
	mainWindow.show()

def showhelp():
	"""
	Mostrar ayuda del programa
	"""
	print '%s v%s\n%s\n\t%s' % (APP_NAME,APP_VERSION,APP_CREDITS,APP_DESC)
	print 'Esta es la ayuda de EVOEditor'
	sys.exit(1)

def showversion():
	print '%s v%s\n%s\n\t%s' % (APP_NAME,APP_VERSION,APP_CREDITS,APP_DESC)
	sys.exit(1)
