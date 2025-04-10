import sys
from collections.abc import Generator
from json import loads

from gevent.os import tp_read

from dify_plugin.core.entities.plugin.io import (
    PluginInStream,
    PluginInStreamEvent,
)
from dify_plugin.core.server.__base.request_reader import RequestReader
from dify_plugin.core.server.stdio.response_writer import StdioResponseWriter


class StdioRequestReader(RequestReader):
    def _read_stream(self) -> Generator[PluginInStream, None, None]:
        buffer = b""
        while True:
            # read data from stdin through tp_read
            data = tp_read(sys.stdin.fileno(), 512)

            if not data:
                continue

            buffer += data

            # process line by line and keep the last line if it is not complete
            lines = buffer.split(b"\n")
            if len(lines) == 0:
                continue

            buffer = lines[-1]

            lines = lines[:-1]
            for line in lines:
                try:
                    data = loads(line)
                    yield PluginInStream(
                        session_id=data["session_id"],
                        event=PluginInStreamEvent.value_of(data["event"]),
                        data=data["data"],
                        reader=self,
                        writer=StdioResponseWriter(),
                    )
                except Exception as e:
                    StdioResponseWriter().error(data={"error": str(e)})
