from flask import Flask, request, jsonify, Blueprint
from redis import Redis
from rq import Queue, Worker
import os
import threading
import json
from waitress import serve
from randomizer.SettingStrings import decrypt_settings_string_enum, encrypt_settings_string_enum
from randomizer.Enums.Types import ItemRandoSelector, KeySelector
from randomizer.Lists.EnemyTypes import EnemySelector
from randomizer.Lists.HardMode import HardBossSelector, HardSelector
from randomizer.Lists.Item import CustomStartingMoveSelector, HHItemSelector
from randomizer.Lists.Logic import GlitchSelector
from randomizer.Lists.Minigame import MinigameSelector
from randomizer.Lists.Multiselectors import FasterCheckSelector, QoLSelector, RemovedBarrierSelector
from randomizer.Lists.Plandomizer import PlandomizerPanels, PlannableCustomLocations, PlannableItems, PlannableKroolPhases, PlannableMinigames, PlannableSpawns, PlannableSwitches
from randomizer.Lists.Songs import ExcludedSongsSelector, MusicSelectionPanel, PlannableSongs, SongFilteringSelector
from randomizer.Lists.Warps import VanillaBananaportSelector
from randomizer.Lists.WrinklyHints import PointSpreadSelector
from worker.tasks import generate_seed

listen = ["tasks_high_priority", "tasks_low_priority"]  # High-priority first
redis_conn = Redis(host="redis", port=6379)
job_timeout = 300  # Timeout in seconds (5 minutes)

app = Flask(__name__)
api = Blueprint("worker_api", __name__)


class PriorityAwareWorker(Worker):
    def execute_job(self, job, queue):
        # Log which queue the job came from and its metadata
        user_ip = job.meta.get("ip", "unknown")
        print(f"Processing job {job.id} from queue '{queue.name}' (IP: {user_ip})")

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
    }
    return jsonify(selector_data)


@api.route("/convert_settings", methods=["POST"])
def convert_settings():
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
    # Start the Flask server
    app.register_blueprint(api)
    serve(app, host="0.0.0.0", port=8000)


def runWorker(jobs):
    # Create queues for high- and low-priority tasks
    queues = [Queue(name, connection=redis_conn, default_timeout=job_timeout) for name in listen]

    # Use the custom PriorityAwareWorker to process tasks
    worker = PriorityAwareWorker(queues, connection=redis_conn)
    # Start processing tasks, prioritizing high-priority queue
    worker.work(max_jobs=jobs, with_scheduler=True)


if __name__ == "__main__":

    # Start the worker in a separate thread
    worker_thread = threading.Thread(target=runWaitressWorker)
    worker_thread.start()

    runWorker(1)
    # Close the worker thread instead of waiting for it to finish
    worker_thread.join(0)
