# -*- coding: utf-8 -*-
###############################################################################
# (C) 2007 EVO Sistemas Libres <central@evosistemas.com>
# editor.py
# Clase de control del editor de EVOEditor
###############################################################################

import gtk,gtksourceview2

class EditorFile:
	"""
	Clase para almacenar los datos de un archivo en edición
	"""
	def __init__(self,filename,sbuffer,lang,scroll,srcview,label,button):
		"""
		Constructor de la clase
		"""
		self.filename=filename
		self.scroll=scroll
		self.sbuffer=sbuffer
		self.lang=lang
		self.srcview=srcview
		self.label=label
		self.button=button
		self.curpos=None

class EditorHelper:
	"""
	Clase de operaciones internas del editor de EVOEditor
	"""
	def __init__(self):
		"""
		Constructor
		"""
		# Lista de archivos en edición
		self.files=[]
		# Clipboard del editor
		self.clipboard=gtk.Clipboard()

	def dummyfile(self):
		"""
		Añade un archivo falso para crear pestañas en el editor
		"""
		self.files.append(None)

	def newfile(self,filename,sbuffer,lang,scroll,srcview,label,button):
		"""
		Crear un nuevo archivo para edición
		"""
		self.files.append(EditorFile(filename,sbuffer,lang,scroll,srcview,label,button))

	def closefile(self,page):
		"""
		Cerrar un archivo en edición
		"""
		del(self.files[page])

	def cut(self,page):
		"""
		Cortar texto seleccionado al portapapeles
		"""
		sbuffer=self.files[page].sbuffer
		if sbuffer.get_has_selection():
			sbuffer.cut_clipboard(self.clipboard,True)
	
	def copy(self,page):
		"""
		Copiar texto seleccionado al portapapeles
		"""
		sbuffer=self.files[page].sbuffer
		if sbuffer.get_has_selection():
			sbuffer.copy_clipboard(self.clipboard)
	
	def paste(self,page):
		"""
		Pegar texto del portapapeles en la posición del cursor
		"""
		self.files[page].sbuffer.paste_clipboard(self.clipboard, None, True)
	
	def delete(self,page):
		"""
		Elimina el texto seleccionado
		"""
		sbuffer=self.files[page].sbuffer
		if sbuffer.get_has_selection():
			sbuffer.delete_selection(False, False)

	def selectall(self,page):
		"""
		Selecciona todo el texto
		"""
		sbuffer=self.files[page].sbuffer
		start,end=sbuffer.get_bounds()
		self.files[page].curpos=sbuffer.get_iter_at_offset(sbuffer.get_property('cursor-position'))
		sbuffer.select_range(start,end)

	def unselect(self,page):
		"""
		Selecciona todo el texto
		"""
		sbuffer=self.files[page].sbuffer
		if not self.files[page].curpos:
			self.files[page].curpos=sbuffer.get_start_iter()
		sbuffer.place_cursor(self.files[page].curpos)

	def indent(self,page,tab):
		"""
		Indentar texto seleccionado o cursor actual con el caracter de tabulación especificado
		"""
		sbuffer=self.files[page].sbuffer
		if sbuffer.get_has_selection():
			# Indentar toda la selección
			selstart,selend=sbuffer.get_selection_bounds()
			startline=selstart.get_line()
			endline=selend.get_line()
			for line in range(startline,endline+1):
				sbuffer.insert(sbuffer.get_iter_at_line_offset(line,0),tab)
		else:
			# Indentar solo línea actual
			curiter=sbuffer.get_iter_at_offset(sbuffer.get_property('cursor-position'))
			sbuffer.insert(curiter,tab)

	def unindent(self,page,tab):
		"""
		Desindentar texto seleccionado o cursor actual con el caracter de tabulación especificado
		"""
		sbuffer=self.files[page].sbuffer
		if sbuffer.get_has_selection():
			# Desindentar toda la selección
			selstart,selend=sbuffer.get_selection_bounds()
			startline=selstart.get_line()
			endline=selend.get_line()
			for line in range(startline,endline+1):
				# Comprobar si se puede desindentar
				starttab=sbuffer.get_iter_at_line_offset(line,0)
				if not starttab.ends_line() and starttab.get_chars_in_line()>len(tab):
					endtab=sbuffer.get_iter_at_line_offset(line,len(tab))
					if tab==sbuffer.get_text(starttab,endtab):
						sbuffer.delete(starttab,endtab)
		else:
			# Desindentar solo línea actual
			curiter=sbuffer.get_iter_at_offset(sbuffer.get_property('cursor-position'))
			line=curiter.get_line()
			starttab=sbuffer.get_iter_at_line_offset(line,0)
			if not starttab.ends_line():
				endtab=sbuffer.get_iter_at_line_offset(line,len(tab))
				if tab==sbuffer.get_text(starttab,endtab):
					sbuffer.delete(starttab,endtab)

	def undo(self,page):
		"""
		Deshacer la última acción
		"""
		sbuffer=self.files[page].sbuffer
		srcview=self.files[page].srcview
		if sbuffer.can_undo():
			sbuffer.undo()
			line,pos=self.getcursorpos(page)
			srcview.scroll_to_iter(sbuffer.get_iter_at_line_offset(line,0),0.4)
		else:
			return False
		return True

	def redo(self,page):
		"""
		Rehacer la última acción
		"""
		sbuffer=self.files[page].sbuffer
		srcview=self.files[page].srcview
		if sbuffer.can_redo():
			sbuffer.redo()
			line,pos=self.getcursorpos(page)
			srcview.scroll_to_iter(sbuffer.get_iter_at_line_offset(line,0),0.4)
		else:
			return False
		return True

	def loaddata(self,sbuffer,filename):
		"""
		Cargar datos de un fichero en un editor
		"""
		# Cargar contenido del ficheros
		try:
			fd=open(filename,'r')
			data=fd.read()
			fd.close()
		except:
			return False
		# Inicio y final del buffer
		startiter,enditer=sbuffer.get_bounds()
		# Hacer una acción undoable para la carga del fichero
		sbuffer.begin_not_undoable_action()
		sbuffer.set_text(data)
		sbuffer.set_modified(False)
		sbuffer.place_cursor(sbuffer.get_start_iter())
		# Finalizar acción undoable
		sbuffer.end_not_undoable_action()
		return True

	def savedata(self,sbuffer,filename):
		"""
		Grabar datos de un editor a un fichero
		"""
		# Inicio y final del buffer
		startiter,enditer=sbuffer.get_bounds()
		# Cargar datos del buffer
		data=startiter.get_text(enditer)
		# Guardar contenido en el ficheros
		try:
			fd=open(filename,'w')
			data=fd.write(data)
			fd.close()
			sbuffer.set_modified(False)
		except:
			return False
		return True

	def setlang(self,page,mimetype):
		print mimetype
		slmanager=gtksourceview2.SourceLanguagesManager()
		lang=slmanager.get_language_from_mime_type(mimetype)
		# Aplicamos la configuración al buffer de edición
		self.files[page].sbuffer.set_language(lang)
		self.files[page].sbuffer.set_highlight(True)
		# Guardamos los datos para el fichero actual
		self.files[page].lang=lang

	def modifiedfiles(self):
		"""
		Devolver el número de archivos que han sido modificados después
		de su creación, carga o última grabación
		"""
		modified=0
		for file in self.files:
			if file.sbuffer.get_modified():
				modified+=1
		return modified

	def gotoline(self,page,line):
		"""
		Colocar cursor en la línea especificada
		"""
		sbuffer=self.files[page].sbuffer
		srcview=self.files[page].srcview
		lines=sbuffer.get_line_count()
		if line>lines:
			line=lines
		cur=sbuffer.get_iter_at_line(line-1)
		sbuffer.place_cursor(cur)
		srcview.scroll_to_iter(cur,0.4)
		
	def toupper(self,page):
		"""
		Convertir texto seleccionado a mayúsculas
		"""
		sbuffer=self.files[page].sbuffer
		if sbuffer.get_has_selection():
			sbuffer.begin_not_undoable_action()
			selstart,selend=sbuffer.get_selection_bounds()
			text=sbuffer.get_text(selstart,selend)
			sbuffer.insert(selstart,text.upper())
			sbuffer.delete_selection(False,False)
			sbuffer.end_not_undoable_action()
	
	def tolower(self,page):
		"""
		Convertir texto seleccionado a mayúsculas
		"""
		sbuffer=self.files[page].sbuffer
		if sbuffer.get_has_selection():
			sbuffer.begin_not_undoable_action()
			selstart,selend=sbuffer.get_selection_bounds()
			text=sbuffer.get_text(selstart,selend)
			sbuffer.insert(selstart,text.lower())
			sbuffer.delete_selection(False,False)
			sbuffer.end_not_undoable_action()

	def getcursorpos(self,page):
		"""
		Devolver posición actual del cursor (line,offset)
		"""
		curiter=self.files[page].sbuffer.get_iter_at_offset(self.files[page].sbuffer.get_property('cursor-position'))
		line=curiter.get_line()
		offset=curiter.get_line_offset()
		return (line,offset)
		
