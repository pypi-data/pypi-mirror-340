from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScodeCls:
	"""Scode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scode", core, parent)

	def get_step(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:SCODe:STEP \n
		Snippet: value: str = driver.source.bb.w3Gpp.mstation.additional.scode.get_step() \n
		Sets the step width for increasing the scrambling code of the additional user equipment. The start value is the
		scrambling code of UE4. \n
			:return: step: integer Range: 0 to #HFFFFFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:SCODe:STEP?')
		return trim_str_response(response)

	def set_step(self, step: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:SCODe:STEP \n
		Snippet: driver.source.bb.w3Gpp.mstation.additional.scode.set_step(step = rawAbc) \n
		Sets the step width for increasing the scrambling code of the additional user equipment. The start value is the
		scrambling code of UE4. \n
			:param step: integer Range: 0 to #HFFFFFF
		"""
		param = Conversions.value_to_str(step)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:SCODe:STEP {param}')
