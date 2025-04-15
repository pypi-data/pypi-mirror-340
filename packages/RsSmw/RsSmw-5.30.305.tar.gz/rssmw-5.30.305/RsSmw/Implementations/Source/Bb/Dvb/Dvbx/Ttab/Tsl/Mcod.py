from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McodCls:
	"""Mcod commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mcod", core, parent)

	def set(self, mod_cod: enums.DvbS2XmodCodUniqueTsl, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:TTAB:TSL<CH0>:MCOD \n
		Snippet: driver.source.bb.dvb.dvbx.ttab.tsl.mcod.set(mod_cod = enums.DvbS2XmodCodUniqueTsl.MCU1, channelNull = repcap.ChannelNull.Default) \n
		Selects a predefined modulation and coding scheme. Time-slicing supports the MODCOD unique categories except the super
		frame spreads. \n
			:param mod_cod: MCU1| MCU2| MCU3| MCU4| MCU5| MCU6| MCU7| MCU8| MCU9| MCU10| MCU11| MCU12| MCU13| MCU14| MCU15| MCU16| MCU17| MCU18| MCU19| MCU20| MCU21| MCU22| MCU23| MCU24| MCU25| MCU26| MCU27| MCU28| MCU29| MCU30| MCU31| MCU32| MCU33| MCU34| MCU35| MCU36| MCU37| MCU38| MCU39| MCU40| MCU41| MCU42| MCU43| MCU44| MCU45| MCU46| MCU47| MCU48| MCU49| MCU50| MCU51| MCU52| MCU53| MCU54| MCU55| MCU56| MCU57| MCU58| MCU59| MCU60| MCU61| MCU62| MCU63| MCU64| MCU65| MCU66| MCU67| MCU68| MCU69| MCU70| MCU71| MCU72| MCU73| MCU74| MCU75| MCU76| MCU77| MCU78| MCU79| MCU80| MCU81| MCU82| MCU83| MCU84| MCU85| MCU86| MCU87| MCU88| MCU89| MCU90| MCU91| MCU92| MCU93| MCU94| MCU95| MCU96| MCU97| MCU98| MCU99| MCU100| MCU101| MCU102| MCU103| MCU104| MCU105| MCU106| MCU107| MCU108| MCU109| MCU110| MCU111| MCU112| MCU113| MCU114| MCU115| MCU116
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
		"""
		param = Conversions.enum_scalar_to_str(mod_cod, enums.DvbS2XmodCodUniqueTsl)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBX:TTAB:TSL{channelNull_cmd_val}:MCOD {param}')

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.DvbS2XmodCodUniqueTsl:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:TTAB:TSL<CH0>:MCOD \n
		Snippet: value: enums.DvbS2XmodCodUniqueTsl = driver.source.bb.dvb.dvbx.ttab.tsl.mcod.get(channelNull = repcap.ChannelNull.Default) \n
		Selects a predefined modulation and coding scheme. Time-slicing supports the MODCOD unique categories except the super
		frame spreads. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tsl')
			:return: mod_cod: MCU1| MCU2| MCU3| MCU4| MCU5| MCU6| MCU7| MCU8| MCU9| MCU10| MCU11| MCU12| MCU13| MCU14| MCU15| MCU16| MCU17| MCU18| MCU19| MCU20| MCU21| MCU22| MCU23| MCU24| MCU25| MCU26| MCU27| MCU28| MCU29| MCU30| MCU31| MCU32| MCU33| MCU34| MCU35| MCU36| MCU37| MCU38| MCU39| MCU40| MCU41| MCU42| MCU43| MCU44| MCU45| MCU46| MCU47| MCU48| MCU49| MCU50| MCU51| MCU52| MCU53| MCU54| MCU55| MCU56| MCU57| MCU58| MCU59| MCU60| MCU61| MCU62| MCU63| MCU64| MCU65| MCU66| MCU67| MCU68| MCU69| MCU70| MCU71| MCU72| MCU73| MCU74| MCU75| MCU76| MCU77| MCU78| MCU79| MCU80| MCU81| MCU82| MCU83| MCU84| MCU85| MCU86| MCU87| MCU88| MCU89| MCU90| MCU91| MCU92| MCU93| MCU94| MCU95| MCU96| MCU97| MCU98| MCU99| MCU100| MCU101| MCU102| MCU103| MCU104| MCU105| MCU106| MCU107| MCU108| MCU109| MCU110| MCU111| MCU112| MCU113| MCU114| MCU115| MCU116"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DVB:DVBX:TTAB:TSL{channelNull_cmd_val}:MCOD?')
		return Conversions.str_to_scalar_enum(response, enums.DvbS2XmodCodUniqueTsl)
