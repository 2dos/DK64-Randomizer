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
from randomizer.SettingStrings import decrypt_settings_string_enum, encrypt_settings_string_enum
from randomizer.Enums.Types import ItemRandoSelector, KeySelector
from randomizer.Lists.EnemyTypes import EnemySelector
from randomizer.Lists.HardMode import HardBossSelector, HardSelector
from randomizer.Lists.Item import CustomStartingMoveSelector, HHItemSelector
from randomizer.Lists.Logic import GlitchSelector
from randomizer.Lists.Minigame import MinigameSelector
from randomizer.Lists.Multiselectors import FasterCheckSelector, QoLSelector, RemovedBarrierSelector, CBRandoSelector
from randomizer.Lists.Plandomizer import PlandomizerPanels, PlannableCustomLocations, PlannableItems, PlannableKroolPhases, PlannableMinigames, PlannableSpawns, PlannableSwitches
from randomizer.Lists.Songs import ExcludedSongsSelector, MusicSelectionPanel, PlannableSongs, SongFilteringSelector
from randomizer.Lists.Warps import VanillaBananaportSelector
from randomizer.Lists.WrinklyHints import PointSpreadSelector
from version import version
import logging
from tasks import generate_seed
from opentelemetry_instrumentation_rq import RQInstrumentor
from randomizer.Lists.Exceptions import SettingsIncompatibleException, PlandoIncompatibleException
from opentelemetry.instrumentation.redis import RedisInstrumentor


listen = ["tasks_high_priority", "tasks_low_priority"]  # High-priority first
redis_conn = Redis(host="redis", port=6379)
job_timeout = 300  # Timeout in seconds (5 minutes)
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
BRANCH = os.environ.get("BRANCH", "LOCAL")
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

if __name__ == "__main__" or os.environ.get("BRANCH", "LOCAL") != "LOCAL":
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


class PriorityAwareWorker(Worker):
    """Worker that processes high-priority tasks first."""

    def execute_job(self, job, queue):
        """Process a job from the queue."""
        # Log which queue the job came from and its metadata
        user_ip = job.meta.get("ip", "unknown")
        job_branch = job.meta.get("branch", "stable")
        if job_branch != BRANCH and BRANCH != "LOCAL":
            print(f"Skipping job {job.id} from queue '{queue.name}' (IP: {user_ip}) due to branch mismatch (job branch: {job_branch}, expected: {BRANCH})")
            logger.info(f"Skipping job {job.id} from queue '{queue.name}' (IP: {user_ip}) due to branch mismatch (job branch: {job_branch}, expected: {BRANCH})")
            # Check how long the job has been in the queue
            try:
                if job.enqueued_at is not None and (job.enqueued_at - job.started_at).total_seconds() > 60 * 60 * 24:
                    print(f"Job {job.id} has been in the queue for over 24 hours, cancelling it")
                    logger.info(f"Job {job.id} has been in the queue for over 24 hours, cancelling it")
                    job.cancel()
            except Exception:
                print(f"Failed to check job duration, cancelling it")
                logger.info(f"Failed to check job duration, cancelling it")
            return
        print(f"Processing job {job.id} from queue '{queue.name}' (IP: {user_ip}) with metadata: {json.dumps(job.meta)}")
        logger.info(f"Processing job {job.id} from queue '{queue.name}' (IP: {user_ip}) with metadata: {json.dumps(job.meta)}")

        # Process the job
        super().execute_job(job, queue)


@api.route("/get_selector_info", methods=["GET"])
def get_selector_info():
    """Get the selector data for the randomizer."""
    selector_data = {
        "minigames": MinigameSelector,
        "misc_changes": QoLSelector,
        "hard_mode": HardSelector,
        "hard_bosses": HardBossSelector,
        "enemies": EnemySelector,
        "excluded_songs": ExcludedSongsSelector,
        "song_filters": SongFilteringSelector,
        "itemRando": ItemRandoSelector,
        "keys": KeySelector,
        "glitches": GlitchSelector,
        "helm_hurry_items": HHItemSelector,
        "vanilla_warps": VanillaBananaportSelector,
        "plando_custom_locations": PlannableCustomLocations,
        "plando_items": PlannableItems,
        "plando_minigames": PlannableMinigames,
        "plando_panels": PlandomizerPanels,
        "plando_phases": PlannableKroolPhases,
        "plando_spawns": PlannableSpawns,
        "plando_switches": PlannableSwitches,
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
    """Convert settings between JSON and encrypted string formats."""
    data = request.get_json()
    if "settings" in data:
        try:
            # Attempt to interpret `settings` as JSON
            settings_json = json.loads(data["settings"])
            # If successful, encrypt it
            encrypted = encrypt_settings_string_enum(settings_json)
            return jsonify({"settings_string": encrypted})
        except json.JSONDecodeError:
            # If `settings` is not JSON, decrypt it
            decrypted = decrypt_settings_string_enum(data["settings"])
            return jsonify(decrypted)
    else:
        return jsonify({"error": "Invalid data"}), 400


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
    worker = PriorityAwareWorker(queues, connection=redis_conn)

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
