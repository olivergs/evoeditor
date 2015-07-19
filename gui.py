# -*- coding: utf-8 -*-
################################################################################
# (C) 2007 EVO Sistemas Libres <central@evosistemas.com>
# gui.py
# Clase de control del GUI de EVOEditor
################################################################################

# Importaciones de python
import sys,time,mimetypes,pango

# Importaciones de GTK, Glade y GTKSourceView
import gobject,gtk,gtk.glade,gtksourceview2

# Carga de plugins
from plugins import tasks

class EVOEditorGUI:
	"""
	Clase principal del editor EVOEditor
	"""
	# Diccionario de códigos de teclado
	keymap={
		'home': 65360,
		'left': 65361,
		'up': 65362,
		'right': 65363,
		'down': 65364,
		'pgup': 65365,
		'pgdown': 65366,
		'end': 65367,
		'tab': 65289,
		'shifttab': 65056,
		'kpadd': 65451,
		'kpminus': 65453,
	}

	def __init__(self,config,gladetree):
		"""
		Constructor de la clase de control del GUI
		"""
		# Almacenar configuración
		self.config=config
		# Almacenar objeto de Glade para definiciones del GUI
		self.gladetree=gladetree
		# Contenedor para los widgets utilizados
		self.widgets={}
		# Carga de las ventanas de la aplicación
		self.mainWindow=self.gladetree.get_widget('winMain')	
		self.aboutDialog=self.gladetree.get_widget('winAboutDialog')
		self.preferencesWindow=self.gladetree.get_widget('winPreferencesDialog')
		self.fileDialog=self.gladetree.get_widget('winFileChoose')
		self.gotoLineDialog=self.gladetree.get_widget('winGotoLineDialog')

	def getwidgets(self):
		"""
		Cargar widgets necesarios para el control de la aplicación
		"""
		# Lista de widgets a cargar
		widgetlist=[
			# Contenedor de las barras de herramientas
			'hbxToolbars',
			# Barra de estado
			'stbMain',
			# Información en la barra de estado
			'lblEditorInfo',
			# Widget del editor
			'ntbEditor',
			# Widget de la barra de herramientas principal
			'tlbMain',
			# Widgets de menús y barras de herramientas de la ventana principal
			'mnuViewSidePanel','mnuViewBottomPanel',
			'tlbgFullscreen','mnuViewFullscreen',
			'mnuViewLineNums','mnuViewLineMargin','mnuViewLineMarkers',
			# Menú de lenguajes de programación
			'mnuToolsLangs',
			# Menú de los plugins
			'mnuToolsPlugins',
			# Widgets de separación de la ventana principal
			'vpnMain','hpnMain',
			# Widgets contenedores de los plugins
			'ntbBottom','ntbLeft',
			# Widget del diálogo de ir a línea
			'entGotoLine',
		]
		for widgetname in widgetlist:
			self.widgets[widgetname]=self.gladetree.get_widget(widgetname)
		# Carga de contenedores disponibles para los plugins
		self.containers={
			'bottom': self.widgets['ntbBottom'],
			'left': self.widgets['ntbLeft'],
			'editor': self.widgets['ntbEditor'],
		}

	def connectsignals(self):
		"""
		Conectar señales del GUI
		"""
		# Conectar las señales
		signals = {
			# Señales de control de la ventana principal
			'switchSidePanel': self.switchSidePanel,
			'switchBottomPanel': self.switchBottomPanel,
			# Señales de preferencias
			'showPreferences': self.showPreferences,
			'savePreferences': self.savePreferences,
			# Señales del diálogo Acerca de...
			'showAbout': self.showAbout,
			# Señales del editor
			'newFile': self.newFile,
			'openFile': self.openFile,
			'saveFile': self.saveFile,
			'saveFileAs': self.saveFileAs,
			'reloadFile': self.reloadFile,
			'closeFile': self.closeFile,
			'closeFileAll': self.closeFileAll,
			'cutText': self.cutText,
			'copyText': self.copyText,
			'pasteText': self.pasteText,
			'deleteText': self.deleteText,
			'selectAll': self.selectAll,
			'unselectText': self.unselectText,
			'indentText': self.indentText,
			'unindentText': self.unindentText,
			'undoAction': self.undoAction,
			'redoAction': self.redoAction,
			'showLineNums': self.showLineNums,
			'showLineMarkers': self.showLineMarkers,
			'showLineMargin': self.showLineMargin,
			'pageChanged': self.pageChanged,
			'gotoLine': self.gotoLine,
			'fileStats': self.fileStats,
			'toUpper': self.toUpper,
			'toLower': self.toLower,
			'zoomEditor': self.zoomEditor,
			# Señales de control general del GUI
			'switchFullscreen': self.switchFullscreen,
			'quitProgram': self.quitProgram,
			# Prueba de eventos
			'prueba': self.prueba,
			'pruebakey': self.pruebakey,
		}
		self.gladetree.signal_autoconnect(signals)

	def loadlangs(self):
		"""
		Carga de los lenguajes de programación disponibles para resaltado
		"""
		return
		"""
		# Carga de los tipos mime extra para coloreado de sintaxis
		mimetypes.init(['./data/mimetypes'])
		# Carga de los lenguajes
		self.srclangs={}
		slmanager=gtksourceview2.SourceLanguagesManager()
		submenu=gtk.Menu()
		# Generación del diccionario de lenguajes
		for lang in slmanager.get_available_languages():
			self.srclangs[lang.get_name()]=lang.get_mime_types()
		# Ordenamos los lenguajes por orden alfabético
		langs=self.srclangs.keys()
		langs.sort()
		# Añadimos el texto plano como lenguaje por defecto
		self.srclangs['Texto plano']='text/plain'
		plain=gtk.RadioMenuItem(group=None,label='Texto plano')
		plain.connect('activate',self.setEditorLanguage)
		plain.show()
		submenu.add(plain)
		# Añadimos las entradas del menú de lenguajes por orden alfabético
		for I in langs:
			item=gtk.RadioMenuItem(group=plain,label=I)
			submenu.add(item)
			item.connect('activate',self.setEditorLanguage)
			item.show()
		self.widgets['mnuToolsLangs'].set_submenu(submenu)
		"""

	def loadplugins(self):
		"""
		Carga de los plugins disponibles
		"""
		submenu=gtk.Menu()
		pluginlist=self.plugins.available.keys()
		pluginlist.sort()
		# Añadimos las entradas del menú de lenguajes por orden alfabético
		for pluginid in pluginlist:
			if self.plugins.available[pluginid].configurable:
				item=gtk.MenuItem(label=self.plugins.available[pluginid].name)
				item.show()
				submenu.add(item)
				subitem=gtk.CheckMenuItem(label='Activado')
				subitemconfig=gtk.MenuItem(label='Configurar')
				subitem.connect('activate',self.switchPlugins,pluginid)
				subitemconfig.connect('activate',self.plugins.available[pluginid].showconfig)
				if self.plugins.available[pluginid].enabled:
					subitem.set_active(True)
				subitem.show()
				subitemconfig.show()
				pluginsubmenu=gtk.Menu()
				pluginsubmenu.add(subitem)
				pluginsubmenu.add(subitemconfig)
				item.set_submenu(pluginsubmenu)
			else:
				item=gtk.CheckMenuItem(label=self.plugins.available[pluginid].name)
				submenu.add(item)
				item.connect('activate',self.switchPlugins,pluginid)
				if self.plugins.available[pluginid].enabled:
					item.set_active(True)
				item.show()
		self.widgets['mnuToolsPlugins'].set_submenu(submenu)

	def loadconfig(self):
		"""
		Carga de la configuración de la aplicación
		"""
		# Carga de la configuración general del GUI
		self.mainWindow.resize(self.config.gui['width'], self.config.gui['height'])
		self.widgets['vpnMain'].set_position(self.config.gui['vpanpos'])
		self.widgets['hpnMain'].set_position(self.config.gui['hpanpos'])
		self.switchSidePanel()
		self.switchBottomPanel()
		self.showLineNums()
		self.showLineMarkers()
		self.showLineMargin()
		# Carga de la configuración en el diálogo de preferencias
		self.config.setprefs(self.preferencesWindow)

		# Shortcuts especiales de EVOEditor o del usuario
		# self.shortcuts=gtk.AccelGroup()
		# self.mainWindow.add_accel_group(self.shortcuts)

		# Prueba de carga del módulo de tareas
		#tasks.PluginLoader(self.mainWindow,self.widgets['ntbBottom'])

	def run(self):
		"""
		Finalizar inicialización del GUI
		"""
		gtk.main()

	########################################################################
	# Señales de control de la ventana principal
	########################################################################
	
	def switchSidePanel(self,widget=None):
		"""
		Mostrar diálogo de preferencias
		"""
		if widget:
			self.config.gui['sidepanel']=widget.get_active()
		else:
			self.widgets['mnuViewSidePanel'].set_active(self.config.gui['sidepanel'])
		if self.config.gui['sidepanel']:
			self.widgets['ntbLeft'].show()
		else:
			self.widgets['ntbLeft'].hide()

	def switchBottomPanel(self,widget=None):
		"""
		Guardar preferencias
		"""
		if widget:
			self.config.gui['bottompanel']=widget.get_active()
		else:
			self.widgets['mnuViewBottomPanel'].set_active(self.config.gui['bottompanel'])
		if self.config.gui['bottompanel']:
			self.widgets['ntbBottom'].show()
		else:
			self.widgets['ntbBottom'].hide()

	def switchPlugins(self,widget,pluginid):
		"""
		Cargar y descargar plugins
		"""
		if widget.get_active():
			self.plugins.enable(pluginid)
		else:
			self.plugins.disable(pluginid)

	########################################################################
	# Señales de preferencias
	########################################################################

	def showPreferences(self,widget):
		"""
		Mostrar diálogo de preferencias
		"""
		self.openDialog(self.preferencesWindow,close=True)

	def savePreferences(self,widget):
		"""
		Guardar preferencias
		"""
		pass

	########################################################################
	# Señales del diálogo Acerca de...
	########################################################################

	def showAbout(self,widget):
		"""
		Mostrar diálogo Acerca de...
		"""
		self.openDialog(self.aboutDialog,close=True)

	########################################################################
	# Señales y funciones del editor
	########################################################################

	def newFile(self,widget):
		"""
		Crear una nueva pestaña de edición para un nuevo archivo
		"""
		# Preparamos widget del editor
		sbuffer = gtksourceview2.SourceBuffer()
		sbuffer.connect('modified-changed', self.modifiedFile)
		sbuffer.connect('changed', self.updateStatus)
		scroll=gtk.ScrolledWindow()
		srcview=gtksourceview2.SourceView(sbuffer)
		srcview.modify_font(pango.FontDescription('monospace 8'))
		srcview.connect('key_press_event',self.enhanceInput)
		srcview.connect('scroll_event',self.zoomEditor)
		srcview.connect('event', self.updateStatus)
		# Preparamos widget de la pestaña del editor
		vbox=gtk.HBox()
		image=gtk.image_new_from_icon_name('gtk-close',-1)
		image.set_size_request(12,12)
		closebut=gtk.Button()
		closebut.set_size_request(20,16)
		closebut.set_image(image)
		closebut.connect('clicked',self.closeFile)
		closebut.set_relief(gtk.RELIEF_NONE)
		label=gtk.Label('Sin Título')
		label.set_padding(5,0)
		label.set_use_markup(True)
		vbox.add(label)
		vbox.add(closebut)
		# Almacenar los datos de la nueva página en la lista de ficheros en edición
		self.editor.newfile(None,sbuffer,None,scroll,srcview,label,closebut)
		scroll.add(srcview)
		# Importante: Para que se muestre el tab, hay que mostrar el control hijo y su etiqueta
		scroll.show()
		srcview.show()
		label.show()
		closebut.show()
		# Crear la página de editor y seleccionarla como página actual dandole el foco
		page=self.widgets['ntbEditor'].append_page(scroll, vbox)
		self.setPageConfig(page)
		self.widgets['ntbEditor'].set_current_page(page)
		self.editor.files[page].srcview.grab_focus()
		try:
			# Lanzar evento para los plugins
			self.plugins.event('newfile',{'fileid': page,})
		except:
			pass
		self.updateStatus(widget)
		return page

	def openFile(self,widget=None,filenames=None):
		"""
		Cargar un archivo
		"""
		# Abrir diálogo de selección de archivo
		self.fileDialog.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
		self.fileDialog.set_select_multiple(True)
		if filenames==None:
			curfile=self.widgets['ntbEditor'].get_current_page()
			if curfile>-1:
				curfilename=self.editor.files[curfile].filename
				if curfilename!=None:
					dirname=''
					path=curfilename.split('/')
					for I in range(1,len(path)-1):
						dirname+='/%s' % path[I]
					self.fileDialog.set_current_folder(dirname)
			resp=self.fileDialog.run()
			if resp==gtk.RESPONSE_OK:
				filenames=self.fileDialog.get_filenames()
		else:
			resp=gtk.RESPONSE_OK
		if resp==gtk.RESPONSE_OK:
			for filename in filenames:
				# Recortar el nombre del archivo
				path=filename.split('/')
				fname=path[len(path)-1]
				# Comprobar si el archivo ya está abierto
				page=None
				for I in range(0,len(self.editor.files)):
					label=self.editor.files[I].filename
					if filename == label:
						page=I
				if page!=None:
					# Activar página del archivo a abrir
					self.widgets['ntbEditor'].set_current_page(page)
				else:
					# Crear una nueva pestaña
					page=self.newFile(widget)
					# Cambio de etiqueta de la página actual
					self.editor.files[page].label.set_label(fname)
					self.widgets['ntbEditor'].set_menu_label_text(self.editor.files[page].scroll,fname)
					self.editor.files[page].filename=filename
					# Comprobar tipo mime del fichero para resaltado de sintaxis
					mimetype=mimetypes.guess_type(filename)
					if mimetype[0]:
						slmanager = gtksourceview2.SourceLanguagesManager()
						lang = slmanager.get_language_from_mime_type(mimetype[0])
						# Aplicamos la configuración al buffer de edición
						self.editor.files[page].sbuffer.set_language(lang)
						self.editor.files[page].sbuffer.set_highlight(True)
						# Guardamos los datos para el fichero actual
						self.editor.files[page].lang=lang
					# Cargar contenido del archivo
					if not self.editor.loaddata(self.editor.files[page].sbuffer,filename):
						# Mostrar mensaje de fallo
						self.widgets['ntbEditor'].remove_page(page)
						self.statusMessage('error',
							'Error cargando el fichero "%s"' % filename,
							'Se ha producido un error al realizar la operación de carga del fichero "%s".' % filename)
						self.editor.closefile(page)
						# Marcar el archivo como no modificado
					else:
						self.unmodifiedFile(self.editor.files[page].sbuffer)
						try:
							# Lanzar evento para los plugins
							self.plugins.event('openfile',[page])
						except:
							pass
						self.statusMessage('info','Archivo "%s" cargado correctamente' % filename)
						self.pageChanged(None,None,page)

			# Cerramos el diálogo de selección de archivo
		self.closeDialog(self.fileDialog)

	def saveFile(self,widget):
		"""
		Guardar archivo actual
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			if self.editor.files[curpage].filename:
				if not self.editor.savedata(self.editor.files[curpage].sbuffer,self.editor.files[curpage].filename):
					# Mostrar mensaje de fallo
					self.statusMessage('error',
						'Error grabando el fichero "%s"' % self.editor.files[curpage].filename,
						'Se ha producido un error al realizar la operación de grabación del fichero "%s".' % self.editor.files[curpage].filename)
				# Marcar el archivo como no modificado
				self.unmodifiedFile(self.editor.files[curpage].sbuffer)
				try:
					# Lanzar evento para los plugins
					self.plugins.event('savefile',[curpage])
				except:
					pass
				self.statusMessage('info','Archivo "%s" gardado correctamente' % self.editor.files[curpage].filename)
			else:
				self.saveFileAs(widget)

	def saveFileAs(self,widget):
		"""
		Guardar archivo actual como otro archivo
		"""
		# Comprobar si hay páginas en el editor
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			self.fileDialog.set_select_multiple(False)
			self.fileDialog.set_do_overwrite_confirmation(True)
			self.fileDialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
			resp = self.fileDialog.run()
			if resp == gtk.RESPONSE_OK:
				# Almacenar la ruta completa al archivo
				filename=self.fileDialog.get_filename()
				# Guardar archivo
				if not self.editor.savedata(self.editor.files[curpage].sbuffer,filename):
					# Mostrar mensaje de fallo
					self.statusMessage('error',
						'Error grabando el fichero "%s"' % filename,
						'Se ha producido un error al realizar la operación de grabación del fichero "%s".' % filename)
					self.closeDialog(self.fileDialog)
					return
				# Marcar el archivo como no modificado
				self.unmodifiedFile(self.editor.files[curpage].sbuffer)
				# Recortar el nombre del archivo
				path=filename.split('/')
				fname=path[len(path)-1]
				# Guardar nombre de archivo y asignarlo al texto de la pestaña de página
				self.editor.files[curpage].filename=filename
				self.editor.files[curpage].label.set_label(fname)
				self.widgets['ntbEditor'].set_menu_label_text(self.editor.files[curpage].scroll,fname)
				# Seleccionar el tipo de lenguaje para la ventana de editor
				mimetype=mimetypes.guess_type(filename)
				if mimetype[0]:
					slmanager = gtksourceview2.SourceLanguagesManager()
					lang = slmanager.get_language_from_mime_type(mimetype[0])
					# Aplicamos la configuración al buffer de edición
					self.editor.files[curpage].sbuffer.set_language(lang)
					self.editor.files[curpage].sbuffer.set_highlight(True)
					# Guardamos los datos para el fichero actual
					self.editor.files[curpage].lang=lang
				try:
					# Lanzar evento para los plugins
					self.plugins.event('savefile',[page])
				except:
					pass
			# Cerramos el diálogo de selección de archivo
			self.closeDialog(self.fileDialog)
			self.statusMessage('info','Archivo "%s" gardado correctamente' % filename)

	def reloadFile(self,widget):
		"""
		Recargar un fichero
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage!=-1:
			if not self.editor.loaddata(self.editor.files[curpage].sbuffer,self.editor.files[curpage].filename):
				self.statusMessage('error','Error al recargar el archivo "%s"' % self.editor.files[curpage].filename,True)
			else:
				self.unmodifiedFile(self.editor.files[curpage].sbuffer)
				self.statusMessage('info','Archivo "%s" recargado correctamente' % self.editor.files[curpage].filename)

	def closeFile(self,widget,curpage=None,checkmodif=True):
		"""
		Cerrar archivo actual
		"""
		if not curpage:
			curpage=self.widgets['ntbEditor'].get_current_page()
			for I in range(0,len(self.editor.files)):
				if widget==self.editor.files[I].button:
					curpage=I
		try:
			# Lanzar evento para los plugins
			self.plugins.event('closefile',{'fileid': curpage,})
		except:
			pass
		if curpage!=-1:
			self.widgets['ntbEditor'].set_current_page(curpage)
			if self.editor.files[curpage].sbuffer.get_modified():
				if checkmodif:
					if self.msgDialog('question','¿Desea grabar el fichero "%s" antes de cerrarlo?' % self.editor.files[curpage].label.get_text()):
						self.saveFile(widget)
			self.widgets['ntbEditor'].remove_page(curpage)
			self.editor.closefile(curpage)

	def closeFileAll(self,widget):
		"""
		Cerrar todos los archivos actualmente en edición
		"""
		modified=self.editor.modifiedfiles()
		check=False
		if modified>0:
			if self.msgDialog('question','¿Desea que se le pregunte si guardar los archivos modificados?',
				'Esisten actualmente <b>%s</b> ficheros <b>sin guardar</b>. Si responde <b>Si</b>, se le preguntará si desea guardar dichos ficheros.' % modified):
				check=True
		numfiles=len(self.editor.files)-1
		for I in range(0,numfiles+1):
			self.closeFile(widget,numfiles-I,checkmodif=check)

			
	def modifiedFile(self,widget):
		"""
		Marca una pestaña del editor como modificada
		"""
		for I in range(0,len(self.editor.files)):
			if widget==self.editor.files[I].sbuffer:
				label=self.editor.files[I].label.get_text()
				self.editor.files[I].label.set_label('<span foreground="#FF0000">' + label + '</span>')
				self.mainWindow.set_title('EVOEditor - ' + label + ' [modificado]')

	def unmodifiedFile(self,widget):
		"""
		Marca una pestaña del editor como modificada
		"""
		for I in range(0,len(self.editor.files)):
			if widget==self.editor.files[I].sbuffer:
				label=self.editor.files[I].label.get_text()
				self.editor.files[I].label.set_label('<span foreground="#000000">' + label + '</span>')
				self.mainWindow.set_title('EVOEditor - ' + label)

	def cutText(self,widget):
		"""
		Cortar el texto seleccionado
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			self.editor.cut(curpage)

	def copyText(self,widget):
		"""
		Copiar el texto seleccionado
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			self.editor.copy(curpage)

	def pasteText(self,widget):
		"""
		Pegar texto crtado/copiado
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			self.editor.paste(curpage)

	def deleteText(self,widget):
		"""
		Borrar texto seleccionado
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			self.editor.delete(curpage)

	def selectAll(self,widget):
		"""
		Seleccionar todo el texto
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			self.editor.selectall(curpage)

	def unselectText(self,widget):
		"""
		Deseleccionar
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			self.editor.unselect(curpage)

	def indentText(self,widget):
		"""
		Indentar el texto seleccionado
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			tab='\t'
			if self.config.editor['tabsasspaces']:
				tab=''
				for I in range(0,self.config.editor['tabwidth']):
					tab+=' '
			self.editor.indent(curpage,tab)

	def unindentText(self,widget):
		"""
		Desindentar texto seleccionado
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			tab='\t'
			if self.config.editor['tabsasspaces']:
				tab=''
				for I in range(0,self.config.editor['tabwidth']):
					tab+=' '
			self.editor.unindent(curpage,tab)

	def undoAction(self,widget):
		"""
		Deshacer última acción realizada
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			if not self.editor.undo(curpage):
				self.msgDialog('warning','No hay acciones que puedan deshacerse')
			else:
				if not self.editor.files[curpage].sbuffer.get_modified():
					self.unmodifiedFile(self.editor.files[curpage].sbuffer)

	def redoAction(self,widget):
		"""
		Rehacer última acción realizada
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			if not self.editor.redo(curpage):
				self.msgDialog('warning','No hay acciones que puedan rehacerse')
			else:
				if not self.editor.files[curpage].sbuffer.get_modified():
					self.unmodifiedFile(self.editor.files[curpage].sbuffer)

	def showLineNums(self,widget=None):
		"""
		Mostrar/Ocultar números de línea
		"""
		if widget:
			self.config.editor['linenums']=widget.get_active()
		else:
			self.widgets['mnuViewLineNums'].set_active(self.config.editor['linenums'])
		self.reloadEditorConfig()

	def fileStats(self,widget):
		"""
		Muestra estadísticas básicas sobre el fichero en edición
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			lines=self.editor.files[curpage].sbuffer.get_line_count()
			chars=self.editor.files[curpage].sbuffer.get_char_count()
			stats='<b>Líneas:</b> %s\n<b>Caracteres:</b> %s' % (lines,chars)
			self.msgDialog('info','Estadísticas',stats)

	def showLineMargin(self,widget=None):
		"""
		Mostrar/Ocultar margen de línea
		"""
		if widget:
			self.config.editor['margin']=widget.get_active()
		else:
			self.widgets['mnuViewLineMargin'].set_active(self.config.editor['margin'])
		self.reloadEditorConfig()

	def showLineMarkers(self,widget=None):
		"""
		Mostrar/Ocultar marcadores de línea
		"""
		if widget:
			self.config.editor['markers']=widget.get_active()
		else:
			self.widgets['mnuViewLineMarkers'].set_active(self.config.editor['markers'])
		self.reloadEditorConfig()

	def gotoLine(self,widget):
		self.widgets['entGotoLine'].set_text('')
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			resp=self.openDialog(self.gotoLineDialog)
			if resp==gtk.RESPONSE_OK:
				line=int(self.widgets['entGotoLine'].get_text().strip())
				self.editor.gotoline(curpage,line)
		self.closeDialog(self.gotoLineDialog)

	def setMarker(self,page,marker,line):
		"""
		Añadir marcador de línea
		"""
		curiter=self.editor.files[page].sbuffer.get_iter_at_line(line)
		return self.editor.files[page].sbuffer.create_marker('%s' % marker, marker, curiter)

	def highlightText(self,page,start,end,tagname=None,fg='#FFFFFF',bg='#FF0000'):
		"""
		Añadir marcador de línea
		"""
		sbuffer=self.editor.files[page].sbuffer
		if tagname:
			tag=sbuffer.get_tag_table().lookup(tagname)
			if not tag:
				tag=sbuffer.create_tag(tagname)
		else:
			tag=sbuffer.create_tag()
		tag.set_property('background',bg)
		tag.set_property('foreground',fg)
		sbuffer.apply_tag(tag,start,end)

	def setEditorLanguage(self,widget,mimetype=None):
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			if not mimetype:
				mimetype=self.srclangs[widget.get_child().get_text()][0]
			self.editor.setlang(curpage,mimetype)

	def reloadEditorConfig(self):
		"""
		Recargar configuración del editor y aplicarla en todos los ficheros
		"""
		for I in range(0,len(self.editor.files)):
			self.setPageConfig(I)

	def setPageConfig(self,page):
		"""
		Aplicar configuración actual a la página especificada
		"""
		# Propiedades del SourceBuffer
		self.editor.files[page].sbuffer.set_max_undo_levels(self.config.editor['maxundo'])
		# Propiedades del SourceView
		self.editor.files[page].srcview.set_show_line_numbers(self.config.editor['linenums'])
		self.editor.files[page].srcview.set_show_line_markers(self.config.editor['markers'])
		self.editor.files[page].srcview.set_show_margin(self.config.editor['margin'])
		self.editor.files[page].srcview.set_margin(self.config.editor['marginpos'])
		self.editor.files[page].srcview.set_auto_indent(self.config.editor['autoindent'])
		# Configuración de los tabuladores del editor
		self.editor.files[page].srcview.set_tabs_width(self.config.editor['tabwidth'])
		self.editor.files[page].srcview.set_insert_spaces_instead_of_tabs(self.config.editor['tabsasspaces'])
		self.editor.files[page].srcview.set_smart_home_end(self.config.editor['smartkeys'])

	def pageChanged(self,widget,page,pagenum):
		"""
		Detecta un cambio de página en el editor
		"""		
		self.updateStatus(page,page=pagenum)
		modified=''
		if isinstance(page,gtksourceview2.SourceBuffer):
			if self.editor.files[pagenum].sbuffer.get_modified():
				modified='[modificado]'
			filename=self.editor.files[pagenum].label.get_text()
			title='EVOEditor - %s %s' % (filename,modified)
			self.mainWindow.set_title(title)
		try:
			# Lanzar evento para los plugins
			self.plugins.event('pagechanged',{'fileid': pagenum,})
		except:
			pass

	def updateStatus(self,widget,size=None,count=None,extendsel=None,page=False):
		"""
		Actualiza la posición actual del cursor
		"""
		if not page:
			page=self.widgets['ntbEditor'].get_current_page()
		if page>-1:
			line,offset=self.editor.getcursorpos(page)
			line+=1
			if self.editor.files[page].srcview.get_overwrite():
				inssob='SOB'
			else:
				inssob='INS'
			filename=self.editor.files[page].filename
			self.widgets['lblEditorInfo'].set_text('Archivo: %s Línea: %s Col: %s %s' % (filename,line,offset,inssob))
			# Añadir texto para modificado
			# Añadir texto para nombre del ficheros

	def enhanceInput(self,widget,event):
		"""
		Controlar determinadas pulsaciones de caracteres en el editor
		para cambiar su comportamiento habitual
		"""
		# Cambiar comportamiento de la tabulación para tabular selecciones
		page=self.widgets['ntbEditor'].get_current_page()
		if page>-1:
			if event.keyval==self.keymap['tab']:
				self.indentText(widget)
				return True
			if event.keyval==self.keymap['shifttab']:
				self.unindentText(widget)
				return True
			# Teclas para acceso directo a páginas del editor
			if event.state & gtk.gdk.MOD1_MASK==gtk.gdk.MOD1_MASK:
				if event.keyval<256 and int(chr(event.keyval)) in range(1,9):
					page=int(chr(event.keyval))-1
				if event.keyval==self.keymap['home'] or event.keyval==self.keymap['up']:
					page=0
				if event.keyval==self.keymap['end'] or event.keyval==self.keymap['down']:
					page=-1
				if event.keyval==self.keymap['pgup']:
					if page>=10:
						page-=10
				if event.keyval==self.keymap['pgdown']:
					page+=10
				if event.keyval==self.keymap['left']:
					if page>0:
						page-=1
				if event.keyval==self.keymap['right']:
					page+=1
				self.widgets['ntbEditor'].set_current_page(page)
				return True
			# Propagar el evento
		return False

	def toUpper(self,widget):
		"""
		Convertir el texto seleccionado a mayúsculas
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			self.editor.toupper(curpage)
	
	def toLower(self,widget):
		"""
		Convertir el texto seleccionado a minúsculas
		"""
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			self.editor.tolower(curpage)

	def zoomEditor(self,widget=None,event=None):
		"""
		Realizar zoom sobre el editor de texto
		"""
		def zoomIn():
			"""
			Aumentar tamaño del texto
			"""
			fontsize=srcview.get_pango_context().get_font_description().get_size() / 1024
			if fontsize<32:
				fontsize+=1
				srcview.modify_font(pango.FontDescription('monospace %s' % fontsize))
			return True

		def zoomOut():
			"""
			Reducir tamaño del texto
			"""
			fontsize=srcview.get_pango_context().get_font_description().get_size() / 1024
			if fontsize>6:
				fontsize-=1
				srcview.modify_font(pango.FontDescription('monospace %s' % fontsize))
			return True
		
		curpage=self.widgets['ntbEditor'].get_current_page()
		if curpage>-1:
			srcview=self.editor.files[curpage].srcview
			if widget.get_name()=='mnuViewZoomIn':
				return zoomIn()
			if widget.get_name()=='mnuViewZoomOut':
				return zoomOut()
			if event.direction == gtk.gdk.SCROLL_UP and event.state & gtk.gdk.CONTROL_MASK==gtk.gdk.CONTROL_MASK:
				return zoomIn()
			if event.direction == gtk.gdk.SCROLL_DOWN and event.state & gtk.gdk.CONTROL_MASK==gtk.gdk.CONTROL_MASK:
				return zoomOut()
		return False

	########################################################################
	# Control básico de la aplicación
	########################################################################

	def switchFullscreen(self,widget):
		"""
		Cambiar la ventana principal al modo de pantalla completa
		"""
		status=widget.get_active()
		if status:
			self.mainWindow.fullscreen()
		else:
			self.mainWindow.unfullscreen()
		self.widgets['tlbgFullscreen'].set_active(status)
		self.widgets['mnuViewFullscreen'].set_active(status)

	def msgDialog(self,mode,msg,desc=None,parent=None,cancel=False):
		"""
		Mostrar diálogo de mensaje
		"""
		dialogmodes={
			'info': (gtk.MESSAGE_INFO,gtk.BUTTONS_OK),
			'warning': (gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE),
			'question': (gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO),
			'error': (gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE),
		}
		# Comprobamos si el modo de diálogo es correcto
		if dialogmodes.has_key(mode):
			mode=dialogmodes[mode]
			if not parent:
				parent=self.mainWindow
		else:
			parent=self.mainWindow
			mode=dialogmodes['error']
			msg='Error interno'
			desc='Se ha producido un error al definir un diálogo de mensaje'
		# Creación del diálogo
		dialog=gtk.MessageDialog(parent,gtk.DIALOG_MODAL and gtk.DIALOG_DESTROY_WITH_PARENT,mode[0],mode[1])
		if cancel:
			dialog.add_button('Cancelar', 1)
		# Añadir el mensaje del diálogo
		dialog.set_markup('<b>' + msg + '</b>')
		# Añadir mensaje secundario si se ha especificado
		if desc:
			dialog.format_secondary_markup(desc)
		# Mostrar diálogo y recoger respuesta
		resp=dialog.run()
		# Interpretación de la respuesta
		if cancel:
			if resp==1:
				resp='cancel'
			else:
				resp=resp==gtk.RESPONSE_YES
		else:
			resp=resp==gtk.RESPONSE_YES
		# Cierre del diálogo
		dialog.destroy()
		return resp

	def statusMessage(self,context,message,desc=None,showdialog=False):
		"""
		Mostrar un mensaje de estado
		"""
		contextid=self.widgets['stbMain'].get_context_id(context)
		self.widgets['stbMain'].pop(contextid)
		self.widgets['stbMain'].push(contextid,message)
		if desc or showdialog:
			self.msgDialog(context,message)

	def openDialog(self,dialog,delete=False,close=False):
		"""
		Mostrar un dialogo
		"""
		resp=dialog.run()
		if (not delete and resp==gtk.RESPONSE_DELETE_EVENT) or close:
			self.closeDialog(dialog)
		return resp
		
	def closeDialog(self,dialog):
		"""
		Cerrar un diálogo
		"""
		dialog.hide()
		return True

	def quitProgram(self,widget,event=None):
		"""
		Comprueba los archivos no guardados y muestra el diálogo de confirmación de salida
		"""
		if self.msgDialog('question','¿Realmente desea salir de EVOEditor?'):
			self.closeFileAll(widget)
			gtk.main_quit()
		return True

	def htmlColor(self,color):
		"""
		Convertir una instancia de gtk.gdk.Color() en color HTML
		"""
		r=hex(color.red/256)[2:].upper()
		g=hex(color.green/256)[2:].upper()
		b=hex(color.blue/256)[2:].upper()
		if len(r)<2: r='0'+r
		if len(g)<2: g='0'+g
		if len(b)<2: b='0'+b
		return '#%s%s%s' % (r,g,b)

	def pruebakey(self,widget,event):
		"""
		Comprobar teclas pulsadas sobre un control
		"""
		print event.keyval

	def prueba(self, widget, event):
		"""
		Comprobar eventos
		"""
		print event.type
		print dir(event)

# Programa principal
if __name__=='__main__':
	pass
