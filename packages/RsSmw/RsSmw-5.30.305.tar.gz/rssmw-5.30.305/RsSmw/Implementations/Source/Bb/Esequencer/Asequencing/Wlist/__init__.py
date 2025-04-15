from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WlistCls:
	"""Wlist commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("wlist", core, parent)

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	# noinspection PyTypeChecker
	def get_dasr(self) -> enums.ExtSeqAdwRate:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:ASEQuencing:WLISt:DASR \n
		Snippet: value: enums.ExtSeqAdwRate = driver.source.bb.esequencer.asequencing.wlist.get_dasr() \n
		The desired ARB sample rate directly influences the minimum common clock rate all waveforms are resampled to. The higher
		the desired rate, the higher the common sample rate, in order to optimize the ADW sample rate. At the same time, the
		required memory will also increase. \n
			:return: sample_rate: SR37M5| SR75M| SR300M| SR2G4 SR37M5: sample rate = 37.5 MHz SR75M: sample rate = 75 MHz SR300M: sample rate = 300 MHz SR2G4: sample rate = 2.4 GHz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ESEQuencer:ASEQuencing:WLISt:DASR?')
		return Conversions.str_to_scalar_enum(response, enums.ExtSeqAdwRate)

	def set_dasr(self, sample_rate: enums.ExtSeqAdwRate) -> None:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:ASEQuencing:WLISt:DASR \n
		Snippet: driver.source.bb.esequencer.asequencing.wlist.set_dasr(sample_rate = enums.ExtSeqAdwRate.SR2G4) \n
		The desired ARB sample rate directly influences the minimum common clock rate all waveforms are resampled to. The higher
		the desired rate, the higher the common sample rate, in order to optimize the ADW sample rate. At the same time, the
		required memory will also increase. \n
			:param sample_rate: SR37M5| SR75M| SR300M| SR2G4 SR37M5: sample rate = 37.5 MHz SR75M: sample rate = 75 MHz SR300M: sample rate = 300 MHz SR2G4: sample rate = 2.4 GHz
		"""
		param = Conversions.enum_scalar_to_str(sample_rate, enums.ExtSeqAdwRate)
		self._core.io.write(f'SOURce<HwInstance>:BB:ESEQuencer:ASEQuencing:WLISt:DASR {param}')

	def clone(self) -> 'WlistCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = WlistCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
