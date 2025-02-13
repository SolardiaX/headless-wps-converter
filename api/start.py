import os
import traceback
import uuid

from flask import Flask, request, send_file
from waitress import serve


app = Flask(__name__)


@app.route("/convert", methods=["POST"])
def do_convert():    
    file_name_uuid = str(uuid.uuid4())

    post_file = request.files['file']

    if post_file is None:
        return {"success": False}, 400

    try:
        post_file_ext = post_file.filename.rsplit('.')[-1]

        src_file = f"/tmp/converter/{file_name_uuid}.{post_file_ext}"
        dest_file = f"/tmp/converter/{file_name_uuid}.pdf"

        post_file.save(src_file)

        print("Starting file converter - [%s]" % post_file.filename)
        
        if post_file_ext.lower() in ["pptx", "ppt"]:
            from modules.ppt import convert
            convert(src_file, dest_file)
        if post_file_ext.lower() in ["docx", "doc"]:
            from modules.doc import convert
            convert(src_file, dest_file)

        print("Finished file converter - [%s]" % post_file.filename)

        return send_file(dest_file, as_attachment=True)
    except Exception as e:
        print('Failed to execute file converter = [%s]' % post_file)
        print(traceback.format_exc())

        return {"success": False}, 500


if __name__ == "__main__":
    os.makedirs("/tmp/converter", exist_ok=True)
    serve(app, host="0.0.0.0", port=6100)
