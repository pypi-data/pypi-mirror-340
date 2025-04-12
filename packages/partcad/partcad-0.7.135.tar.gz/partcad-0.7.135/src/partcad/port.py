#
# OpenVMP, 2024
#
# Author: Roman Kuzmenko
# Created: 2024-04-20
#
# Licensed under Apache License, Version 2.0.
#

from .interface import Interface

from . import telemetry


@telemetry.instrument(exclude=["info"])
class WithPorts(Interface):
    interfaces: dict[str, dict[str, dict[str, str]]]

    def __init__(
        self,
        name: str,
        project,
        config: dict = {},
    ):
        super().__init__(name, project, config, config_section="implements")
        self.interfaces = None

    def get_interfaces(self):
        with self.lock:
            if self.interfaces is None:
                self.instantiate_interfaces()
            return self.interfaces

    def get_interface(self, interface_name: str):
        if interface_name.startswith("/") and not interface_name.startswith("//"):
            # Workaround the old syntax for absolute package paths
            interface_name = "/" + interface_name
        return self.get_interfaces()[interface_name]

    def instantiate_interfaces(self):
        self.interfaces = {}

        # Recursively merge the inherited interfaces
        @telemetry.start_as_current_span("WithPorts.instantiate_interfaces.merge_inherits")
        def merge_inherits(inherits, interface_state: str = "", top_level=False):
            if not top_level and len(inherits.keys()) == 1 and (len(list(inherits.values())[0].instances.keys()) == 1):
                compatible = True
            else:
                compatible = False

            for interface_name, inherit in inherits.items():
                interface = inherit.interface

                # Ignore abstract interfaces
                if interface.abstract:
                    continue

                if not ":" in interface_name:
                    interface_name = self.project.name + ":" + interface_name

                if not compatible and interface_name not in self.interfaces:
                    self.interfaces[interface_name] = {}

                for instance_name in inherit.instances.keys():
                    if instance_name != "" and interface_state != "":
                        instance_full_name = interface_state + "-" + instance_name
                    elif instance_name != "":
                        instance_full_name = instance_name
                    elif interface_state != "":
                        instance_full_name = interface_state
                    else:
                        instance_full_name = ""

                    if not compatible:
                        if instance_name not in self.interfaces[interface_name]:
                            self.interfaces[interface_name][instance_full_name] = {}

                        for port_name in interface.get_ports().keys():
                            if instance_full_name != "" and port_name != "":
                                port_full_name = instance_full_name + "-" + port_name
                            elif instance_full_name != "":
                                port_full_name = instance_full_name
                            elif port_name != "":
                                port_full_name = port_name
                            else:
                                port_full_name = ""

                            self.interfaces[interface_name][instance_full_name][port_name] = port_full_name

                    merge_inherits(interface.get_parents(), instance_full_name)

        merge_inherits(self.get_parents(), top_level=True)

    def info(self):
        return {
            "interfaces": dict(
                (
                    interface_name,
                    dict(
                        (
                            instance_name,
                            dict((port_name, port) for port_name, port in instance.items()),
                        )
                        for instance_name, instance in interface.items()
                    ),
                )
                for interface_name, interface in self.get_interfaces().items()
            ),
            "ports": dict(
                (
                    port_name,
                    {
                        "location": port.location,
                        "sketch": f"{port.sketch.project_name}:{port.sketch.name}",
                    },
                )
                for port_name, port in self.get_ports().items()
            ),
        }
