__author__ = 'Gareth'

import logging
import os
import yaml

from beaker.middleware import SessionMiddleware
from bottle import run, default_app, request, hook

from internal.blocks import Blocks
from internal.data import Data
from internal.db import Db
from internal.schemas import schemas
from internal.templates import Templates
from internal.util import log_request, log


class Manager(object):

    db = {}
    mongo_conf = {}
    mongo = None

    def __init__(self):
        self.app = default_app()

        self.db = yaml.load(open("config/database.yml", "r"))
        self.mongo_conf = self.db["mongo"]
        self.main_conf = yaml.load(open("config/config.yml", "r"))

        self.setup_mongo()

        self.db_uri = self.mongo.uri + ".sessions"

        session_opts = {
            "session.cookie_expires": True,
            "session.type": "mongodb",
            "session.url": self.db_uri,
            "session.lock_dir": "sessions/lock/",
            "session.skip_pickle": True,
            "secret": self.main_conf["secret"]
        }

        def setup_request():
            request.session = request.environ['beaker.session']

        hook('before_request')(setup_request)

        self.wrapped = SessionMiddleware(self.app, session_opts)

        self.blocks = Blocks(self)
        self.data = Data(self)
        self.templates = Templates(self)

        self.routes = {}
        self.api_routes = []

        files = os.listdir("routes")
        files.remove("__init__.py")

        for _file in files:
            if _file.endswith(".py"):
                module = _file.rsplit(".", 1)[0]
                if module in self.main_conf.get("disabled-routes", []):
                    log("Routes module '%s' is disabled - not loading."
                        % module, logging.INFO)
                    continue
                try:
                    log("Loading routes module '%s'..." % module, logging.INFO)
                    mod = __import__("routes.%s" % module, fromlist=["Routes"])
                    self.routes[module] = mod.Routes(self.wrapped, self)
                except Exception as e:
                    log("Error loading routes module '%s': %s" % (module, e))

        log("%s routes set up." % len(self.app.routes))

    def add_api_route(self, route):
        if route in self.api_routes:
            return False
        self.api_routes.append(route)
        self.api_routes = sorted(self.api_routes)
        return True

    def get_app(self):
        return self.wrapped

    def setup_mongo(self):
        try:
            self.mongo = Db(self.mongo_conf)
            self.mongo.setup()

            for key in schemas.keys():
                log("Adding schema for collection: %s" % key)
                self.mongo.add_schema(key, schemas[key])

            self.mongo.client.admin.command("ping")
            log("Set up Mongo successfully.")
        except Exception as e:
            log("Unable to set up Mongo: %s" % e, logging.ERROR)

    def start(self):
        def log_all():
            log_request(request, "%s %s " % (request.method, request.fullpath))

        hook('after_request')(log_all)

        try:
            config = yaml.load(open("config/development.yml", "r"))
            host = config.get("host", "127.0.0.1")
            port = config.get("port", 8080)
            server = config.get("server", "cherrypy")
        except Exception as e:
            log("Unable to load development config: %s" % e)
            log("Continuing using the defaults.")
            host = "127.0.0.1"
            port = 8080
            server = "cherrypy"

        run(app=self.wrapped, host=host, port=port, server=server)
