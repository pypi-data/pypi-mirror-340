from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TdurationCls:
	"""Tduration commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tduration", core, parent)

	def get_sone(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PKEY:TDURation:SONE \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.pkey.tduration.get_sone() \n
		Sets the duration of step 1 for Public key transitions. \n
			:return: duration: integer Range: 1 to 86400
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PKEY:TDURation:SONE?')
		return Conversions.str_to_int(response)

	def set_sone(self, duration: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PKEY:TDURation:SONE \n
		Snippet: driver.source.bb.gnss.galileo.osnma.pkey.tduration.set_sone(duration = 1) \n
		Sets the duration of step 1 for Public key transitions. \n
			:param duration: integer Range: 1 to 86400
		"""
		param = Conversions.decimal_value_to_str(duration)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PKEY:TDURation:SONE {param}')

	def get_stwo(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PKEY:TDURation:STWO \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.pkey.tduration.get_stwo() \n
		Sets the duration of step 2 for Public key transitions. \n
			:return: duration: integer Range: 1 to 86400
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PKEY:TDURation:STWO?')
		return Conversions.str_to_int(response)

	def set_stwo(self, duration: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PKEY:TDURation:STWO \n
		Snippet: driver.source.bb.gnss.galileo.osnma.pkey.tduration.set_stwo(duration = 1) \n
		Sets the duration of step 2 for Public key transitions. \n
			:param duration: integer Range: 1 to 86400
		"""
		param = Conversions.decimal_value_to_str(duration)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PKEY:TDURation:STWO {param}')
