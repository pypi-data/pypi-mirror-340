from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FphrCls:
	"""Fphr commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fphr", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:FPhr:STATe \n
		Snippet: value: bool = driver.source.bb.huwb.fconfig.fphr.get_state() \n
		Queries the state of the forward error correction in the PHY header. Enables or disables the forward error correction in
		the PHY header automatically, depending on the selected operating band and SFD. \n
			:return: fecin_phr: 1| ON| 0| OFF 0 For [:SOURcehw]:BB:HUWB:OBANd OB780|OB868|OB915|OB2380|OB2450. For [:SOURcehw]:BB:HUWB:OBANd OB5800|OB6200 and [:SOURcehw]:BB:HUWB:SFD SFD_0. 1 For [:SOURcehw]:BB:HUWB:OBANd OB5800|OB6200 and [:SOURcehw]:BB:HUWB:SFD SFD_1|SFD_2|SFD_3|SFD_4.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:FPhr:STATe?')
		return Conversions.str_to_bool(response)
