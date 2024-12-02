import json
import secrets
from os import path, walk, environ
from werkzeug.utils import secure_filename
import time

COOLDOWN_PERIOD = 300  # 5 minutes in seconds

from cleanup import enable_cleanup
from flask import Blueprint, Flask, jsonify, make_response, request, session, send_from_directory, render_template, redirect, send_file
from flask_cors import CORS
from redis import Redis
from rq import Queue
from rq.job import Job
from datetime import datetime, UTC
from oauth import DiscordAuth
import requests
from version import version
from waitress import serve
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
import logging

import os
import threading

app = Flask(__name__, static_folder="", template_folder="")
app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)
# Shared structure to manage threads
tasks = {}


class TaskThread(threading.Thread):
    def __init__(self, task_id, target, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_id = task_id
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def run(self):
        self.result = self.target(self.kwargs.get("args")[0])


redis_conn = Redis(host="redis", port=6379)
task_queue_high = Queue("tasks_high_priority", connection=redis_conn)  # High-priority queue
task_queue_low = Queue("tasks_low_priority", connection=redis_conn)  # Low-priority queue
CORS(app)
# Prepend all routes with /api
app.config["SECRET_KEY"] = secrets.token_hex(256)

api = Blueprint("api", __name__, url_prefix="/api")
ALLOWED_REFERRERS = ["https://dk64randomizer.com"]
API_KEYS = ["your_api_key_1", "your_api_key_2"]
discord = DiscordAuth(
    environ.get("CLIENT_ID"),
    environ.get("CLIENT_SECRET"),
    environ.get("REDIRECT", "http://localhost:8000/admin"),
    "463917049782075395",
)
admin_roles = ["550784070188138508"]


@api.before_request
def enforce_api_restrictions():
    referer = request.headers.get("Referer")
    api_key = request.headers.get("X-API-Key")
    # Check if the request is allowed based on referer or API key
    if referer not in ALLOWED_REFERRERS and "*" not in ALLOWED_REFERRERS and api_key not in API_KEYS:
        print(f"Unauthorized access attempt from IP: {get_user_ip()}, Referer: {referer}, API Key: {api_key}")
        return set_response(json.dumps({"error": "Unauthorized access"}), 403)
    # Validate the request is JSON
    if request.method in ["POST", "PUT"] and request.content_type != "application/json":
        return set_response(json.dumps({"error": "Invalid content type"}), 400)
    # Check if they provide a branch in their args, if they don't default to dev
    if "branch" not in request.args:
        request.args = request.args.to_dict()
        request.args["branch"] = "dev"


def set_response(content, status_code, content_type="application/json", version_header=version):
    """Utility function to set common response headers."""
    response = make_response(content, status_code)
    response.mimetype = content_type
    response.headers["Content-Type"] = f"{content_type}; charset=utf-8"
    response.headers["Version"] = version_header
    return response


def update_presets():
    """Update the presets list with the global and local presets."""
    presets = []
    local_presets = []
    with open("static/presets/preset_files.json", "r") as f:
        presets = json.load(f)
    if path.isfile("local_presets.json"):
        with open("local_presets.json", "r") as f:
            local_presets = json.load(f)
            for local_preset in local_presets:
                found_preset = False
                for i, global_preset in enumerate(presets):
                    if global_preset.get("name") == local_preset.get("name"):
                        presets[i] = local_preset
                        found_preset = True
                        break
                if not found_preset:
                    presets.append(local_preset)
    return presets, local_presets


def get_user_ip():
    """Retrieve the user's IP address."""
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0]
    return request.remote_addr


@api.route("/submit-task", methods=["POST"])
def submit_task():
    data = request.json
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
    current_time = int(time.time())

    # Determine the priority based on the cooldown period
    if last_submission_time is None or current_time - int(last_submission_time) > COOLDOWN_PERIOD:
        # High-priority queue
        task = task_queue_high.enqueue("tasks.generate_seed", settings_data, meta={"ip": user_ip})
        priority = "High"
    else:
        # Low-priority queue
        task = task_queue_low.enqueue("tasks.generate_seed", settings_data, meta={"ip": user_ip})
        priority = "Low"

    # Update the last submission time for this IP
    redis_conn.set(last_submission_key, current_time)

    return set_response(json.dumps({"task_id": task.id, "status": task.get_status(), "priority": priority}), 200)


@api.route("/task-status/<task_id>", methods=["GET"])
def task_status(task_id):
    if os.environ.get("TEST_REDIS") == "1":
        global tasks
        task_thread = tasks.get(task_id)
        if task_thread:
            if task_thread.is_alive():
                return jsonify({"task_id": task_id, "status": "started", "priority": "High"}), 200
            else:
                # Retrieve and return the result
                result = task_thread.result
                return set_response(json.dumps({"result": result, "status": "finished"}), 200)
        return jsonify({"error": "Task not found"}), 404
    # Fetch task from both queues
    task = Job.fetch(task_id, connection=redis_conn)
    if not task:
        return set_response(json.dumps({"error": "Task not found"}), 404)
    # Get what was returned from the task
    if task.result:
        return set_response(json.dumps({"result": task.result, "status": "finished"}), 200)
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
def get_version():
    return set_response(json.dumps({"version": version}), 200)


@api.route("/get_presets", methods=["GET"])
def get_presets():
    return_blank = request.args.get("return_blank")
    presets_to_return = []
    presets, local_presets = update_presets()
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


@api.route("/admin", methods=["GET"])
def admin_portal():
    if session.get("admin") is None:
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
    presets, local_presets = update_presets()
    return render_template("admin.html.jinja2", local_presets=local_presets)


@api.route("/admin/presets", methods=["PUT", "DELETE"])
def admin_presets():
    if not session.get("admin", False):
        return set_response(json.dumps({"message": "You do not have permission to access this page."}), 403)

    content = request.json
    presets, local_presets = update_presets()
    if request.method == "PUT":
        preset_name = content.get("name")
        found_preset = False
        for i, preset in enumerate(local_presets):
            if preset.get("name").lower() == preset_name.lower():
                local_presets[i] = content
                found_preset = True
                break
        if not found_preset:
            local_presets.append(content)

        with open("local_presets.json", "w") as f:
            f.write(json.dumps(local_presets))
        update_presets()
        return set_response(json.dumps({"message": "Local presets updated"}), 200)

    elif request.method == "DELETE":
        preset_name = content.get("name")
        found = False
        for i, preset in enumerate(local_presets):
            if preset.get("name").lower() == preset_name.lower():
                local_presets.pop(i)
                found = True
                break
        if not found:
            return set_response(json.dumps({"message": "Preset not found"}), 404)
        else:
            with open("local_presets.json", "w") as f:
                f.write(json.dumps(local_presets))
            update_presets()
            return set_response(json.dumps({"message": "Local presets deleted"}), 200)


@api.route("/get_seed", methods=["GET"])
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
        return set_response({"error": str(e)}, 500)


@api.route("/get_spoiler_log", methods=["GET"])
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
        return set_response({"error": str(e)}, 500)


@api.route("/current_total", methods=["GET"])
def get_current_total():
    current_total, last_generated_time = get_total_info()
    response_data = {
        "total_seeds": current_total,
        "last_generated_time": last_generated_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
    }
    return set_response(json.dumps(response_data), 200)


def get_total_info():
    current_total = 0
    try:
        with open("current_total.cfg", "r") as f:
            current_total = int(f.read())
    except Exception:
        # If we can't read the file, just set it to 0 in the file.
        with open("current_total.cfg", "w") as f:
            f.write("0")
    last_generated_time = datetime.now(UTC)
    try:
        with open("last_generated_time.cfg", "r") as f:
            last_generated_time = datetime.strptime(f.read(), "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        # If we can't read the file, just set it to 0 in the file.
        with open("last_generated_time.cfg", "w") as f:
            f.write(str(last_generated_time))
    return current_total, last_generated_time


@api.route("/get_selector_info", methods=["GET"])
def get_selector_info():
    """Get the selector data for the randomizer."""
    # If the branch arg is master call os.environ.get("WORKER_URL_MASTER") with requests
    # Else call os.environ.get("WORKER_URL_DEV") with requests
    url = environ.get("WORKER_URL_MASTER") if request.args.get("branch") == "master" else environ.get("WORKER_URL_DEV")
    response = requests.get(f"{url}/get_selector_info")
    return set_response(response.json(), response.status_code)


@api.route("/convert_settings", methods=["POST"])
def convert_settings():
    url = environ.get("WORKER_URL_MASTER") if request.args.get("branch") == "master" else environ.get("WORKER_URL_DEV")
    data = request.get_json()
    response = requests.post(f"{url}/convert_settings", json=data)
    return set_response(response.json(), response.status_code)

app.register_blueprint(api, url_prefix="/api")

print("Pre startup")
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
    logger.info("Starting the server")
    if os.environ.get("BRANCH") == "LOCAL":
        logger.info("Starting the server in local mode")

        @app.route("/")
        def index():
            """Serve the index page."""
            print("Serving index page")
            return send_from_directory(".", "index.html")

        @app.route("/randomizer")
        def rando():
            """Serve the randomizer page."""
            return send_from_directory(".", "randomizer.html")

        ALLOWED_REFERRERS.extend(["*"])
        API_KEYS.append("LOCAL_API_KEY")

    serve(app, host="0.0.0.0", port=8000)
