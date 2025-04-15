from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FcontrolCls:
	"""Fcontrol commands group definition. 13 total commands, 0 Subgroups, 13 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fcontrol", core, parent)

	def get_cf_extension(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:CFEXtension \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_cf_extension() \n
		Set the value of the individual bits of the frame control field. \n
			:return: extension: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:CFEXtension?')
		return trim_str_response(response)

	def set_cf_extension(self, extension: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:CFEXtension \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_cf_extension(extension = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param extension: 2 bits
		"""
		param = Conversions.value_to_str(extension)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:CFEXtension {param}')

	def get_fds(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:FDS \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_fds() \n
		Set the value of the individual bits of the frame control field. \n
			:return: fds: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:FDS?')
		return trim_str_response(response)

	def set_fds(self, fds: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:FDS \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_fds(fds = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param fds: 2 bits
		"""
		param = Conversions.value_to_str(fds)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:FDS {param}')

	def get_mdata(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:MDATa \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_mdata() \n
		Set the value of the individual bits of the frame control field. \n
			:return: mdata: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:MDATa?')
		return trim_str_response(response)

	def set_mdata(self, mdata: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:MDATa \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_mdata(mdata = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param mdata: 2 bits
		"""
		param = Conversions.value_to_str(mdata)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:MDATa {param}')

	def get_mfragments(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:MFRagments \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_mfragments() \n
		Set the value of the individual bits of the frame control field. \n
			:return: mfragments: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:MFRagments?')
		return trim_str_response(response)

	def set_mfragments(self, mfragments: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:MFRagments \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_mfragments(mfragments = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param mfragments: 2 bits
		"""
		param = Conversions.value_to_str(mfragments)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:MFRagments {param}')

	def get_order(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:ORDer \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_order() \n
		Set the value of the individual bits of the frame control field. \n
			:return: order: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:ORDer?')
		return trim_str_response(response)

	def set_order(self, order: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:ORDer \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_order(order = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param order: 2 bits
		"""
		param = Conversions.value_to_str(order)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:ORDer {param}')

	def get_pframe(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:PFRame \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_pframe() \n
		Set the value of the individual bits of the frame control field. \n
			:return: protd_frm: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:PFRame?')
		return trim_str_response(response)

	def set_pframe(self, protd_frm: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:PFRame \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_pframe(protd_frm = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param protd_frm: 2 bits
		"""
		param = Conversions.value_to_str(protd_frm)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:PFRame {param}')

	def get_pmanagement(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:PMANagement \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_pmanagement() \n
		Set the value of the individual bits of the frame control field. \n
			:return: pmanagement: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:PMANagement?')
		return trim_str_response(response)

	def set_pmanagement(self, pmanagement: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:PMANagement \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_pmanagement(pmanagement = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param pmanagement: 2 bits
		"""
		param = Conversions.value_to_str(pmanagement)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:PMANagement {param}')

	def get_pversion(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:PVERsion \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_pversion() \n
		Set the value of the individual bits of the frame control field. \n
			:return: pversion: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:PVERsion?')
		return trim_str_response(response)

	def set_pversion(self, pversion: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:PVERsion \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_pversion(pversion = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param pversion: 2 bits
		"""
		param = Conversions.value_to_str(pversion)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:PVERsion {param}')

	def get_retry(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:RETRy \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_retry() \n
		Set the value of the individual bits of the frame control field. \n
			:return: retry: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:RETRy?')
		return trim_str_response(response)

	def set_retry(self, retry: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:RETRy \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_retry(retry = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param retry: 2 bits
		"""
		param = Conversions.value_to_str(retry)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:RETRy {param}')

	def get_sub_type(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:SUBType \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_sub_type() \n
		Set the value of the individual bits of the frame control field. \n
			:return: sub_type: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:SUBType?')
		return trim_str_response(response)

	def set_sub_type(self, sub_type: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:SUBType \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_sub_type(sub_type = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param sub_type: 2 bits
		"""
		param = Conversions.value_to_str(sub_type)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:SUBType {param}')

	def get_tds(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:TDS \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_tds() \n
		Set the value of the individual bits of the frame control field. \n
			:return: tds: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:TDS?')
		return trim_str_response(response)

	def set_tds(self, tds: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:TDS \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_tds(tds = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param tds: 2 bits
		"""
		param = Conversions.value_to_str(tds)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:TDS {param}')

	def get_type_py(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:TYPE \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_type_py() \n
		Set the value of the individual bits of the frame control field. \n
			:return: type_py: 2 bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:TYPE?')
		return trim_str_response(response)

	def set_type_py(self, type_py: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol:TYPE \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_type_py(type_py = rawAbc) \n
		Set the value of the individual bits of the frame control field. \n
			:param type_py: 2 bits
		"""
		param = Conversions.value_to_str(type_py)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol:TYPE {param}')

	def get_value(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.mac.fcontrol.get_value() \n
		Sets the value of the frame control field. The frame control field has a length of 2 bytes (16 bits) and is used to
		define, for example, the protocol version, the frame type, and its function. As an alternative, the individual bits can
		be set. \n
			:return: fcontrol: 16 bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol?')
		return trim_str_response(response)

	def set_value(self, fcontrol: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MAC:FCONtrol \n
		Snippet: driver.source.bb.wlad.pconfig.mac.fcontrol.set_value(fcontrol = rawAbc) \n
		Sets the value of the frame control field. The frame control field has a length of 2 bytes (16 bits) and is used to
		define, for example, the protocol version, the frame type, and its function. As an alternative, the individual bits can
		be set. \n
			:param fcontrol: 16 bits
		"""
		param = Conversions.value_to_str(fcontrol)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MAC:FCONtrol {param}')
