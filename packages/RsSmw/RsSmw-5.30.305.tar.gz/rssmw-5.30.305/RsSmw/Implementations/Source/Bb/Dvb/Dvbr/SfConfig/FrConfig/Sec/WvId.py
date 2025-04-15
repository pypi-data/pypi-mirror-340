from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WvIdCls:
	"""WvId commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("wvId", core, parent)

	def set(self, wv_id: enums.DvbRcs2WaveformId, sfCfgIxNull=repcap.SfCfgIxNull.Default, frCfgIxNull=repcap.FrCfgIxNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBR:SFConfig<CH0>:FRConfig<ST0>:SEC<DI0>:WVID \n
		Snippet: driver.source.bb.dvb.dvbr.sfConfig.frConfig.sec.wvId.set(wv_id = enums.DvbRcs2WaveformId.LM1, sfCfgIxNull = repcap.SfCfgIxNull.Default, frCfgIxNull = repcap.FrCfgIxNull.Default, indexNull = repcap.IndexNull.Default) \n
		Select a reference waveform, defined for the transmission format class. \n
			:param wv_id: LM1| LM2| LM3| LM4| LM5| LM6| LM7| LM8| LM9| LM10| LM11| LM12| LM13| LM14| LM15| LM16| LM17| LM18| LM19| LM20| LM21| LM22| LM32| LM33| LM34| LM35| LM36| LM37| LM38| LM39| LM40| LM41| LM42| LM43| LM44| LM45| LM46| LM47| LM48| LM49| SSLM1| SSLM2| SSLM3| SSLM4| SSLM5| SSLM6| SSLM7| SSLM8| SSLM9| SSLM10| SSLM11| SSLM12| SSLM13| SSLM14| SSLM15| SSLM16| SSLM17| SSLM18| SSLM19 LMID or SSLMID deoending on the selected Tx format class [:SOURcehw]:BB:DVB:DVBR:SFConfigch0:FRConfigst0:TXFormat. LMID ID is the waveform identifier according to specification in Annex A of LM = linear modulation (the default Tx format class) SSLMID ID is the waveform identifier according to specification in Annex A of SSLM = SS linear modulation
			:param sfCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'SfConfig')
			:param frCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'FrConfig')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sec')
		"""
		param = Conversions.enum_scalar_to_str(wv_id, enums.DvbRcs2WaveformId)
		sfCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(sfCfgIxNull, repcap.SfCfgIxNull)
		frCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(frCfgIxNull, repcap.FrCfgIxNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBR:SFConfig{sfCfgIxNull_cmd_val}:FRConfig{frCfgIxNull_cmd_val}:SEC{indexNull_cmd_val}:WVID {param}')

	# noinspection PyTypeChecker
	def get(self, sfCfgIxNull=repcap.SfCfgIxNull.Default, frCfgIxNull=repcap.FrCfgIxNull.Default, indexNull=repcap.IndexNull.Default) -> enums.DvbRcs2WaveformId:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBR:SFConfig<CH0>:FRConfig<ST0>:SEC<DI0>:WVID \n
		Snippet: value: enums.DvbRcs2WaveformId = driver.source.bb.dvb.dvbr.sfConfig.frConfig.sec.wvId.get(sfCfgIxNull = repcap.SfCfgIxNull.Default, frCfgIxNull = repcap.FrCfgIxNull.Default, indexNull = repcap.IndexNull.Default) \n
		Select a reference waveform, defined for the transmission format class. \n
			:param sfCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'SfConfig')
			:param frCfgIxNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'FrConfig')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sec')
			:return: wv_id: LM1| LM2| LM3| LM4| LM5| LM6| LM7| LM8| LM9| LM10| LM11| LM12| LM13| LM14| LM15| LM16| LM17| LM18| LM19| LM20| LM21| LM22| LM32| LM33| LM34| LM35| LM36| LM37| LM38| LM39| LM40| LM41| LM42| LM43| LM44| LM45| LM46| LM47| LM48| LM49| SSLM1| SSLM2| SSLM3| SSLM4| SSLM5| SSLM6| SSLM7| SSLM8| SSLM9| SSLM10| SSLM11| SSLM12| SSLM13| SSLM14| SSLM15| SSLM16| SSLM17| SSLM18| SSLM19 LMID or SSLMID deoending on the selected Tx format class [:SOURcehw]:BB:DVB:DVBR:SFConfigch0:FRConfigst0:TXFormat. LMID ID is the waveform identifier according to specification in Annex A of LM = linear modulation (the default Tx format class) SSLMID ID is the waveform identifier according to specification in Annex A of SSLM = SS linear modulation"""
		sfCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(sfCfgIxNull, repcap.SfCfgIxNull)
		frCfgIxNull_cmd_val = self._cmd_group.get_repcap_cmd_value(frCfgIxNull, repcap.FrCfgIxNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DVB:DVBR:SFConfig{sfCfgIxNull_cmd_val}:FRConfig{frCfgIxNull_cmd_val}:SEC{indexNull_cmd_val}:WVID?')
		return Conversions.str_to_scalar_enum(response, enums.DvbRcs2WaveformId)
