from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DzCls:
	"""Dz commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dz", core, parent)

	def set(self, delta_z: float, baseSt=repcap.BaseSt.Default, antenna=repcap.Antenna.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BASE<ST>:A<CH>:DZ \n
		Snippet: driver.source.bb.gnss.rtk.base.a.dz.set(delta_z = 1.0, baseSt = repcap.BaseSt.Default, antenna = repcap.Antenna.Default) \n
		Sets the antenna position of an RTK base station as an offset on the x, y and z axis. The offset is relative to center of
		gravity (COG) . \n
			:param delta_z: float Range: -200 to 200
			:param baseSt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Base')
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
		"""
		param = Conversions.decimal_value_to_str(delta_z)
		baseSt_cmd_val = self._cmd_group.get_repcap_cmd_value(baseSt, repcap.BaseSt)
		antenna_cmd_val = self._cmd_group.get_repcap_cmd_value(antenna, repcap.Antenna)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RTK:BASE{baseSt_cmd_val}:A{antenna_cmd_val}:DZ {param}')

	def get(self, baseSt=repcap.BaseSt.Default, antenna=repcap.Antenna.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BASE<ST>:A<CH>:DZ \n
		Snippet: value: float = driver.source.bb.gnss.rtk.base.a.dz.get(baseSt = repcap.BaseSt.Default, antenna = repcap.Antenna.Default) \n
		Sets the antenna position of an RTK base station as an offset on the x, y and z axis. The offset is relative to center of
		gravity (COG) . \n
			:param baseSt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Base')
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
			:return: delta_z: float Range: -200 to 200"""
		baseSt_cmd_val = self._cmd_group.get_repcap_cmd_value(baseSt, repcap.BaseSt)
		antenna_cmd_val = self._cmd_group.get_repcap_cmd_value(antenna, repcap.Antenna)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RTK:BASE{baseSt_cmd_val}:A{antenna_cmd_val}:DZ?')
		return Conversions.str_to_float(response)
