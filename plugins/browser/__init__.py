# -*- coding: utf-8 -*-
###############################################################################
# (C) 2007 EVO Sistemas Libres <central@evosistemas.com>
# __init__.py
# Plugin de tareas para EVOEditor
###############################################################################

# Importación de PyGTK
import gtk
import gtk.glade
import gtksourceview

# Importaciones específicas para el plugin
import gtkmozembed

###############################################################################
# Parámetros principales del plugin
###############################################################################
PLUGIN_NAME='Browser'
PLUGIN_VERSION='0.1'
PLUGIN_EVOEDITOR_VERSION='0.1'
PLUGIN_DESCRIPTION='Plugin navegación'
PLUGIN_CONFIGURABLE=True
PLUGIN_IMAGE_PATH='plugins/browser/pixmaps/'
PLUGIN_ICON=PLUGIN_IMAGE_PATH + 'browser.png'
PLUGIN_GLADE_FILE='plugins/browser/browser.glade'

###############################################################################
# Clase de carga del plugin
###############################################################################
class PluginLoader:
	"""
	Descripción del plugin
	"""
	def __init__(self,gui):
		"""
		Constructor del Plugin
		"""
		# Guardar instancia del GUI
		self.gui=gui
		# Guardar ventana principal
		self.mainWindow=gui.mainWindow
		# Diccionario de widgets contenedores disponibles para del plugin
		self.container=gui.containers['editor']
		# Carga de fichero glade del plugin
		self.gladetree=gtk.glade.XML(PLUGIN_GLADE_FILE)
		# Carga de los widgets necesarios
		self.__getwidgets()
		# Conectar las señales del widget de tareas
		self.__connectSignals()
		# Inicialización de parámetros del GUI y demás widgets
		self.__initGui()
		# Insertar widgets en los contenedores
		self.__dockWidgets()

	def disable(self):
		"""
		Desactivador del Plugin
		"""
		#self.widgets['sepEditFind'].destroy()
		#self.findDialog.destroy()
		#self.toolbar.destroy()
		pass

	########################################################################
	# Métodos para la inicialización de las distintas partes del plugin
	########################################################################

	def __initGui(self):
		"""
		Inicializar los widgets necesarios para el plugin
		"""
		# Carga de la ventana de configuración del plugin
		if PLUGIN_CONFIGURABLE:
			self.configDialog=self.gladetree.get_widget('winConfig')
		else:
			self.configDialog=None
		self.configDialog.set_version(PLUGIN_VERSION)
		# Ventana navegador
		self.browserDialog=self.gladetree.get_widget('winBrowser')
		# Barra de herramientas
		self.toolbar=self.gladetree.get_widget('hndFindReplace')
		# Instancia del editor
		self.editor=self.gui.editor
		# Lista de páginas con editor:
		self.browsers=[]

	def __getwidgets(self):
		self.widgets={}
		widgetlist=[
		]
		for widgetname in widgetlist:
			self.widgets[widgetname]=self.gladetree.get_widget(widgetname)

	def __connectSignals(self):
		"""
		Conectar señales de los widgets del plugin
		"""
		# Definición del diccionario de señales del plugin
		signals = {
			'showconfig': self.showConfig,
		}
		self.gladetree.signal_autoconnect(signals)

	def __dockWidgets(self):
		"""
		Insertar widgets del plugin en el contenedor seleccionado
		"""
		moz=gtkmozembed.MozEmbed()
		moz.show()
		label=gtk.Label('HOLAAA')
		label.show()
		page=self.container.append_page(moz,label)
		self.editor.dummyfile()
		self.browsers.append(page)
		moz.load_url('http://www.google.com')
		# Añadir entradas al menú de edición
		#editmenu=self.gui.gladetree.get_widget('menuEdit_menu')
		#accelgroup=gtk.AccelGroup()
		#self.gui.mainWindow.add_accel_group(accelgroup)
		#self.widgets['mnuEditFind'].unparent()
		#self.widgets['mnuEditReplace'].unparent()
		#self.widgets['sepEditFind']=gtk.SeparatorMenuItem()
		#self.widgets['sepEditFind'].show()
		#editmenu.insert(self.widgets['sepEditFind'],14)
		#editmenu.insert(self.widgets['mnuEditReplace'],14)
		#editmenu.insert(self.widgets['mnuEditFind'],14)
		#self.widgets['mnuEditFind'].add_accelerator('activate', accelgroup,ord('F'),gtk.gdk.CONTROL_MASK,gtk.ACCEL_VISIBLE)
		#self.widgets['mnuEditReplace'].add_accelerator('activate', accelgroup,ord('R'),gtk.gdk.CONTROL_MASK,gtk.ACCEL_VISIBLE)
		## Añadir barra de búsqueda
		#self.toolbar.unparent()
		#self.toolbar.show()
		#self.gui.widgets['hbxToolbars'].add(self.toolbar)
		# Conectar shortcuts
		# self.mainWindow.add_accel_group(self.shortcuts)

	########################################################################
	# Señales comunes de los plugins
	########################################################################

	def showConfig(self):
		"""
		Mostrar diálogo de configuración del plugin
		"""
		if self.configDialog:
			self.gui.openDialog(self.configDialog,close=True)

	########################################################################
	# Métodos para interconexión con EVOEditor
	########################################################################
	
	def newProject(self):
		"""
		Se ejecutará cuando se cree un nuevo proyecto
		"""
		pass

	def loadProject(self):
		"""
		Se ejecutará cuando se cargue un proyecto
		"""
		pass

	def saveProject(self):
		"""
		Se ejecutará cuando se guarde un proyecto
		"""
		pass
	
	def closeProject(self):
		"""
		Se ejecutará cuando se cierre un proyecto
		"""
		pass

	def newFile(self,args):
		"""
		Se ejecutará cuando se cree un nuevo archivo para edición
		"""
		pass
	
	def loadFile(self,args):
		"""
		Se ejecutará cuando se cargue un archivo para edición
		"""
		pass

	def saveFile(self,args):
		"""
		Se ejecutará cuando se guarde un archivo en edición
		"""
		pass

	def closeFile(self,args):
		"""
		Se ejecutará cuando se inicie el cierre de un archivo en edición
		"""
		pass

	########################################################################
	# Métodos propios del plugin
	########################################################################

################################################################################
# Definiciones de clases propias del plugin
################################################################################
