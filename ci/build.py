import sys
import anyio
import dagger
from ci import settings

"""
create the build container.
"""
async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        ci_environment = settings.ci_environment,
        compatibility = settings.compatibility,
        gherkin = settings.gherkin,
        messages = settings.messages,
        out = await (
            client.container()
            .from_("python:3.11-slim")
            .with_directory("/host", client.host().directory(
                ci_environment,
                compatibility,
                gherkin,
                messages,
                )
            )
            .with_exec(["ls", "-al", "/host"])
            .stdout()
        )

    print(out)

anyio.run(main)
