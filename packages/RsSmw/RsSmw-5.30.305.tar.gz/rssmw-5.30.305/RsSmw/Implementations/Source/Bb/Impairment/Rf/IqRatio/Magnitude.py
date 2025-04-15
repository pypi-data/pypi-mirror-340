from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MagnitudeCls:
	"""Magnitude commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("magnitude", core, parent)

	def set(self, ipartq_ratio: float, path=repcap.Path.Default) -> None:
		"""SCPI: [SOURce]:BB:IMPairment:RF<CH>:IQRatio:[MAGNitude] \n
		Snippet: driver.source.bb.impairment.rf.iqRatio.magnitude.set(ipartq_ratio = 1.0, path = repcap.Path.Default) \n
		Sets the ratio of I modulation to Q modulation (amplification imbalance) of the corresponding digital channel.
		Value range
			Table Header: Impairments / Min /dB / Max /dB / Increment \n
			- Digital / 4 / 4 / 0.0001
			- Analog / 1 / 1 / 0.0001 \n
			:param ipartq_ratio: float The setting value can be either in dB or %. An input in percent is rounded to the closest valid value in dB. Range: -4 to 4, Unit: dB | PCT (setting command) / dB (result value)
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
		"""
		param = Conversions.decimal_value_to_str(ipartq_ratio)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SOURce:BB:IMPairment:RF{path_cmd_val}:IQRatio:MAGNitude {param}')

	def get(self, path=repcap.Path.Default) -> float:
		"""SCPI: [SOURce]:BB:IMPairment:RF<CH>:IQRatio:[MAGNitude] \n
		Snippet: value: float = driver.source.bb.impairment.rf.iqRatio.magnitude.get(path = repcap.Path.Default) \n
		Sets the ratio of I modulation to Q modulation (amplification imbalance) of the corresponding digital channel.
		Value range
			Table Header: Impairments / Min /dB / Max /dB / Increment \n
			- Digital / 4 / 4 / 0.0001
			- Analog / 1 / 1 / 0.0001 \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: ipartq_ratio: No help available"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:RF{path_cmd_val}:IQRatio:MAGNitude?')
		return Conversions.str_to_float(response)
