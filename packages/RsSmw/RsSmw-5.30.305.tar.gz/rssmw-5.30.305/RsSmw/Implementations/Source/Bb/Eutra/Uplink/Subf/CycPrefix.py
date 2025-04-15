from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CycPrefixCls:
	"""CycPrefix commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cycPrefix", core, parent)

	def set(self, cyclic_prefix: enums.EuTraDuration, subframeNull=repcap.SubframeNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST0>]:CYCPrefix \n
		Snippet: driver.source.bb.eutra.uplink.subf.cycPrefix.set(cyclic_prefix = enums.EuTraDuration.EXTended, subframeNull = repcap.SubframeNull.Default) \n
		If BB:EUTR:UL:CPC USER, sets the cyclic prefix for the selected subframe. \n
			:param cyclic_prefix: NORMal| EXTended
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
		"""
		param = Conversions.enum_scalar_to_str(cyclic_prefix, enums.EuTraDuration)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{subframeNull_cmd_val}:CYCPrefix {param}')

	# noinspection PyTypeChecker
	def get(self, subframeNull=repcap.SubframeNull.Default) -> enums.EuTraDuration:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST0>]:CYCPrefix \n
		Snippet: value: enums.EuTraDuration = driver.source.bb.eutra.uplink.subf.cycPrefix.get(subframeNull = repcap.SubframeNull.Default) \n
		If BB:EUTR:UL:CPC USER, sets the cyclic prefix for the selected subframe. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:return: cyclic_prefix: NORMal| EXTended"""
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{subframeNull_cmd_val}:CYCPrefix?')
		return Conversions.str_to_scalar_enum(response, enums.EuTraDuration)
