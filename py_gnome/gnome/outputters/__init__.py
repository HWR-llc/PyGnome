
from outputter import Outputter, BaseOutputterSchema
from netcdf import NetCDFOutput, NetCDFOutputSchema
from renderer import Renderer, RendererSchema
from rasterer import Rasterer, RastererSchema
from weathering import WeatheringOutput
from binary import BinaryOutput, BinaryOutputSchema
from geo_json import (TrajectoryGeoJsonOutput,
                      IceGeoJsonOutput)
from json import (IceJsonOutput,
                  CurrentJsonOutput,
                  SpillJsonOutput)

from kmz import KMZOutput
from image import IceImageOutput
from shape import ShapeOutput
from oil_budget import OilBudgetOutput

# NOTE: no need for __all__ if you want export everything!
outputters = [Outputter,
              NetCDFOutput,
              Renderer,
              Rasterer,
              WeatheringOutput,
              BinaryOutput,
              TrajectoryGeoJsonOutput,
              IceGeoJsonOutput,
              IceJsonOutput,
              CurrentJsonOutput,
              SpillJsonOutput,
              KMZOutput,
              IceImageOutput,
              ShapeOutput]

schemas = set()
for cls in outputters:
    if hasattr(cls, '_schema'):
        schemas.add(cls._schema)
schemas = list(schemas)