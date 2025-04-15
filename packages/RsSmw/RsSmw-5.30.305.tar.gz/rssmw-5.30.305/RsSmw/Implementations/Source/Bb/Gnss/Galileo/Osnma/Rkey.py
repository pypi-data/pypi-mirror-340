from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RkeyCls:
	"""Rkey commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rkey", core, parent)

	def get_nt_day(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:RKEY:NTDay \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.rkey.get_nt_day() \n
		Sets the number of root key transitions per day. \n
			:return: trans_per_day: integer Range: 1 to 24
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:RKEY:NTDay?')
		return Conversions.str_to_int(response)

	def set_nt_day(self, trans_per_day: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:RKEY:NTDay \n
		Snippet: driver.source.bb.gnss.galileo.osnma.rkey.set_nt_day(trans_per_day = 1) \n
		Sets the number of root key transitions per day. \n
			:param trans_per_day: integer Range: 1 to 24
		"""
		param = Conversions.decimal_value_to_str(trans_per_day)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:RKEY:NTDay {param}')

	def get_to_midnight(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:RKEY:TOMidnight \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.rkey.get_to_midnight() \n
		Sets a time offset of the TESLA chain transitions per day. \n
			:return: time_offset: integer Range: 0 to 86400
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:RKEY:TOMidnight?')
		return Conversions.str_to_int(response)

	def set_to_midnight(self, time_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:RKEY:TOMidnight \n
		Snippet: driver.source.bb.gnss.galileo.osnma.rkey.set_to_midnight(time_offset = 1) \n
		Sets a time offset of the TESLA chain transitions per day. \n
			:param time_offset: integer Range: 0 to 86400
		"""
		param = Conversions.decimal_value_to_str(time_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:RKEY:TOMidnight {param}')
