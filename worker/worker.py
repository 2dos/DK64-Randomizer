"""Worker process for the randomizer service."""

from flask import Flask, request, jsonify, Blueprint
from redis import Redis
from rq import Queue, Worker
import threading
import json
import os
from waitress import serve
from opentelemetry import trace
import socket

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from randomizer.Settings import Settings
from randomizer.ProtoSerializer import serialize_settings_to_base64, deserialize_settings_from_base64, proto_to_settings, settings_to_proto
from randomizer.Enums.Types import ItemRandoSelector, KeySelector, ItemRandoFillerSelector
from randomizer.Lists.EnemyTypes import EnemySelector
from randomizer.Lists.HardMode import HardBossSelector, HardSelector
from randomizer.Lists.Item import CustomStartingMoveSelector, HHItemSelector
from randomizer.Lists.Logic import GlitchSelector, TrickSelector
from randomizer.Lists.Minigame import MinigameSelector
from randomizer.Lists.Multiselectors import FasterCheckSelector, QoLSelector, RemovedBarrierSelector, CBRandoSelector, RandomColorSelector, BossesSelector
from randomizer.Lists.Plandomizer import PlandomizerPanels, PlannableCustomLocations, PlannableItems, PlannableKroolPhases, PlannableMinigames, PlannableSpawns
from randomizer.Lists.Songs import ExcludedSongsSelector, MusicSelectionPanel, PlannableSongs, SongFilteringSelector
from randomizer.Lists.Warps import VanillaBananaportSelector
from randomizer.Lists.WrinklyHints import PointSpreadSelector
from version import version
import logging
import sys
from tasks import generate_seed
from opentelemetry_instrumentation_rq import RQInstrumentor
from randomizer.Lists.Exceptions import SettingsIncompatibleException, PlandoIncompatibleException
from opentelemetry.instrumentation.redis import RedisInstrumentor
from types import SimpleNamespace

BRANCH = os.environ.get("BRANCH", "LOCAL")
listen_branch = BRANCH
if BRANCH == "master":
    listen_branch = "stable"
else:
    listen_branch = "dev"
listen = [f"tasks_high_priority_{listen_branch}", f"tasks_low_priority_{listen_branch}"]  # High-priority first
redis_conn = Redis(host="redis", port=6379)
job_timeout = 300  # Timeout in seconds (5 minutes)
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
# Define a resource to identify your service
resource = Resource(
    attributes={
        "service.name": "worker-" + BRANCH,
        "service.version": str(version),
        "deployment.environment": BRANCH,
        "container.id": next((l.rsplit("/", 1)[-1] for l in open("/proc/self/cgroup") if "docker" in l), "") if os.path.exists("/proc/self/cgroup") else "",
        "container.name": socket.gethostname(),
    }
)


app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)
api = Blueprint("worker_api", __name__)


span = trace.get_current_span()
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer_provider = trace.get_tracer_provider()

# # Configure OTLP Exporter for sending traces to the collector
otlp_exporter = OTLPSpanExporter(endpoint="http://host.docker.internal:4318/v1/traces")

# # Add the BatchSpanProcessor to the TracerProvider
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
if __name__ == "__main__" and os.environ.get("BRANCH", "LOCAL") != "LOCAL":
    reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="http://host.docker.internal:4318/v1/metrics"))
    meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meterProvider)
    FlaskInstrumentor().instrument_app(app)
    RQInstrumentor().instrument()
    RedisInstrumentor().instrument()
    # create the providers
    logger_provider = LoggerProvider(resource=resource)
    # set the providers
    set_logger_provider(logger_provider)
    handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)
    logger.addHandler(handler)


@api.route("/get_selector_info", methods=["GET"])
def get_selector_info():
    """Get the selector data for the randomizer."""
    selector_data = {
        "minigames": MinigameSelector,
        "misc_changes": QoLSelector,
        "bosses": BossesSelector,
        "hard_mode": HardSelector,
        "hard_bosses": HardBossSelector,
        "enemies": EnemySelector,
        "excluded_songs": ExcludedSongsSelector,
        "random_colors": RandomColorSelector,
        "song_filters": SongFilteringSelector,
        "itemRando": ItemRandoSelector,
        "item_filler": ItemRandoFillerSelector,
        "keys": KeySelector,
        "glitches": GlitchSelector,
        "tricks": TrickSelector,
        "helm_hurry_items": HHItemSelector,
        "vanilla_warps": VanillaBananaportSelector,
        "plando_custom_locations": PlannableCustomLocations,
        "plando_items": PlannableItems,
        "plando_minigames": PlannableMinigames,
        "plando_panels": PlandomizerPanels,
        "plando_phases": PlannableKroolPhases,
        "plando_spawns": PlannableSpawns,
        "points_spread": PointSpreadSelector,
        "custom_starting_moves": CustomStartingMoveSelector,
        "select_song_panel": MusicSelectionPanel,
        "select_songs": PlannableSongs,
        "remove_barriers": RemovedBarrierSelector,
        "faster_checks": FasterCheckSelector,
        "cb_rando_levels": CBRandoSelector,
    }
    return json.dumps(selector_data, sort_keys=False)


@api.route("/convert_settings", methods=["POST"])
def convert_settings():
    """Convert settings between JSON and protobuf string formats."""
    data = request.get_json()
    if "settings" in data:
        try:
            # Attempt to interpret `settings` as JSON
            settings_json = json.loads(data["settings"])
            # If successful, convert to Settings object and serialize to proto
            settings_obj = Settings(settings_json)
            proto_string = settings_obj.to_proto_string()
            return jsonify({"settings_string": proto_string})
        except json.JSONDecodeError:
            # If `settings` is not JSON, deserialize from proto string
            proto = deserialize_settings_from_base64(data["settings"])
            settings_container = SimpleNamespace()
            proto_to_settings(proto, settings_container)
            return jsonify(settings_container.__dict__)
    else:
        return jsonify({"error": "Invalid data"}), 400


@api.route("/export_archipelago_yaml", methods=["POST"])
def export_archipelago_yaml():
    """Export settings to Archipelago YAML format."""
    try:
        from randomizer.ArchipelagoMapper import export_to_yaml

        data = request.get_json()

        # Get settings from request
        settings_data = data.get("settings", {})
        player_name = data.get("player_name", "Player")
        game_version = data.get("game_version", "0.6.6")

        # Settings should already be a dict from serialize_settings()
        # Only deserialize if it's actually a proto string (not JSON)
        if isinstance(settings_data, str):
            # Check if it looks like a proto string (not JSON)
            if not settings_data.strip().startswith("{"):
                proto = deserialize_settings_from_base64(settings_data)
                from google.protobuf.json_format import MessageToDict

                settings_data = MessageToDict(proto, preserving_proto_field_name=True)
            else:
                # It's a JSON string, parse it
                settings_data = json.loads(settings_data)

        # Log a sample of settings keys to help with debugging
        if settings_data:
            sample_keys = list(settings_data.keys())[:20]
            logging.info(f"Exporting YAML with {len(settings_data)} settings. Sample keys: {sample_keys}")

            # Debug list fields
            list_fields = ["remove_barriers_selected", "tricks_selected", "glitches_selected", "hard_mode_selected", "enemies_selected"]
            for field in list_fields:
                if field in settings_data:
                    value = settings_data[field]
                    logging.info(f"  {field}: {value} (type: {type(value).__name__}, len: {len(value) if isinstance(value, (list, tuple)) else 'N/A'})")

            # Debug item_rando_list_1 for dropsanity
            if "item_rando_list_1" in settings_data:
                item_list = settings_data["item_rando_list_1"]
                logging.info(f"  item_rando_list_1: {item_list} (len: {len(item_list) if isinstance(item_list, (list, tuple)) else 'N/A'})")

        # Generate YAML
        yaml_content = export_to_yaml(settings_data, player_name=player_name, game_version=game_version)

        return jsonify({"yaml": yaml_content, "success": True})
    except Exception as e:
        logging.error(f"Error exporting to YAML: {str(e)}", exc_info=True)
        return jsonify({"error": str(e), "success": False}), 500


def runWaitressWorker():
    """Run the worker using Waitress."""
    # Start the Flask server
    app.register_blueprint(api)
    serve(app, host="0.0.0.0", port=8000)


def runWorker(jobs):
    """Run the worker using RQ."""
    # Create queues for high- and low-priority tasks
    queues = [Queue(name, connection=redis_conn, default_timeout=job_timeout) for name in listen]

    # Use the custom PriorityAwareWorker to process tasks
    worker = Worker(queues, connection=redis_conn)

    def handle_exception(job, exc_type, exc_value, traceback):
        if isinstance(exc_value, (SettingsIncompatibleException, PlandoIncompatibleException)):
            # Do not retry the job
            job.meta["retry"] = False
            job.save_meta()
            return False  # Return False to indicate that the job should not be retried
        return True  # For other exceptions, retry the job

    worker.push_exc_handler(handle_exception)

    # Start processing tasks, prioritizing high-priority queue
    worker.work(max_jobs=jobs, with_scheduler=False)


if __name__ == "__main__":

    # Start the worker in a separate thread
    worker_thread = threading.Thread(target=runWaitressWorker)
    worker_thread.start()
    runWorker(None)
    # Close the worker thread instead of waiting for it to finish
    worker_thread.join(0)
