from flask import Flask, render_template, request, send_file
from dotenv import load_dotenv
import io, os, base64, yt_dlp

load_dotenv() # loads .env variables


# Create yt_dlp configuration options
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'forcefilename': True,
    'merge_output_format': 'mp4',
    'outtmpl' : 'video.mp4',
}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


# video download route
@app.route("/download", methods=['POST'])
def download_video_route():
    try:
        request_json = request.get_json()
        url = request_json["video_url"]

        if url == '':
            return {"error":"empty url string"}, 400

        try:
            os.remove("video.mp4")
        except:
            pass


        try:
            # Download the YouTube video using `yt_dlp` and read the content as bytes
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=True)

        except:
            print(f"error while downloading - {url}")
            return {"error":"couldnt download video sucessfully"}, 500


        return send_file("video.mp4", as_attachment=True, download_name="video.mp4")
    except:
        return "error", 500

# index route
@app.route("/")
def hello_world():
    return render_template("home.html")



if __name__ == '__main__':
    app.run(debug=os.getenv("RUN_AS_DEBUG"))