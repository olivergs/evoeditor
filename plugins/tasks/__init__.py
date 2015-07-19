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

###############################################################################
# Parámetros principales del plugin
###############################################################################
PLUGIN_NAME='Tareas'
PLUGIN_VERSION='v0.1'
PLUGIN_EVOEDITOR_VERSION='0.1'
PLUGIN_DESCRIPTION='Plugin de tareas'
PLUGIN_CONFIGURABLE=False
PLUGIN_ICON='plugins/tasks/pixmaps/tasks.png'
PLUGIN_GLADE_FILE='plugins/tasks/tasks.glade'

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
		self.container=gui.containers['bottom']
		# Carga de fichero glade del plugin
		self.gladetree=gtk.glade.XML(PLUGIN_GLADE_FILE)
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
		self.TasksWidget.destroy()
		#self.container.remove_page(self.page)
	
	########################################################################
	# Métodos para la inicialización de las distintas partes del plugin
	########################################################################

	def __initGui(self):
		"""
		Inicializar los widgets necesarios para el plugin
		"""
		# Widget del módulo de tareas
		self.TasksWidget=self.gladetree.get_widget('TaskWidget')
		# Diálogo de edición de tareas
		self.winTaskEdit=self.gladetree.get_widget('winTaskEditDialog')
		# TreeView encargado de mostrar las tareas
		self.tv=self.gladetree.get_widget('tvTaskList')
		# Modelo de datos del TreeView
		self.dm=gtk.ListStore(gtk.gdk.Pixbuf,gtk.gdk.Pixbuf,str,int,str)
		# Asociación del modelo de datos con el TreeView
		self.tv.set_model(self.dm)
		self.tv.set_headers_visible(True)
		# Renderers de las celdas
		textRenderer = gtk.CellRendererText()
		imgRenderer = gtk.CellRendererPixbuf()
		# Agregamos las columnas del TreeView
		self.tv.append_column(gtk.TreeViewColumn('Tipo', imgRenderer, pixbuf=0))
		self.tv.append_column(gtk.TreeViewColumn('Prioridad', imgRenderer, pixbuf=1))
		self.tv.append_column(gtk.TreeViewColumn('Archivo', textRenderer, text=2))
		self.tv.append_column(gtk.TreeViewColumn('Linea', textRenderer, text=3))
		self.tv.append_column(gtk.TreeViewColumn('Título', textRenderer, text=4))

	def __connectSignals(self):
		"""
		Conectar señales de los widgets del plugin
		"""
		# Definición del diccionario de señales del plugin
		signals = {
			'showconfig': self.showConfig,
			'addTask': self.addTask,
			'editTask': self.editTask,
			'removeTask': self.removeTask,
			'saveTask': self.saveTask,
			'cancelTaskEdit': self.cancelTaskEdit,
		}
		self.gladetree.signal_autoconnect(signals)

	def __dockWidgets(self):
		"""
		Insertar widgets del plugin en el contenedor seleccionado
		"""
		# Desconectar el widget de la ventana principal y mostrarlo
		self.TasksWidget.unparent()
		self.TasksWidget.show()
		# Insertar el mídulo de tareas en una nueva página del contenedor
		self.TasksLabel=gtk.Label('Tareas')
		self.TasksLabel.show()
		self.page=self.container.insert_page(self.TasksWidget,self.TasksLabel,0)
		self.container.set_current_page(self.page)

	########################################################################
	# Señales comunes de los plugins
	########################################################################

	def showConfig(self,widget):
		"""
		Mostrar diálogo de configuración del plugin
		"""
		pass

	########################################################################
	# Métodos para interconexión con EVOEditor
	########################################################################
	
	def newProject(self,args):
		"""
		Se ejecutará cuando se cree un nuevo proyecto
		"""
		pass

	def loadProject(self,args):
		"""
		Se ejecutará cuando se cargue un proyecto
		"""
		pass

	def saveProject(self,args):
		"""
		Se ejecutará cuando se guarde un proyecto
		"""
		pass
	
	def closeProject(self,args):
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
		Se ejecutará cuando se cierre archivo en edición
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

	def addTask(self,widget):
		"""
		Muestra el diálogo para añadir una nueva tarea al proyecto
		"""
		self.mainWindow.set_sensitive(False)
		self.winTaskEdit.set_keep_above(True)
		self.winTaskEdit.show()

	def editTask(self,widget,path=None,column=None):
		"""
		Edita una tarea existente
		"""
		# Comprobar si hay alguna tarea seleccionada
		# Cargar datos de la tarea seleccionada en diálogo de edición
		# Mostrar diálogo de edición
		self.mainWindow.set_sensitive(False)
		self.winTaskEdit.set_keep_above(True)
		self.winTaskEdit.show()
		
	def removeTask(self,widget):
		"""
		Elimina una tarea existente
		"""
		# Comprobar si hay alguna tarea seleccionada
		# Pedir confirmación para eliminación de la tarea
		# Quitar tarea del TreeView
		print "Eliminar tarea"

	def saveTask(self,widget):
		"""
		Añade la nueva tarea al TreeView
		"""
		tasktype='Error'
		taskprio='Alta'
		file='__init__.py'
		line=10
		title='Prueba de tarea añadida'
		typePixbuf=gtk.gdk.pixbuf_new_from_file('plugins/tasks/pixmaps/type' + tasktype + '.png')
		prioPixbuf=gtk.gdk.pixbuf_new_from_file('plugins/tasks/pixmaps/prio' + taskprio + '.png')
		self.dm.append([typePixbuf,prioPixbuf,file,line,title])

	def cancelTaskEdit(self,widget,event=None):
		"""
		Añade la nueva tarea al treeview
		"""
		self.mainWindow.set_sensitive(True)
		self.winTaskEdit.hide()
		return True
