# -*- coding: utf-8 -*-
################################################################################
# (C) 2007 EVO Sistemas Libres <central@evosistemas.com>
# plugin.py
# Módulo para manejo de plugins de EVOEditor
################################################################################

# Importaciones de Python
import os

class PluginHelper:
	"""
	Clase encargada de la gestión de los plugins del editor
	"""
	def __init__(self,gui):
		"""
		Inicialización de la clase de gestión de Plugins
		"""
		self.available={}
		self.gui=gui
		self.load()

	def load(self):
		"""
		Lee el directorio de plugins y carga sus definiciones
		"""
		# Limpiar definiciones previamente cargadas
		self.available={}
		# Buscar plugins en el directorio de plugins
		ls=os.listdir('./plugins')
		for pluginid in ls:
			if os.path.isdir('./plugins/' + pluginid):
				try:
					plugin=Plugin(pluginid)
					self.available[pluginid]=plugin
				except Exception, detail:
					self.gui.msgDialog('error','Error al cargar el plugin %s' % pluginid,detail.message)

	def enable(self,pluginid):
		"""
		Activa el plugin especificado
		"""
		if self.available.has_key(pluginid):
			self.available[pluginid].enable(self.gui)

	def disable(self,pluginid):
		"""
		Desactiva el plugin especificado
		"""
		if self.available.has_key(pluginid):
			self.available[pluginid].disable(self.gui)

	def event(self,event,parms):
		"""
		Ejecuta un evento para todos los plugins activos
		"""
		for I in self.available:
			if self.available[I].enabled:
				if event=='newfile':
					self.available[I].instance.newFile(parms)
				if event=='closefile':
					self.available[I].instance.closeFile(parms)
				if event=='pagechanged':
					self.available[I].instance.pageChanged(parms)

class Plugin:
	"""
	Clase de representación de un plugin
	"""
	def __init__(self,pluginid):
		"""
		Constructor del plugin
		"""
		self.mod=__import__('plugins.%s' % pluginid,globals(),locals(),[pluginid],-1)
		self.pluginid=pluginid
		self.name=self.mod.PLUGIN_NAME
		self.configurable=self.mod.PLUGIN_CONFIGURABLE
		self.enabled=False

	def enable(self,gui):
		"""
		Activar el plugin si está inactivo
		"""
		if not self.enabled:
			try:
				self.instance=self.mod.PluginLoader(gui)
				self.enabled=True
			except Exception, detail:
				gui.msgDialog('error','Error al activar el plugin %s' % self.name,detail.message)

	def disable(self,gui):
		"""
		Desactivar el plugin si está activo
		"""
		if self.enabled:
			try:
				self.instance.disable()
				del(self.instance)
				self.enabled=False
			except Exception, detail:
				gui.msgDialog('error','Error al desactivar el plugin %s' % self.name,detail.message)

	def showconfig(self,widget=None):
		"""
		Mostrar diálogo de configuración del plugin
		"""
		if self.configurable and self.enabled:
			self.instance.showConfig()
