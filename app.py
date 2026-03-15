from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

UPLOAD_FOLDER = "submissions"
ALLOWED_EXTENSIONS = {"ppt", "pptx", "pdf", "zip"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        urn = request.form["urn"]
        file = request.files["file"]

        if file and allowed_file(file.filename):

            extension = file.filename.rsplit(".", 1)[1]
            filename = f"{urn}.{extension}"

            filepath = os.path.join(UPLOAD_FOLDER, filename)

            # Prevent duplicate submission
            if os.path.exists(filepath):
                return "You have already submitted your file."

            file.save(filepath)

            return redirect("/submissions")

    return render_template("upload.html")


@app.route("/submissions")
def submissions():

    files = os.listdir(UPLOAD_FOLDER)

    return render_template("submissions.html", files=files)


app.run(debug=True)