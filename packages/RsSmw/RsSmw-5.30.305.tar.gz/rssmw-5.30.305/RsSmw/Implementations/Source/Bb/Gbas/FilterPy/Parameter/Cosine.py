from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CosineCls:
	"""Cosine commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cosine", core, parent)

	def get_cofs(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GBAS:FILTer:PARameter:COSine:COFS \n
		Snippet: value: float = driver.source.bb.gbas.filterPy.parameter.cosine.get_cofs() \n
		Sets the corresponding filter parameter.
			Table Header: Filter Type / Parameter / Parameter Name / min / max / increment / default \n
			- APCO25 / roll-off factor / <Apco25> / 0.05 / 0.99 / 0.01 / 0.2
			- COSine / roll-off factor / <Cosine> / 0.05 / 1.00 / 0.01 / 0.35
			- COSine / bandwidth to symbol rate ratio / <CoFs> / 2 / 2 / 0.01 / 1.00
			- GAUSs / roll-off factor / <Gauss> / 0.15 / 2.5 / 0.01 / 0.3
			- LPASs / cut off frequency / <LPass> / 0.05 / 2 / 0.01 / 0.5
			- LPASSEVM / cut off frequency / <LPassEvm> / 0.05 / 2 / 0.01 / 0.5
			- PGAuss / roll-off factor / <PGauss> / 0.15 / 2.5 / 0.01 / 0.3
			- RCOSine / roll-off factor / <RCosine> / 0.05 / 1.00 / 0.01 / 0.35
			- SPHase / B x T / <SPhase> / 0.15 / 2.5 / 0.01 / 2 \n
			:return: cofs: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GBAS:FILTer:PARameter:COSine:COFS?')
		return Conversions.str_to_float(response)

	def set_cofs(self, cofs: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:FILTer:PARameter:COSine:COFS \n
		Snippet: driver.source.bb.gbas.filterPy.parameter.cosine.set_cofs(cofs = 1.0) \n
		Sets the corresponding filter parameter.
			Table Header: Filter Type / Parameter / Parameter Name / min / max / increment / default \n
			- APCO25 / roll-off factor / <Apco25> / 0.05 / 0.99 / 0.01 / 0.2
			- COSine / roll-off factor / <Cosine> / 0.05 / 1.00 / 0.01 / 0.35
			- COSine / bandwidth to symbol rate ratio / <CoFs> / 2 / 2 / 0.01 / 1.00
			- GAUSs / roll-off factor / <Gauss> / 0.15 / 2.5 / 0.01 / 0.3
			- LPASs / cut off frequency / <LPass> / 0.05 / 2 / 0.01 / 0.5
			- LPASSEVM / cut off frequency / <LPassEvm> / 0.05 / 2 / 0.01 / 0.5
			- PGAuss / roll-off factor / <PGauss> / 0.15 / 2.5 / 0.01 / 0.3
			- RCOSine / roll-off factor / <RCosine> / 0.05 / 1.00 / 0.01 / 0.35
			- SPHase / B x T / <SPhase> / 0.15 / 2.5 / 0.01 / 2 \n
			:param cofs: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(cofs)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:FILTer:PARameter:COSine:COFS {param}')

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GBAS:FILTer:PARameter:COSine \n
		Snippet: value: float = driver.source.bb.gbas.filterPy.parameter.cosine.get_value() \n
		Sets the corresponding filter parameter.
			Table Header: Filter Type / Parameter / Parameter Name / min / max / increment / default \n
			- APCO25 / roll-off factor / <Apco25> / 0.05 / 0.99 / 0.01 / 0.2
			- COSine / roll-off factor / <Cosine> / 0.05 / 1.00 / 0.01 / 0.35
			- COSine / bandwidth to symbol rate ratio / <CoFs> / 2 / 2 / 0.01 / 1.00
			- GAUSs / roll-off factor / <Gauss> / 0.15 / 2.5 / 0.01 / 0.3
			- LPASs / cut off frequency / <LPass> / 0.05 / 2 / 0.01 / 0.5
			- LPASSEVM / cut off frequency / <LPassEvm> / 0.05 / 2 / 0.01 / 0.5
			- PGAuss / roll-off factor / <PGauss> / 0.15 / 2.5 / 0.01 / 0.3
			- RCOSine / roll-off factor / <RCosine> / 0.05 / 1.00 / 0.01 / 0.35
			- SPHase / B x T / <SPhase> / 0.15 / 2.5 / 0.01 / 2 \n
			:return: cosine: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GBAS:FILTer:PARameter:COSine?')
		return Conversions.str_to_float(response)

	def set_value(self, cosine: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:FILTer:PARameter:COSine \n
		Snippet: driver.source.bb.gbas.filterPy.parameter.cosine.set_value(cosine = 1.0) \n
		Sets the corresponding filter parameter.
			Table Header: Filter Type / Parameter / Parameter Name / min / max / increment / default \n
			- APCO25 / roll-off factor / <Apco25> / 0.05 / 0.99 / 0.01 / 0.2
			- COSine / roll-off factor / <Cosine> / 0.05 / 1.00 / 0.01 / 0.35
			- COSine / bandwidth to symbol rate ratio / <CoFs> / 2 / 2 / 0.01 / 1.00
			- GAUSs / roll-off factor / <Gauss> / 0.15 / 2.5 / 0.01 / 0.3
			- LPASs / cut off frequency / <LPass> / 0.05 / 2 / 0.01 / 0.5
			- LPASSEVM / cut off frequency / <LPassEvm> / 0.05 / 2 / 0.01 / 0.5
			- PGAuss / roll-off factor / <PGauss> / 0.15 / 2.5 / 0.01 / 0.3
			- RCOSine / roll-off factor / <RCosine> / 0.05 / 1.00 / 0.01 / 0.35
			- SPHase / B x T / <SPhase> / 0.15 / 2.5 / 0.01 / 2 \n
			:param cosine: float Range: 0.15 to 2.5
		"""
		param = Conversions.decimal_value_to_str(cosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:FILTer:PARameter:COSine {param}')
