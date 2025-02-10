"""Controller Router manages all the worker nodes."""

import json
import logging
import os
import copy
import secrets
import threading
import time
import socket
from datetime import UTC, datetime
from os import environ, path, walk

import requests
from flask import Blueprint, Flask, jsonify, make_response, redirect, render_template, request, send_file, send_from_directory, session
from flask_cors import CORS
from flask_session import Session
from opentelemetry import trace

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from redis import Redis, from_url
from rq import Queue
from rq.job import Job, Retry
from version import version
from waitress import serve
from werkzeug.utils import secure_filename
from cleanup import enable_cleanup
from oauth import DiscordAuth
from functools import wraps
from swagger_ui import flask_api_doc
from werkzeug.middleware.proxy_fix import ProxyFix
from opentelemetry_instrumentation_rq import RQInstrumentor

COOLDOWN_PERIOD = 300  # 5 minutes in seconds

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define a resource to identify your service
resource = Resource(
    attributes={
        "service.name": "controller",
        "service.version": str(version),
        "deployment.environment": os.environ.get("BRANCH", "LOCAL"),
        "container.id": next((l.rsplit("/", 1)[-1] for l in open("/proc/self/cgroup") if "docker" in l), "") if os.path.exists("/proc/self/cgroup") else "",
        "container.name": socket.gethostname(),
    }
)

app = Flask(__name__, static_folder="", template_folder="templates")
app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)
flask_api_doc(app, config_path="./swagger.yaml", url_prefix="/api/doc", title="API doc")
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
# Configure Redis for storing the session data on the server-side
app.config["SESSION_TYPE"] = "redis"
redis_conn = Redis(host="redis", port=6379)
app.config["SESSION_REDIS"] = redis_conn
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
    RQInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    RedisInstrumentor().instrument()
    FlaskInstrumentor().instrument_app(app)
    handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)
    logger.addHandler(handler)


# Create and initialize the Flask-Session object AFTER `app` has been configured
server_session = Session(app)


# Shared structure to manage threads
tasks = {}


class TaskThread(threading.Thread):
    """Thread to run a task in the background."""

    def __init__(self, task_id, target, *args, **kwargs):
        """Initialize the thread with the task ID and target function."""
        super().__init__(*args, **kwargs)
        self.task_id = task_id
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.result_complete = False
        self.result = None

    def run(self):
        """Run the task in the background."""
        if not self.result_complete:
            self.result_complete = True
            self.result = self.target(self.kwargs.get("args")[0])


task_queue_high = Queue("tasks_high_priority", connection=redis_conn)  # High-priority queue
task_queue_low = Queue("tasks_low_priority", connection=redis_conn)  # Low-priority queue
CORS(app, origins=["https://dev.dk64randomizer.com", "https://dk64randomizer.com"])
# Prepend all routes with /api
secret_token = secrets.token_hex(256)

api = Blueprint("api", __name__, url_prefix="/api")
app.config["SECRET_KEY"] = secret_token
# Set the secret key for the blueprint as well
ALLOWED_REFERRERS = ["https://dk64randomizer.com/", "https://dev.dk64randomizer.com/"]
API_KEYS = []
# Check if the file api_keys.cfg exists and load the keys
if path.isfile("api_keys.cfg"):
    with open("api_keys.cfg", "r") as f:
        keys = f.read().splitlines()
        cleared_keys = [key for key in keys if len(key) > 0]
        API_KEYS.extend(cleared_keys)

discord = DiscordAuth(
    environ.get("CLIENT_ID"),
    environ.get("CLIENT_SECRET"),
    environ.get("REDIRECT", "http://localhost:8000/admin"),
    "463917049782075395",
)
admin_roles = ["550784070188138508", "550784038600835101"]


def enforce_api_restrictions():
    """Enforce API restrictions on the request."""

    def decorator(func):
        """Enforce API restrictions."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Enforce API restrictions."""
            referer = request.headers.get("Referer")
            api_key = request.headers.get("X-API-Key")

            # Check if the request is allowed based on referer or API key
            if "*" not in ALLOWED_REFERRERS and (referer not in ALLOWED_REFERRERS and api_key not in API_KEYS):
                print(f"Unauthorized access attempt from IP: {get_user_ip()}, Referer: {referer}, API Key: {api_key}")
                return jsonify({"error": "Unauthorized access"}), 403

            # Validate the request is JSON
            if request.method in ["POST", "PUT"] and request.content_type not in ["application/json", "application/json; charset=utf-8"]:
                return jsonify({"error": "Invalid content type"}), 400

            # Check if they provide a branch in their args, if they don't, default to 'dev'
            if "branch" not in request.args:
                args_copy = request.args.to_dict()
                args_copy["branch"] = "stable"
                request.args = args_copy

            return func(*args, **kwargs)

        return wrapper

    return decorator


def set_response(content, status_code, content_type="application/json", version_header=version):
    """Set common response headers."""
    response = make_response(content, status_code)
    response.mimetype = content_type
    response.headers["Content-Type"] = f"{content_type}; charset=utf-8"
    response.headers["Version"] = version_header
    return response


cached_local_presets = None
last_updated = 0
CACHE_DURATION = 300  # Cache duration in seconds


def update_presets(force=False):
    """Update the local presets from the JSON file."""
    global cached_local_presets, last_updated
    current_time = int(time.time())
    if cached_local_presets is not None and (current_time - last_updated) < CACHE_DURATION and not force:
        return cached_local_presets

    if path.isfile("local_presets.json"):
        with open("local_presets.json", "r") as f:
            local_presets = json.load(f)
            cached_local_presets = local_presets
    else:
        local_presets = {"stable": [], "dev": []}
        cached_local_presets = local_presets
    return local_presets


def get_user_ip():
    """Retrieve the user's IP address."""
    if request.headers.get("Cf-Connecting-Ip"):
        return request.headers.get("Cf-Connecting-Ip")
    elif request.headers.get("X-Real-IP"):
        return request.headers.get("X-Real-IP")
    elif request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For")
    return request.remote_addr


@api.route("/submit-task", methods=["POST"])
@enforce_api_restrictions()
def submit_task():
    """Submit a task to the worker queue."""
    data = request.json
    branch = request.args.get("branch", "stable")
    if os.environ.get("TEST_REDIS") == "1":
        # Start the task immediately if we're using a fake Redis server
        # Make it a thread, and we're going to directly import and call the function
        from worker.tasks import generate_seed

        global tasks
        json_data = json.loads(data.get("settings_data"))
        task_thread = TaskThread(task_id="testingID", target=generate_seed, args=(json_data,))
        tasks["testingID"] = task_thread
        task_thread.start()
        return set_response(json.dumps({"task_id": "testingID", "status": "queued", "priority": "High"}), 200)
    if not data or "settings_data" not in data:
        return set_response(json.dumps({"error": "Invalid payload"}), 400)
    if isinstance(data.get("settings_data"), str):
        settings_data = json.loads(data.get("settings_data"))
    else:
        settings_data = data.get("settings_data")
    user_ip = get_user_ip()
    # Check the last submission time for this IP
    last_submission_key = f"last_submission:{user_ip}"
    last_submission_time = redis_conn.get(last_submission_key)
    if last_submission_time is not None:
        last_submission_time = int(last_submission_time.decode())
    current_time = int(time.time())

    # Determine the priority based on the cooldown period
    if last_submission_time is None or current_time - int(last_submission_time) > COOLDOWN_PERIOD:
        # High-priority queue
        task = task_queue_high.enqueue("tasks.generate_seed", settings_data, meta={"ip": user_ip, "branch": branch}, retry=Retry(max=2))
        priority = "High"
    else:
        # Low-priority queue
        task = task_queue_low.enqueue("tasks.generate_seed", settings_data, meta={"ip": user_ip, "branch": branch}, retry=Retry(max=1))
        priority = "Low"

    # Update the last submission time for this IP
    redis_conn.set(last_submission_key, current_time)

    return set_response(json.dumps({"task_id": task.id, "status": task.get_status(), "priority": priority}), 200)


@api.route("/task-status/<task_id>", methods=["GET"])
@enforce_api_restrictions()
def task_status(task_id):
    """Get the status of a task."""
    if os.environ.get("TEST_REDIS") == "1":
        global tasks
        task_thread = tasks.get(task_id)
        if task_thread:
            if not task_thread.result_complete:
                task_thread.run()
            if task_thread.is_alive():
                return jsonify({"task_id": task_id, "status": "started", "priority": "High"}), 200
            else:
                result = task_thread.result
                return set_response(json.dumps({"result": result, "status": "finished"}), 200)
    try:
        task = Job.fetch(task_id, connection=redis_conn)
    except Exception:
        return set_response(json.dumps({"error": "Task not found"}), 404)
    # Fetch task from both queues
    task = Job.fetch(task_id, connection=redis_conn)
    if not task:
        return set_response(json.dumps({"error": "Task not found"}), 404)
    # Get what was returned from the task
    if task.result:
        # make sure we clear the task from the queue if it's done
        result = copy.copy(task.result)
        # task.delete()
        return set_response(json.dumps({"result": result, "status": "finished"}), 200)
    # If the task failed, return the error message
    if task.exc_info:
        # Summarize the error message to just the final exception
        exceptdata = task.exc_info.strip().split("\n")[-1]
        return set_response(json.dumps({"error": exceptdata}), 500)

    # Get the position in the queue
    position = 0
    if task in task_queue_high.jobs:
        position = task_queue_high.jobs.index(task)
    elif task in task_queue_low.jobs:
        position = task_queue_low.jobs.index(task) + len(task_queue_high.jobs)
    return set_response(json.dumps({"task_id": task.id, "status": task.get_status(), "position": position}), 200)


@api.route("/get_version", methods=["GET"])
@enforce_api_restrictions()
def get_version():
    """Get the version of the controller."""
    return set_response(json.dumps({"version": version}), 200)


@api.route("/get_presets", methods=["GET"])
@enforce_api_restrictions()
def get_presets():
    """Get the presets for the randomizer."""
    branch = request.args.get("branch")
    return_blank = request.args.get("return_blank")
    presets_to_return = []
    presets = update_presets()
    presets = presets.get(branch, [])
    if return_blank is None:
        presets_to_return = [preset for preset in presets if preset.get("settings_string") is not None]
    else:
        preset_added = False
        for preset in presets:
            if preset.get("settings_string") is None and not preset_added:
                presets_to_return.append(preset)
                preset_added = True
            elif preset.get("settings_string") is not None:
                presets_to_return.append(preset)

    return set_response(json.dumps(presets_to_return), 200)


@app.route("/admin", methods=["GET"])
def admin_portal():
    """Serve the admin portal."""
    # Branch Data for the admin portal
    branch = os.environ.get("BRANCH", "LOCAL")
    if session.get("admin") is None:
        if branch == "LOCAL":
            # This is a debug chunk of code for when locally testing the admin portal
            session["admin"] = True
        else:
            code = request.args.get("code")
            if code is None:
                return redirect(discord.login())

            tokens = discord.get_tokens(code)
            try:
                guilds = discord.get_guild_roles(tokens.get("access_token"))
            except Exception:
                guilds = {}

            if not any(role in admin_roles for role in guilds.get("roles", [])):
                return set_response("You do not have permission to access this page.", 403, "text/html")
            else:
                session["admin"] = True

    if not session.get("admin", False):
        session.pop("admin")
        return set_response("You do not have permission to access this page.", 403, "text/html")
    local_presets = update_presets()
    return render_template("admin.html", local_presets=local_presets)


@api.route("/admin/presets", methods=["PUT", "DELETE"])
def admin_presets():
    """Update or delete a local preset."""
    if not session.get("admin", False):
        return set_response(json.dumps({"message": "You do not have permission to access this page."}), 403)

    content = request.json
    local_presets = update_presets()
    # Check if branch is in the body
    branch = content.get("branch", "")
    if branch not in ["stable", "dev"]:
        return set_response(json.dumps({"message": "Invalid branch"}), 400)
    if request.method == "PUT":
        preset_name = content.get("name")
        found_preset = False
        for i, preset in enumerate(local_presets[branch]):
            if preset.get("name").lower() == preset_name.lower():
                local_presets[branch][i] = content
                found_preset = True
                break
        if not found_preset:
            local_presets[branch].append(content)

        with open("local_presets.json", "w") as f:
            f.write(json.dumps(local_presets))
        update_presets(True)
        return set_response(json.dumps({"message": "Local presets updated"}), 200)

    elif request.method == "DELETE":
        preset_name = content.get("name")
        found = False
        for i, preset in enumerate(local_presets[branch]):
            if preset.get("name").lower() == preset_name.lower():
                local_presets[branch].pop(i)
                found = True
                break
        if not found:
            return set_response(json.dumps({"message": "Preset not found"}), 404)
        else:
            with open("local_presets.json", "w") as f:
                f.write(json.dumps(local_presets))
            update_presets(True)
            return set_response(json.dumps({"message": "Local presets deleted"}), 200)


@api.route("/get_seed", methods=["GET"])
@enforce_api_restrictions()
def get_seed():
    """Get the lanky for a seed."""
    # Get the hash from the query string and sanitize it
    seed_hash = request.args.get("hash")
    if not seed_hash:
        return set_response({"error": "Missing hash parameter"}, 400)

    file_name = secure_filename(seed_hash)
    base_dir = path.normpath("generated_seeds/")
    json_path = path.normpath(path.join(base_dir, f"{file_name}.json"))
    lanky_path = path.normpath(path.join(base_dir, f"{file_name}.lanky"))

    # Validate that the paths stay within the intended directory
    if not json_path.startswith(base_dir) or not lanky_path.startswith(base_dir):
        return set_response({"error": "Invalid hash parameter"}, 400)

    # Check if the lanky file exists
    if not path.isfile(lanky_path):
        return set_response({"error": "Lanky file not found"}, 404)

    # Serve the lanky file
    try:
        return send_file(
            lanky_path,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"{file_name}.lanky",
        )
    except Exception as e:
        logging.error(f"Error in get_seed: {e}")
        return set_response({"error": "An internal error has occurred"}, 500)


@api.route("/get_spoiler_log", methods=["GET"])
@enforce_api_restrictions()
def get_spoiler_log():
    """Get the spoiler log for a seed."""
    # Get the hash from the query string
    seed_hash = request.args.get("hash")
    if not seed_hash:
        return set_response({"error": "Missing hash parameter"}, 400)

    file_name = secure_filename(seed_hash)
    base_dir = path.normpath("generated_seeds/")
    json_path = path.normpath(path.join(base_dir, f"{file_name}.json"))

    # Ensure the path stays within the intended directory
    if not json_path.startswith(base_dir):
        return set_response({"error": "Access denied"}, 403)

    # Check if the JSON file exists
    if not path.isfile(json_path):
        return set_response({"error": "File not found"}, 404)

    # Read and process the JSON file
    try:
        with open(json_path, "r") as f:
            file_contents = json.load(f)
            current_time = time.time()

            # Check unlock time
            if file_contents.get("Unlock Time", 0) > current_time:
                return set_response({"error": "Spoiler log is locked"}, 425)

            # Return the spoiler log
            return set_response(jsonify(file_contents), 200)
    except json.JSONDecodeError:
        return set_response({"error": "Invalid JSON format in file"}, 500)
    except Exception as e:
        logging.error(f"Error in get_spoiler_log: {e}", exc_info=True)
        return set_response({"error": "An internal error has occurred"}, 500)


@api.route("/current_total", methods=["GET"])
def get_current_total():
    """Get the current total of generated seeds."""
    current_total, last_generated_time = get_total_info()
    if request.args.get("format") == "total_shield":
        response_data = {
            "label": "Seeds Generated",
            "message": str(current_total),
            "schemaVersion": 1,
            "color": "darkcyan",
        }
    elif request.args.get("format") == "time_shield":
        response_data = {
            "label": "Last Generated",
            "message": str(last_generated_time.strftime("%Y-%m-%d %H:%M:%S.%f")),
            "schemaVersion": 1,
            "color": "darkcyan",
        }
    else:
        response_data = {
            "total_seeds": current_total,
            "last_generated_time": last_generated_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
        }
    return set_response(json.dumps(response_data), 200)


def get_total_info():
    """Get the total number of generated seeds."""
    current_total = 0
    try:
        with open("current_total.cfg", "r") as f:
            current_total = int(f.read())
    except ValueError:
        current_total = 0
    except Exception:
        current_total = 0
        with open("current_total.cfg", "w") as f:
            f.write(str(current_total))
    try:
        with open("last_generated_time.cfg", "r") as f:
            last_generated_time = datetime.strptime(f.read().strip(), "%Y-%m-%d %H:%M:%S.%f%z")
    except ValueError:
        logging.error("Incorrect date format in last_generated_time.cfg, resetting to current time.")
        last_generated_time = datetime.now(UTC)
        with open("last_generated_time.cfg", "w") as f:
            f.write(last_generated_time.isoformat())
    except Exception:
        # If we can't read the file, just set it to the current time.
        last_generated_time = datetime.now(UTC)
        with open("last_generated_time.cfg", "w") as f:
            f.write(last_generated_time.isoformat())
    return current_total, last_generated_time


@api.route("/get_selector_info", methods=["GET"])
@enforce_api_restrictions()
def get_selector_info():
    """Get the selector data for the randomizer."""
    # If the branch arg is master call os.environ.get("WORKER_URL_MASTER") with requests
    # Else call os.environ.get("WORKER_URL_DEV") with requests
    url = environ.get("WORKER_URL_MASTER") if request.args.get("branch") == "stable" else environ.get("WORKER_URL_DEV")
    if not url:
        url = "http://127.0.0.1:8000"
    response = requests.get(f"{url}/get_selector_info")
    return set_response(response.text, response.status_code)


@api.route("/convert_settings", methods=["POST"])
@enforce_api_restrictions()
def convert_settings():
    """Convert settings for the randomizer."""
    url = environ.get("WORKER_URL_MASTER") if request.args.get("branch") == "stable" else environ.get("WORKER_URL_DEV")
    if not url:
        url = "http://127.0.0.1:8000"
    data = request.get_json()
    response = requests.post(f"{url}/convert_settings", json=data)
    return set_response(response.json(), response.status_code)


app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
