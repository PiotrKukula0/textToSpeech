from flask import Flask, request, make_response, render_template
from gtts import gTTS


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/tts', methods=['GET'])
def tts():
    text = request.args.get('text')
    allowed_languages = ['en', 'pl']
    language = request.args.get('language', 'en')
    if language not in allowed_languages:
        language = 'en'
    if text and text.strip():
        try:
            tts = gTTS(text=text, lang=language)
            tts.save("audio.mp3")
            with open("audio.mp3", "rb") as f:
                data = f.read()
                response = make_response(data)
                response.headers["Content-Disposition"] = "attachment; filename=audio.mp3"
                return response
        except Exception as e:
            return "An error occurred while generating audio file: {}".format(e)
    else:
        return "No text to speak"


if __name__ == "__main__":
    app.run(debug=True)
