from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PlenCls:
	"""Plen commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("plen", core, parent)

	def set(self, plen: int, sfCfgIxNull=repcap.SfCfgIxNull.Default, frCfgIxNull=repcap.FrCfgIxNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBR:SFConfig<CH0>:FRConfig<ST0>:SEC<DI0>:PLEN \n
		Snippet: driver.source.bb.dvb.dvbr.sfConfig.frConfig.sec.plen.set(plen = 1, sfCfgIxNull = repcap.SfCfgIxNull.Default, frCfgIxNull = repcap.FrCfgIxNull.Default, indexNull = repcap.IndexNull.Default) \n
		Queries the payload length. \n
			:param plen: integer Range: 1 to 1000
			:param sfCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'SfConfig')
			:param frCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'FrConfig')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sec')
		"""
		param = Conversions.decimal_value_to_str(plen)
		sfCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(sfCfgIxNull, repcap.SfCfgIxNull)
		frCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(frCfgIxNull, repcap.FrCfgIxNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBR:SFConfig{sfCfgIxNull_cmd_val}:FRConfig{frCfgIxNull_cmd_val}:SEC{indexNull_cmd_val}:PLEN {param}')

	def get(self, sfCfgIxNull=repcap.SfCfgIxNull.Default, frCfgIxNull=repcap.FrCfgIxNull.Default, indexNull=repcap.IndexNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBR:SFConfig<CH0>:FRConfig<ST0>:SEC<DI0>:PLEN \n
		Snippet: value: int = driver.source.bb.dvb.dvbr.sfConfig.frConfig.sec.plen.get(sfCfgIxNull = repcap.SfCfgIxNull.Default, frCfgIxNull = repcap.FrCfgIxNull.Default, indexNull = repcap.IndexNull.Default) \n
		Queries the payload length. \n
			:param sfCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'SfConfig')
			:param frCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'FrConfig')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sec')
			:return: plen: integer Range: 1 to 1000"""
		sfCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(sfCfgIxNull, repcap.SfCfgIxNull)
		frCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(frCfgIxNull, repcap.FrCfgIxNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DVB:DVBR:SFConfig{sfCfgIxNull_cmd_val}:FRConfig{frCfgIxNull_cmd_val}:SEC{indexNull_cmd_val}:PLEN?')
		return Conversions.str_to_int(response)
