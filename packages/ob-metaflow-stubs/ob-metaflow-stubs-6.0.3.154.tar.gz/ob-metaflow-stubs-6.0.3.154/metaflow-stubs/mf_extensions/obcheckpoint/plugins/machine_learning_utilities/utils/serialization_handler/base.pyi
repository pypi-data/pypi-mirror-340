######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.7.2+obcheckpoint(0.1.9);ob(v1)                                                    #
# Generated on 2025-04-10T22:13:14.985239                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing


class SerializationHandler(object, metaclass=type):
    def serialze(self, *args, **kwargs) -> typing.Union[str, bytes]:
        ...
    def deserialize(self, *args, **kwargs) -> typing.Any:
        ...
    ...

