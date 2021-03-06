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

###############################################################################
# Parámetros principales del plugin
###############################################################################
PLUGIN_NAME='Buscar/Reemplazar'
PLUGIN_VERSION='0.8'
PLUGIN_EVOEDITOR_VERSION='0.1'
PLUGIN_DESCRIPTION='Plugin de búsqueda y reemplazo'
PLUGIN_CONFIGURABLE=True
PLUGIN_IMAGE_PATH='plugins/find/pixmaps/'
PLUGIN_ICON=PLUGIN_IMAGE_PATH + 'find.png'
PLUGIN_GLADE_FILE='plugins/find/find.glade'

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
		self.container=None
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
		self.widgets['mnuEditFind'].destroy()
		self.widgets['mnuEditReplace'].destroy()
		self.widgets['sepEditFind'].destroy()
		self.findDialog.destroy()
		self.toolbar.destroy()

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
		# Ventana de búsqueda
		self.findDialog=self.gladetree.get_widget('winFindReplace')
		# Barra de herramientas
		self.toolbar=self.gladetree.get_widget('hndFindReplace')
		# Instancia del editor
		self.editor=self.gui.editor
		# Añadir variables a los ficheros para uso del plugin
		for file in self.editor.files:
			file.selstart=None
			file.selend=None
		# Carga de colores por defecto de resaltado
		self.widgets['clbFindFG'].set_color(gtk.gdk.color_parse('#000000'))
		self.widgets['clbFindBG'].set_color(gtk.gdk.color_parse('#FFFF00'))
		# Creación de variables internas de búsqueda
		self.match=None
		self.lastmatch=None
		# Carga de imagen del marcador de búsqueda
		imgpath='plugins/find/pixmaps/'
		self.findmarker=gtk.gdk.pixbuf_new_from_file(imgpath+'findmarker.png')

	def __getwidgets(self):
		self.widgets={}
		widgetlist=[
			# Widgets de las opciones de buscar/reemplazar
			'vbxReplaceOptions','tblHighlightOptions',
			'entFindText','entReplaceText','cmbFindArea','chkFindHighlight',
			'chkDontStop','clbFindBG','clbFindFG','chkFindReport',
			'radReplaceConfirm','butFindPrev','butFindNext','butFindStart',
			'mnuEditFind','mnuEditReplace',
		]
		for widgetname in widgetlist:
			self.widgets[widgetname]=self.gladetree.get_widget(widgetname)

	def __connectSignals(self):
		"""
		Conectar señales de los widgets del plugin
		"""
		# Definición del diccionario de señales del plugin
		signals = {
			'findReplace': self.findReplace,
			'findStart': self.findStart,
			'findReset': self.findReset,
			'findFinish': self.findFinish,
			'showconfig': self.showConfig,
		}
		self.gladetree.signal_autoconnect(signals)

	def __dockWidgets(self):
		"""
		Insertar widgets del plugin en el contenedor seleccionado
		"""
		# Añadir entradas al menú de edición
		editmenu=self.gui.gladetree.get_widget('menuEdit_menu')
		accelgroup=gtk.AccelGroup()
		self.gui.mainWindow.add_accel_group(accelgroup)
		self.widgets['mnuEditFind'].unparent()
		self.widgets['mnuEditReplace'].unparent()
		self.widgets['sepEditFind']=gtk.SeparatorMenuItem()
		self.widgets['sepEditFind'].show()
		editmenu.insert(self.widgets['sepEditFind'],14)
		editmenu.insert(self.widgets['mnuEditReplace'],14)
		editmenu.insert(self.widgets['mnuEditFind'],14)
		self.widgets['mnuEditFind'].add_accelerator('activate', accelgroup,ord('F'),gtk.gdk.CONTROL_MASK,gtk.ACCEL_VISIBLE)
		self.widgets['mnuEditReplace'].add_accelerator('activate', accelgroup,ord('R'),gtk.gdk.CONTROL_MASK,gtk.ACCEL_VISIBLE)
		# Añadir barra de búsqueda
		self.toolbar.unparent()
		self.toolbar.show()
		self.gui.widgets['hbxToolbars'].add(self.toolbar)
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
		# Inicializar parámetros de búsqueda para el nuevo fichero
		self.editor.files[args['fileid']].findstart=None
		self.editor.files[args['fileid']].findend=None
		# Añadir marcador de búsqueda al fichero
		self.editor.files[args['fileid']].srcview.set_marker_pixbuf('find',)

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
		# Comprobar si quedan archivos en edición
		if len(self.editor.files)==1:
			self.findFinish()

		
	def pageChanged(self,args):
		"""
		Se ejecutará cuando se cambie de fichero en edición en el editor
		"""
		pass
	
	########################################################################
	# Métodos propios del plugin
	########################################################################

	def findReplace(self,widget,close=True):
		"""
		Mostrar diálogo de búsqueda
		"""
		curpage=self.gui.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			# Inicialización de la sesión de búsqueda
			self.findReset()
			self.tags=[]
			# Preparar diálogo
			self.widgets['entReplaceText'].set_text('')
			if self.widgets['cmbFindArea'].get_active()==-1:
				self.widgets['cmbFindArea'].set_active(0)
			if widget.name=='mnuEditReplace' or widget.name=='tlbtReplace':
				self.widgets['vbxReplaceOptions'].show()
				self.widgets['tblHighlightOptions'].hide()
				self.widgets['chkFindHighlight'].set_active(False)
			else:
				self.widgets['vbxReplaceOptions'].hide()
				self.widgets['tblHighlightOptions'].show()
			# Bucle del diálogo
			self.findDialog.set_keep_above(True)
			self.findDialog.show()

	def findStart(self,widget):
		"""
		Comenzar búsqueda
		"""
		curpage=self.gui.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			# Carga parámetros de búsqueda
			caps=True
			find=self.widgets['entFindText'].get_text()
			replace=self.widgets['entReplaceText'].get_text()
			area=self.widgets['cmbFindArea'].get_active()
			highlight=self.widgets['chkFindHighlight'].get_active()
			report=self.widgets['chkFindReport'].get_active()
			confirm=self.widgets['radReplaceConfirm'].get_active()
			fg=self.gui.htmlColor(self.widgets['clbFindFG'].get_color())
			bg=self.gui.htmlColor(self.widgets['clbFindBG'].get_color())
			if widget.name=='butFindPrev':
				direction=False
			else:
				direction=True
			# Comprobar parámetros de búsqueda
			if find=='':
				self.gui.msgDialog('error','No se ha especificado un patrón de búsqueda',parent=self.findDialog)
			else:
				self.match=self.findtext(curpage,find,replace,area,caps,self.match,direction)
				if not self.match:
					self.gui.msgDialog('error','No se han encontrado coincidencias',parent=self.findDialog)
					self.match=self.lastmatch
				else:
					if highlight or replace!='':
						# Loop de búsqueda
						self.editor.files[self.match.page].sbuffer.begin_user_action()
						while self.match:
							if replace!='':
								resp=True
								if confirm:
									self.editor.files[self.match.page].srcview.scroll_to_iter(self.match.start,0.4)
									self.gui.highlightText(self.match.page,self.match.start,self.match.end,str(self.match.page)+'currentmatch')
									if self.tags.count(str(self.match.page)+'currentmatch')==0:
										self.tags.append(str(self.match.page)+'currentmatch')
									resp=self.gui.msgDialog('question','¿Confirmar reemplazo en la línea %s?' % str(self.match.line+1),parent=self.findDialog,cancel=True)
									self.editor.files[self.match.page].sbuffer.remove_tag_by_name(str(self.match.page)+'currentmatch',
										self.editor.files[self.match.page].sbuffer.get_start_iter(),self.editor.files[self.match.page].sbuffer.get_end_iter())
									if resp=='cancel':
										break
								if resp:
									self.match=self.replacetext(replace,self.match)
									self.subs+=1
							else:
								if highlight:
									self.gui.highlightText(self.match.page,self.match.start,self.match.end,find,fg,bg)
									if self.tags.count(find)==0:
										self.tags.append(find)
							self.match=self.findtext(curpage,find,replace,area,caps,self.match)
							self.lastmatch=self.match
						self.editor.files[self.lastmatch.page].sbuffer.end_user_action()
						if report and replace!='':
							self.gui.msgDialog('info','Se realizaron %s sustituciones' % self.subs,parent=self.findDialog)
							self.subs=0
						self.findReset()
					else:
						if curpage!=self.match.page:
							self.widgets['ntbEditor'].set_current_page(self.match.page)
						if self.lastmatch:
							self.editor.files[self.lastmatch.page].sbuffer.remove_tag_by_name(str(self.lastmatch.page)+'currentmatch',
								self.editor.files[self.lastmatch.page].sbuffer.get_start_iter(),self.editor.files[self.lastmatch.page].sbuffer.get_end_iter())
						self.gui.highlightText(self.match.page,self.match.start,self.match.end,str(self.match.page)+'currentmatch')
						if self.tags.count(str(self.match.page)+'currentmatch')==0:
							self.tags.append(str(self.match.page)+'currentmatch')
						self.editor.files[self.match.page].srcview.scroll_to_iter(self.match.start,0.4)
						self.widgets['butFindPrev'].show()
						self.widgets['butFindNext'].show()
						self.widgets['butFindStart'].hide()
						# Resaltado
						if highlight:
							self.gui.highlightText(self.match.page,self.match.start,self.match.end,find,fg,bg)
							if self.tags.count(find)==0:
								self.tags.append(find)
						self.lastmatch=self.match

	def findReset(self,widget=None):
		"""
		Reinicia la vista de búsqueda
		"""
		if self.lastmatch and self.tags.count(str(self.lastmatch.page)+'currentmatch')>0:
			self.editor.files[self.lastmatch.page].sbuffer.remove_tag_by_name(str(self.lastmatch.page)+'currentmatch',
			self.editor.files[self.lastmatch.page].sbuffer.get_start_iter(),self.editor.files[self.lastmatch.page].sbuffer.get_end_iter())
		for file in self.editor.files:
			file.selstart=None
			file.selend=None
		self.subs=0
		self.match=None
		self.widgets['butFindPrev'].hide()
		self.widgets['butFindNext'].hide()
		self.widgets['butFindStart'].show()

	def findFinish(self,widget=None,event=None):
		"""
		Terminar la sesión de búsqueda
		"""
		self.findReset()
		self.findDialog.hide()
		for file in self.editor.files:
			for tag in self.tags:
				file.sbuffer.remove_tag_by_name(tag,file.sbuffer.get_start_iter(),file.sbuffer.get_end_iter())
		return True

	def findtext(self,page,find,replace,area,caps,match,forward=True):
		"""
		Buscar texto en el editor
		"""
		# Coger el buffer completo del documento
		file=self.editor.files[page]
		sbuffer=file.sbuffer
		if not file.findstart or file.findend:
			if area==0:
				file.findstart,file.findend=sbuffer.get_bounds()
			else:
				file.findstart,file.findend=sbuffer.get_selection_bounds()
		# Comprobar si se debe confirmar reemplazo
		if match:
			start=match.end
			if not forward:
				start=match.start
		else:
			start=file.findstart
		# Comenzar búsqueda
		cur=start
		if forward:
			match=cur.forward_search(find,gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=file.findend)
		else:
			match=cur.backward_search(find,gtk.TEXT_SEARCH_VISIBLE_ONLY,limit=file.findstart)
		if match:
			# Retornar el resultado
			if match:
				sbuffer.place_cursor(match[1])
				# sbuffer.select_range(match[0],match[1])
				return FindMatch(page,match[0].get_line(),match[0],match[1])
		else:
			return None

	def replacetext(self,replacetext,match):
		"""
		Reemplazar texto en el editor
		"""
		file=self.editor.files[match.page]
		sbuffer=file.sbuffer
		pos=match.start.get_offset()
		sbuffer.delete(match.start,match.end)
		sbuffer.insert(match.start,replacetext)
		match.start=sbuffer.get_iter_at_offset(pos)
		match.end=sbuffer.get_iter_at_offset(pos+len(replacetext))
		sbuffer.select_range(match.start,match.end)
		return match

################################################################################
# Definiciones de clases propias del plugin
################################################################################

class FindMatch:
	"""
	Clase para almacenar los datos de una coincidencia de búsqueda
	"""
	def __init__(self,page,line,start,end):
		"""
		Constructor de la clase
		"""
		self.page=page
		self.line=line
		self.start=start
		self.end=end