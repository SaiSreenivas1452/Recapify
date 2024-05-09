from flask import Flask, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

app = Flask(__name__, template_folder='templates')
genai.configure(api_key='AIzaSyAkuJD87qWK_ebHPJYM1KiGZQU1FTmQD5Y')  # Replace with your API key

def get_transcript(video_url):
    video_id = video_url.split('v=')[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = ' '.join([entry['text'] for entry in transcript])
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    if request.method == "POST":
        video_url = request.form["url"]
        try:
            transcript = get_transcript(video_url)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("summarize the key points in below data: " + transcript)
            summary = response.text
        except Exception as e:
            print(e)
            summary = "An error occurred. Please try again."
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
