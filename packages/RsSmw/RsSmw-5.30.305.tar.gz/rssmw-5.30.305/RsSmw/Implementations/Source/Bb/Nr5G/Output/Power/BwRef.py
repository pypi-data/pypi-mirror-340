from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwRefCls:
	"""BwRef commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bwRef", core, parent)

	def get_acrl(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:POWer:BWRef:ACRL \n
		Snippet: value: float = driver.source.bb.nr5G.output.power.bwRef.get_acrl() \n
		Queries the bandwidths/numerologies with their power levels. \n
			:return: act_pow_rel_lvl_pbw: float Range: -80 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:POWer:BWRef:ACRL?')
		return Conversions.str_to_float(response)
