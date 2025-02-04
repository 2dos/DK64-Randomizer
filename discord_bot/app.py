"""Discord bot that generates seeds for DK64 Randomizer."""

import discord
from discord import app_commands
import requests
import asyncio
import logging
import socket
import os
from opentelemetry import trace

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import metrics

from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace.export import BatchSpanProcessor

logging.basicConfig(level=logging.INFO)

# Define a resource to identify your service
resource = Resource(
    attributes={
        "service.name": "discord_bot",
        "service.version": "1.0",
        "deployment.environment": os.environ.get("BRANCH", "LOCAL"),
        "container.id": next((l.rsplit("/", 1)[-1] for l in open("/proc/self/cgroup") if "docker" in l), "") if os.path.exists("/proc/self/cgroup") else "",
        "container.name": socket.gethostname(),
    }
)
logger = logging.getLogger(__name__)

# check the args we started the script with
if __name__ == "__main__" or os.environ.get("BRANCH", "LOCAL") != "LOCAL":
    # create the providers
    logger_provider = LoggerProvider(resource=resource)
    # set the providers
    set_logger_provider(logger_provider)
    # Set up the TracerProvider and Span Exporter
    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer_provider = trace.get_tracer_provider()

    # # Configure OTLP Exporter for sending traces to the collector
    otlp_exporter = OTLPSpanExporter(endpoint="http://host.docker.internal:4318/v1/traces")
    # # Add the BatchSpanProcessor to the TracerProvider
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="http://host.docker.internal:4318/v1/metrics"))
    meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meterProvider)
    RequestsInstrumentor().instrument()
    handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)
    logger.addHandler(handler)
intents = discord.Intents.default()
intents.message_content = True

discord_token = os.environ.get("DISCORD_APP_TOKEN")
headers = {"x-api-key": os.environ.get("DK64_API_KEY")}
# Call the api api.dk64rando.com/api/get_presets
response = requests.get("https://api.dk64rando.com/api/get_presets?branch=dev", headers=headers)
dev_presets = response.json()
response = requests.get("https://api.dk64rando.com/api/get_presets", headers=headers)
stable_presets = response.json()

# Get all the names of the presets
dev_preset_names = [preset["name"] for preset in dev_presets]
stable_preset_names = [preset["name"] for preset in stable_presets]
# Deduplicate the names between both dev and stable
preset_names = list({preset_name.lower(): preset_name for preset_name in dev_preset_names + stable_preset_names}.values())
preset_choices = [app_commands.Choice(name=preset_name, value=preset_name) for preset_name in preset_names]
# Add the custom preset choice
preset_choices.append(app_commands.Choice(name="Custom", value="custom"))
version_choices = [app_commands.Choice(name="Dev", value="dev")]
# version_choices.append(app_commands.Choice(name="Stable", value="stable"))


client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client=client)
client.tree = tree


@client.event
async def on_ready():
    """Event when the bot is ready."""
    logger.info(f"We have logged in as {client.user}")
    client.activity = discord.Game(name="DK64 Randomizer")
    await client.change_presence(activity=client.activity)
    for guild in client.guilds:
        logger.info(f"Syncing commands to guild {guild.name}")
        guild_obj = discord.Object(id=guild.id)
        tree.copy_global_to(guild=guild_obj)
        await tree.sync(guild=guild_obj)
    logger.info("Commands synced to all guilds!")


@client.event
async def on_message(message):
    """Event when a message is sent in a channel."""
    if message.author == client.user:
        return
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith((".z64", ".n64", ".v64")):
                await message.delete()
                await message.channel.send("Files with the extensions .z64, .n64, and .v64 are not allowed to be shared. Sharing ROMs is illegal.")


# When we're added to a guild, register the commands
@client.event
async def on_guild_join(guild: discord.Guild):
    """Event when the bot joins a guild."""
    logger.info(f"Joined guild {guild.name} with {guild.member_count} members!")
    logger.info("Syncing commands to guild")
    guild_obj = discord.Object(id=guild.id)
    tree.copy_global_to(guild=guild_obj)
    await tree.sync(guild=guild_obj)
    logger.info("Commands synced to guild!")


@client.tree.command(name="generate")
@app_commands.describe(version="Generate a seed for Stable or Dev.", preset="Choose a preset or provide custom settings string.", settings="Custom settings string for the seed generation.")
@app_commands.choices(version=version_choices, preset=preset_choices)
async def generate(interaction: discord.Interaction, version: discord.app_commands.Choice[str], preset: discord.app_commands.Choice[str], settings: str = None):
    """Generate a seed for the user."""
    if version.value not in ["stable", "dev"]:
        await interaction.response.send_message("Invalid version. Please choose 'stable' or 'dev'.", ephemeral=True)
        return

    if preset.value not in preset_names and preset.value != "custom":
        await interaction.response.send_message("Invalid preset. Please choose a preset from the list.", ephemeral=True)
        return

    if preset.value == "custom" and not settings:
        await interaction.response.send_message("Please provide a settings string for custom preset.", ephemeral=True)
        return
    restart_on_complete = False
    if preset.value != "custom":
        # Re call the api to get the presets so we can check if the presets have changed
        response = requests.get("https://api.dk64rando.com/api/get_presets?branch=dev", headers=headers)
        dev_presets_data = response.json()
        response = requests.get("https://api.dk64rando.com/api/get_presets", headers=headers)
        stable_presets_data = response.json()
        dev_preset_names = [preset["name"] for preset in dev_presets]
        stable_preset_names = [preset["name"] for preset in stable_presets]
        preset_names_updated = list({preset_name.lower(): preset_name for preset_name in dev_preset_names + stable_preset_names}.values())
        if preset_names_updated != preset_names:
            restart_on_complete = True

        logger.info(f"generate {version.value} with {preset.value}")
        settings_string = ""
        if version.value == "dev":
            for preset_obj in dev_presets_data:
                if preset_obj["name"] == preset.value:
                    settings_string = preset_obj["settings_string"]
                    break
        else:
            for preset_obj in stable_presets_data:
                if preset_obj["name"] == preset.value:
                    settings_string = preset_obj["settings_string"]
                    break
        settings_dict = convert_settings(settings_string, version.value)
    else:
        logger.info(f"generate {version.value} with custom settings: {settings}")
        settings_dict = convert_settings(settings, version.value)

    task_data = submit_task(version.value, settings_dict)
    task_id = task_data["task_id"]
    status = task_data["status"]
    await interaction.response.send_message(f"Generating {version.value} version with {preset.value if preset.value != 'custom' else 'custom settings'}! Status: {status}", ephemeral=True)

    # Start a background task to check task status
    async def monitor_task_status(task_id: str, branch: str, restart_on_complete: bool = False):
        """Monitor the status of the task."""
        task_started = False
        while True:
            task_status = check_task_status(task_id)
            try:
                if task_status["status"] == "started":
                    if not task_started:
                        task_started = True
                        await interaction.followup.send("Seed Generation Started! Please wait for completion.", ephemeral=True)
                if task_status["status"] == "finished":
                    result = task_status.get("result", "No result available")
                    if branch == "dev":
                        url = "https://dev.dk64randomizer.com/randomizer?seed_id=" + str(result.get("seed_number"))
                    else:
                        url = "https://dk64randomizer.com/randomizer?seed_id=" + str(result.get("seed_number"))
                    requestor = interaction.user.mention
                    await interaction.followup.send(f"Seed Generated by {requestor}! {url}")
                    if restart_on_complete:
                        os._exit(1)
                    break
                elif task_status["status"] == "failed":
                    await interaction.followup.send("Task failed! Please try again later.", ephemeral=True)
                    if restart_on_complete:
                        os._exit(1)
                    break
            except Exception as e:
                logger.info(e)
                await interaction.followup.send("An error occurred while checking task status.", ephemeral=True)
                if restart_on_complete:
                    os._exit(1)
                break
            await asyncio.sleep(5)  # Check every 5 seconds

    client.loop.create_task(monitor_task_status(task_id, version.value, restart_on_complete))


def convert_settings(settings_str: str, branch: str):
    """Convert settings between JSON and encrypted string formats."""
    url = "https://api.dk64rando.com/api/convert_settings"
    if branch == "dev":
        url += "?branch=dev"
    settings = requests.post(url, headers=headers, json={"settings": settings_str})
    return settings.json()


def submit_task(version: str, settings: dict):
    """Submit a task to generate a seed."""
    url = "https://api.dk64rando.com/api/submit-task"
    if version == "dev":
        url += "?branch=dev"
    task = requests.post(url, headers=headers, json={"settings_data": settings})
    return task.json()


def check_task_status(task_id: str):
    """Check the status of a task."""
    url = f"https://api.dk64rando.com/api/task-status/{task_id}"
    status = requests.get(url, headers=headers)
    return status.json()


client.run(discord_token)
