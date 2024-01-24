"""Execute a command."""

import sys
import anyio
import dagger


async def hello():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        greeting = (
            client.container()
            # pull container
            .from_("python:3.11-slim-buster")
            # get Python version
            .with_exec(["python3", "-VV"])
        )
        # execute
        banner = await greeting.stdout()
        print("Hello from Dagger running ", banner)

anyio.run(hello)
