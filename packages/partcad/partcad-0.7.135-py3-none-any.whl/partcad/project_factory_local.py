#
# OpenVMP, 2023
#
# Author: Roman Kuzmenko
# Created: 2023-08-19
#
# Licensed under Apache License, Version 2.0.
#

import os
from . import project_factory as pf
from . import telemetry


class LocalImportConfiguration:
    def __init__(self):
        self.import_config_path = self.config_obj.get("path").replace("/", os.path.sep)
        self.can_be_empty = self.config_obj.get("canBeEmpty", False)


@telemetry.instrument()
class ProjectFactoryLocal(pf.ProjectFactory, LocalImportConfiguration):
    def __init__(self, ctx, parent, config):
        pf.ProjectFactory.__init__(self, ctx, parent, config)
        LocalImportConfiguration.__init__(self)

        if not os.path.isabs(self.import_config_path) and self.config_dir != "":
            self.import_config_path = os.path.join(self.config_dir, self.import_config_path)

        self.path = self.import_config_path
        # TODO(clairbee): figure `import_config_url` out using `parent.import_config_url` and `self.path`

        if not self.can_be_empty and not os.path.exists(self.import_config_path):
            raise Exception("PartCAD config not found: %s" % self.import_config_path)

        # Complement the config object here if necessary
        self._create(config)

        # TODO(clairbee): consider installing a symlink in the parent's project

        self._save()
