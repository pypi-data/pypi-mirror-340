#
# PartCAD, 2025
#
# Author: Roman Kuzmenko
# Created: 2025-01-03
#
# Licensed under Apache License, Version 2.0.
#

from .test import Test
from .. import logging as pc_logging
from ..part import Part
from ..part_config import PartConfiguration
from ..part_config_manufacturing import METHOD_ADDITIVE

from OCP.ShapeAnalysis import ShapeAnalysis_FreeBoundsProperties


class CamAdditiveSolidTest(Test):
    def __init__(self) -> None:
        super().__init__("cam-additive")

    async def test(self, tests_to_run: list[Test], ctx, shape, test_ctx: dict = {}) -> bool:
        if not isinstance(shape, Part):
            self.debug(shape, "Not applicable")
            return self.TEST_PASSED

        manufacturing_data = PartConfiguration.get_manufacturing_data(shape)
        if manufacturing_data.method != METHOD_ADDITIVE:
            self.debug(shape, "Not applicable")
            return self.TEST_PASSED

        # TODO(clairbee): Utilize the data provided in the config

        # TODO(clairbee): Improve and extend the below
        wrapped = await shape.get_wrapped(ctx)
        fbp = ShapeAnalysis_FreeBoundsProperties(wrapped)
        fbp.Perform()
        if fbp.NbFreeBounds() != 0:
            return self.failed(shape, "The shape is not solid")

        return self.passed(shape)
