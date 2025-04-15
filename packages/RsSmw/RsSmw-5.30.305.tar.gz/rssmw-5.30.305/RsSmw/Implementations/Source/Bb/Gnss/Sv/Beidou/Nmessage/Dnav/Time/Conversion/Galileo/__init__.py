from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GalileoCls:
	"""Galileo commands group definition. 7 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("galileo", core, parent)

	@property
	def aone(self):
		"""aone commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_aone'):
			from .Aone import AoneCls
			self._aone = AoneCls(self._core, self._cmd_group)
		return self._aone

	@property
	def azero(self):
		"""azero commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_azero'):
			from .Azero import AzeroCls
			self._azero = AzeroCls(self._core, self._cmd_group)
		return self._azero

	@property
	def tot(self):
		"""tot commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tot'):
			from .Tot import TotCls
			self._tot = TotCls(self._core, self._cmd_group)
		return self._tot

	def get_wnot(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:BEIDou:NMESsage:DNAV:TIME:CONVersion:GALileo:WNOT \n
		Snippet: value: int = driver.source.bb.gnss.sv.beidou.nmessage.dnav.time.conversion.galileo.get_wnot() \n
		No command help available \n
			:return: wnot: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SV:BEIDou:NMESsage:DNAV:TIME:CONVersion:GALileo:WNOT?')
		return Conversions.str_to_int(response)

	def set_wnot(self, wnot: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:BEIDou:NMESsage:DNAV:TIME:CONVersion:GALileo:WNOT \n
		Snippet: driver.source.bb.gnss.sv.beidou.nmessage.dnav.time.conversion.galileo.set_wnot(wnot = 1) \n
		No command help available \n
			:param wnot: No help available
		"""
		param = Conversions.decimal_value_to_str(wnot)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:BEIDou:NMESsage:DNAV:TIME:CONVersion:GALileo:WNOT {param}')

	def clone(self) -> 'GalileoCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GalileoCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
