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
		"""SCPI: [SOURce<HW>]:FSIMulator:DEL:TYPE<CH>:UNIT \n
		Snippet: driver.source.fsimulator.delPy.typePy.unit.set(delay_unit = enums.UnitTimeSecMsUsNsPs.MS, typePy = repcap.TypePy.Default) \n
		Sets the delay unit for the values of the basic delay, additional delay and resulting delay. Note that this setting only
		changes the Doppler unit in local mode. To set the speed units via remote control set the unit after the speed value. \n
			:param delay_unit: S| MS| US| NS| PS
			:param typePy: optional repeated capability selector. Default value: Nr1 (settable in the interface 'TypePy')
		"""
		param = Conversions.enum_scalar_to_str(delay_unit, enums.UnitTimeSecMsUsNsPs)
		typePy_cmd_val = self._cmd_group.get_repcap_cmd_value(typePy, repcap.TypePy)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:DEL:TYPE{typePy_cmd_val}:UNIT {param}')

	# noinspection PyTypeChecker
	def get(self, typePy=repcap.TypePy.Default) -> enums.UnitTimeSecMsUsNsPs:
		"""SCPI: [SOURce<HW>]:FSIMulator:DEL:TYPE<CH>:UNIT \n
		Snippet: value: enums.UnitTimeSecMsUsNsPs = driver.source.fsimulator.delPy.typePy.unit.get(typePy = repcap.TypePy.Default) \n
		Sets the delay unit for the values of the basic delay, additional delay and resulting delay. Note that this setting only
		changes the Doppler unit in local mode. To set the speed units via remote control set the unit after the speed value. \n
			:param typePy: optional repeated capability selector. Default value: Nr1 (settable in the interface 'TypePy')
			:return: delay_unit: S| MS| US| NS| PS"""
		typePy_cmd_val = self._cmd_group.get_repcap_cmd_value(typePy, repcap.TypePy)
		response = self._core.io.query_str(f'SOURce<HwInstance>:FSIMulator:DEL:TYPE{typePy_cmd_val}:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.UnitTimeSecMsUsNsPs)
