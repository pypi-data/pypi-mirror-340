from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AngleCls:
	"""Angle commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("angle", core, parent)

	def set(self, dep_angle: float, mimoTap=repcap.MimoTap.Default, ray=repcap.Ray.Default) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:MIMO:TAP<CH>:TGN:RAY<ST>:DEParture:ANGLe \n
		Snippet: driver.source.fsimulator.mimo.tap.tgn.ray.departure.angle.set(dep_angle = 1.0, mimoTap = repcap.MimoTap.Default, ray = repcap.Ray.Default) \n
		Sets the AoA (Angle of Arrival) / AoD (Angle of Departure) of the selected ray. \n
			:param dep_angle: float Range: 0 to 359.999
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:param ray: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ray')
		"""
		param = Conversions.decimal_value_to_str(dep_angle)
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		ray_cmd_val = self._cmd_group.get_repcap_cmd_value(ray, repcap.Ray)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:MIMO:TAP{mimoTap_cmd_val}:TGN:RAY{ray_cmd_val}:DEParture:ANGLe {param}')

	def get(self, mimoTap=repcap.MimoTap.Default, ray=repcap.Ray.Default) -> float:
		"""SCPI: [SOURce<HW>]:FSIMulator:MIMO:TAP<CH>:TGN:RAY<ST>:DEParture:ANGLe \n
		Snippet: value: float = driver.source.fsimulator.mimo.tap.tgn.ray.departure.angle.get(mimoTap = repcap.MimoTap.Default, ray = repcap.Ray.Default) \n
		Sets the AoA (Angle of Arrival) / AoD (Angle of Departure) of the selected ray. \n
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:param ray: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ray')
			:return: dep_angle: float Range: 0 to 359.999"""
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		ray_cmd_val = self._cmd_group.get_repcap_cmd_value(ray, repcap.Ray)
		response = self._core.io.query_str(f'SOURce<HwInstance>:FSIMulator:MIMO:TAP{mimoTap_cmd_val}:TGN:RAY{ray_cmd_val}:DEParture:ANGLe?')
		return Conversions.str_to_float(response)
