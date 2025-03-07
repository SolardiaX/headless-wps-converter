import os
import uuid
from io import BytesIO

from flask import Flask, request, send_file
from loguru import logger
from waitress import serve

logger.add("/tmp/api.log", rotation="100 MB", retention="10 days")

app = Flask(__name__)


@app.route("/convert", methods=["POST"])
def do_convert():
    file_name_uuid = str(uuid.uuid4())

    post_file = request.files["file"]

    if post_file is None:
        return {"success": False}, 400

    try:
        post_file_ext = post_file.filename.rsplit(".")[-1]

        src_file = f"/tmp/converter/{file_name_uuid}.{post_file_ext}"
        dest_file = f"/tmp/converter/{file_name_uuid}.pdf"

        post_file.save(src_file)

        logger.info("Starting file converter - [%s]" % post_file.filename)

        if post_file_ext.lower() in ["pptx", "ppt"]:
            from modules.ppt import convert

            convert(src_file, dest_file)
        if post_file_ext.lower() in ["docx", "doc"]:
            from modules.doc import convert

            convert(src_file, dest_file)

        logger.info("Finished file converter - [%s]" % post_file.filename)

        return_data = BytesIO()
        with open(dest_file, "rb") as fo:
            return_data.write(fo.read())
        # (after writing, cursor will be at last byte, so move it to start)
        return_data.seek(0)

        os.remove(src_file)
        os.remove(dest_file)

        return send_file(return_data, as_attachment=True)
    except Exception as e:
        logger.error(
            f"Failed to execute file converter, file - [{post_file}], error - {e}"
        )

        return {"success": False}, 500


if __name__ == "__main__":
    os.makedirs("/tmp/converter", exist_ok=True)
    serve(app, host="0.0.0.0", port=6100)
