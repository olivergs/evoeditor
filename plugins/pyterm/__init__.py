# -*- coding: utf-8 -*-
###############################################################################
# (C) 2007 EVO Sistemas Libres <central@evosistemas.com>
# __init__.py
# Plugin de tareas para EVOEditor
###############################################################################

# Importación de PyGTK
import gtk
import gtk.glade

# Importaciones específicas para el plugin
import vte

###############################################################################
# Parámetros principales del plugin
###############################################################################
PLUGIN_NAME='Python Terminal'
PLUGIN_VERSION='0.1'
PLUGIN_EVOEDITOR_VERSION='0.1'
PLUGIN_DESCRIPTION='Plugin de terminal de python'
PLUGIN_CONFIGURABLE=True
PLUGIN_IMAGE_PATH='plugins/pyterm/pixmaps/'
PLUGIN_ICON=PLUGIN_IMAGE_PATH + 'python.png'
PLUGIN_GLADE_FILE='plugins/pyterm/pyterm.glade'

# Otras constantes del plugin
DEFAULT_TERMINAL_COMMAND='python'

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
		self.containers=gui.containers
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
		self.terminal.destroy()

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
		# Inicialización del terminal
		self.terminalcmd=DEFAULT_TERMINAL_COMMAND
		self.terminal=vte.Terminal()
		self.terminal.connect('child-exited',self.termRestart)
		self.terminal.fork_command(self.terminalcmd)

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
		self.terminal.set_scroll_on_output(True)
		self.terminal.set_scroll_on_keystroke(True)
		label=gtk.Label('Python')
		label.show()
		hbox=gtk.HBox()
		self.scroll=gtk.VScrollbar()
		self.scroll.set_adjustment(self.terminal.get_adjustment())
		hbox.pack_start(self.terminal)
		hbox.pack_start(self.scroll)
		hbox.show_all()
		page=self.containers['bottom'].prepend_page(hbox,label)
		self.containers['bottom'].set_current_page(page)

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

	def pageChanged(self,args):
		"""
		Se ejecutará cuando se cambie de fichero en edición en el editor
		"""
		pass

	########################################################################
	# Métodos propios del plugin
	########################################################################

	def termRestart(self,vt):
		"""
		Reiniciar el terminal cuando el proceso hijo termine
		"""
		vt.fork_command(self.terminalcmd)

################################################################################
# Definiciones de clases propias del plugin
################################################################################
