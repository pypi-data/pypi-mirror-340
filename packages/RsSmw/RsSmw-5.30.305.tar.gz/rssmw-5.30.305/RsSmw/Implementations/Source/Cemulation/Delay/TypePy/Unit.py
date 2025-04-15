from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UnitCls:
	"""Unit commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("unit", core, parent)

	def set(self, delay_unit: enums.UnitTimeSecMsUsNsPs, typePy=repcap.TypePy.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:DELay:TYPE<CH>:UNIT \n
		Snippet: driver.source.cemulation.delay.typePy.unit.set(delay_unit = enums.UnitTimeSecMsUsNsPs.MS, typePy = repcap.TypePy.Default) \n
		No command help available \n
			:param delay_unit: No help available
			:param typePy: optional repeated capability selector. Default value: Nr1 (settable in the interface 'TypePy')
		"""
		param = Conversions.enum_scalar_to_str(delay_unit, enums.UnitTimeSecMsUsNsPs)
		typePy_cmd_val = self._cmd_group.get_repcap_cmd_value(typePy, repcap.TypePy)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:DELay:TYPE{typePy_cmd_val}:UNIT {param}')

	# noinspection PyTypeChecker
	def get(self, typePy=repcap.TypePy.Default) -> enums.UnitTimeSecMsUsNsPs:
		"""SCPI: [SOURce<HW>]:CEMulation:DELay:TYPE<CH>:UNIT \n
		Snippet: value: enums.UnitTimeSecMsUsNsPs = driver.source.cemulation.delay.typePy.unit.get(typePy = repcap.TypePy.Default) \n
		No command help available \n
			:param typePy: optional repeated capability selector. Default value: Nr1 (settable in the interface 'TypePy')
			:return: delay_unit: No help available"""
		typePy_cmd_val = self._cmd_group.get_repcap_cmd_value(typePy, repcap.TypePy)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:DELay:TYPE{typePy_cmd_val}:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.UnitTimeSecMsUsNsPs)
