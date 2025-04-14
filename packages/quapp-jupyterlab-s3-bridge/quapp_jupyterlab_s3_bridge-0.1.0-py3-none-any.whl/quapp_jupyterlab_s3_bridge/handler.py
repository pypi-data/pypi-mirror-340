# handler.py
import json
import tornado.web
from jupyter_server.base.handlers import APIHandler
from .manager import S3SelectiveContentsManager

class VersionsHandler(APIHandler):
    @tornado.web.authenticated
    async def get(self):
        cm = self.settings.get("contents_manager")
        if not isinstance(cm, S3SelectiveContentsManager):
            self.set_status(400)
            self.finish(json.dumps({"error": "Not S3SelectiveContentsManager"}))
            return
        try:
            versions = cm.get_versions_list()
            self.finish(json.dumps({"data": versions}))
        except Exception as e:
            self.set_status(500)
            self.finish(json.dumps({"error": str(e)}))

class PresignedUrlsHandler(APIHandler):
    @tornado.web.authenticated
    async def patch(self, version: int):
        if not version.isdigit():
            self.set_status(400)
            self.finish(json.dumps({"error": "Invalid version"}))
            return
        version = int(version)
        cm = self.settings.get("contents_manager")
        if not isinstance(cm, S3SelectiveContentsManager):
            self.set_status(400)
            self.finish(json.dumps({"error": "Not S3SelectiveContentsManager"}))
            return
        try:
            urls = cm.update_file_list(version)
            self.finish(json.dumps({"data": urls}))
        except Exception as e:
            self.set_status(500)
            self.finish(json.dumps({"error": str(e)}))

class UploadS3Handler(APIHandler):
    @tornado.web.authenticated
    async def post(self):
        cm = self.settings.get("contents_manager")
        if not isinstance(cm, S3SelectiveContentsManager):
            self.set_status(400)
            self.finish(json.dumps({"error": "Not S3SelectiveContentsManager"}))
            return
        try:
            await cm.upload_to_backend(description="FileBrowser Save S3")
            self.finish(json.dumps({"status": "ok"}))
        except Exception as e:
            self.set_status(500)
            self.finish(json.dumps({"error": str(e)}))
