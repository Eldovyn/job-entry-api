from flask import Blueprint, request, send_file
from ..controllers import BatchFormController
import cloudinary.api
import requests
import tempfile

attachment_router = Blueprint("attachment_router", __name__)


@attachment_router.get("/job-entry/cv")
async def get_cv():
    params = request.args
    attachment_id = params.get("attachment_id", "")
    result = cloudinary.api.resource_by_asset_id("284a33fddaa1e0382f2d19701760e42f")
    print(result)
    return "oke"
