from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdopplerCls:
	"""Fdoppler commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdoppler", core, parent)

	@property
	def actual(self):
		"""actual commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_actual'):
			from .Actual import ActualCls
			self._actual = ActualCls(self._core, self._cmd_group)
		return self._actual

	def set(self, fdoppler: float, fadingGroup=repcap.FadingGroup.Default, path=repcap.Path.Default) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:MDELay:DEL30:GROup<ST>:PATH<CH>:FDOPpler \n
		Snippet: driver.source.fsimulator.mdelay.del30.group.path.fdoppler.set(fdoppler = 1.0, fadingGroup = repcap.FadingGroup.Default, path = repcap.Path.Default) \n
		Queries the resulting Doppler frequency for the fading configuration. The Doppler frequency is determined by the selected
		speed ([:SOURce<hw>]:FSIMulator:DELay|DEL:GROup<st>:PATH<ch>:SPEed) . For the Pure Doppler and Rice fading profiles, the
		actual Doppler shift is a function of the selected ratio of the Doppler shift to the Doppler frequency
		([:SOURce<hw>]:FSIMulator:DELay|DEL:GROup<st>:PATH<ch>:FRATio) .
		Use the command [:SOURce<hw>]:FSIMulator:DELay|DEL:GROup<st>:PATH<ch>:FDOPpler:ACTual? to query the actual Doppler shift. \n
			:param fdoppler: float Range: 0 to max*, Unit: Hz *) Option: R&S SMW-B14 max = 4000 R&S SMW-B15 max depends on the System Configuration LxMxN and profile as follows: Lx1x1 with L = 1 to 8: max = 4000 1x2x2/2x2x2/2x2x1/2x1x2/3x2x2/4x2x2/1x2x4/1x4x2: max = 4000 1x2x8/1x8x2/1x4x4/2x4x4/2x2x4: max = 2000 1x8x4/1x4x8/2x4x4: max = 600 1x8x8 (subset 1 or 2) : max = 300 (R&S SMW-K821) 1x8x8 (all subsets) : max = 150 (R&S SMW-B15/K75) [:SOURcehw]:FSIMulator:DELay|DEL:GROupst:PATHch:PROFile BELLindoor|BELVehicle: max = 50
			:param fadingGroup: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
		"""
		param = Conversions.decimal_value_to_str(fdoppler)
		fadingGroup_cmd_val = self._cmd_group.get_repcap_cmd_value(fadingGroup, repcap.FadingGroup)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:MDELay:DEL30:GROup{fadingGroup_cmd_val}:PATH{path_cmd_val}:FDOPpler {param}')

	def get(self, fadingGroup=repcap.FadingGroup.Default, path=repcap.Path.Default) -> float:
		"""SCPI: [SOURce<HW>]:FSIMulator:MDELay:DEL30:GROup<ST>:PATH<CH>:FDOPpler \n
		Snippet: value: float = driver.source.fsimulator.mdelay.del30.group.path.fdoppler.get(fadingGroup = repcap.FadingGroup.Default, path = repcap.Path.Default) \n
		Queries the resulting Doppler frequency for the fading configuration. The Doppler frequency is determined by the selected
		speed ([:SOURce<hw>]:FSIMulator:DELay|DEL:GROup<st>:PATH<ch>:SPEed) . For the Pure Doppler and Rice fading profiles, the
		actual Doppler shift is a function of the selected ratio of the Doppler shift to the Doppler frequency
		([:SOURce<hw>]:FSIMulator:DELay|DEL:GROup<st>:PATH<ch>:FRATio) .
		Use the command [:SOURce<hw>]:FSIMulator:DELay|DEL:GROup<st>:PATH<ch>:FDOPpler:ACTual? to query the actual Doppler shift. \n
			:param fadingGroup: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
			:return: fdoppler: float Range: 0 to max*, Unit: Hz *) Option: R&S SMW-B14 max = 4000 R&S SMW-B15 max depends on the System Configuration LxMxN and profile as follows: Lx1x1 with L = 1 to 8: max = 4000 1x2x2/2x2x2/2x2x1/2x1x2/3x2x2/4x2x2/1x2x4/1x4x2: max = 4000 1x2x8/1x8x2/1x4x4/2x4x4/2x2x4: max = 2000 1x8x4/1x4x8/2x4x4: max = 600 1x8x8 (subset 1 or 2) : max = 300 (R&S SMW-K821) 1x8x8 (all subsets) : max = 150 (R&S SMW-B15/K75) [:SOURcehw]:FSIMulator:DELay|DEL:GROupst:PATHch:PROFile BELLindoor|BELVehicle: max = 50"""
		fadingGroup_cmd_val = self._cmd_group.get_repcap_cmd_value(fadingGroup, repcap.FadingGroup)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SOURce<HwInstance>:FSIMulator:MDELay:DEL30:GROup{fadingGroup_cmd_val}:PATH{path_cmd_val}:FDOPpler?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'FdopplerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FdopplerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
