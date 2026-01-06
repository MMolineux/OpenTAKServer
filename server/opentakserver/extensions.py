from dataclasses import dataclass
import logging
import os
from typing import Any, Optional

import colorlog
from flask_babel import Babel
from flask_ldap3_login import LDAP3LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import yaml
from opentakserver.defaultconfig import DefaultConfig
from opentakserver.models.Base import Base
from flask_mailman import Mail
from flask_apscheduler import APScheduler

from opentakserver.telemetry import TelemetryOpts, setup_telemetry
from opentelemetry.metrics._internal import Meter
from opentakserver.telemetry.ots import configure_logging, configure_metrics, configure_tracing


def _get_config() -> dict[str, Any]:
    config = DefaultConfig.to_dict()
    if not os.path.exists(os.path.join(config.get("OTS_DATA_FOLDER"), "config.yml")):
        DefaultConfig.to_file()  # persist default settings
    else:
        filepath = os.path.join(config.get("OTS_DATA_FOLDER"), "config.yml")
        with open(filepath, "r") as f:
            config = yaml.safe_load(f)
    return config

__cfg = _get_config()

# quick dirty fix to keep global "extensions" pattern for now. 
#TODO: needs to be swapped out for dependency injection later.
logger: logging.Logger = None # type: ignore
meter: Optional[Meter] = None 
mail:Mail = None # type: ignore
apscheduler:APScheduler = None # type: ignore
db:SQLAlchemy = None # type: ignore
socketio:SocketIO = None # type: ignore
migrate:Migrate = None # type: ignore
ldap_manager:LDAP3LoginManager = None # type: ignore
babel:Babel = None # type: ignore

@dataclass
class ExtensionOpts:
    service_name: str

def inject_extension_dependencies(opts:ExtensionOpts):
    """Call from each entry point (opentakserver, eud_handler, cot_parser) at least once during start up to initialize the above module variables.
    
    Adds dependency injection support without modifying how this "global" extensions module works.
    """
    global logger,meter,mail,apscheduler,db,socketio,migrate,ldap_manager,babel
    
    # setup telemtry deps
    _ots_telemetry_opts = TelemetryOpts(
        logging=configure_logging(__cfg),
        metrics=configure_metrics(__cfg),
        tracing=configure_tracing(__cfg)
        )
    # allow entrypoint to override service_name
    _ots_telemetry_opts.logging.service_name = opts.service_name
    _ots_telemetry_opts.metrics.service_name = opts.service_name
    _ots_telemetry_opts.tracing.service_name = opts.service_name
    
    # override above vars
    if logger is None: # meter is optionally None
        logger,meter = setup_telemetry(_ots_telemetry_opts)
    if mail is None:
        mail = Mail()
    if apscheduler is None:
        apscheduler = APScheduler()
    if db is None:
        db = SQLAlchemy(model_class=Base)
    if socketio is None:
        socketio = SocketIO(async_mode="gevent",cors_allowed_origins=["*"])
    if migrate is None:
        migrate = Migrate()
    if ldap_manager is None:
        ldap_manager = LDAP3LoginManager()
    if babel is None:
        babel = Babel()