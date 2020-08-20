import cv2
import numpy as np
import milvago


class WebCamera:
    def __init__(self, camera_id: str):
        self.video = cv2.VideoCapture(int(camera_id))

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, image = np.array(self.video.read())
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class WebcamStream(milvago.HttpMlv):

    def __init__(self):
        milvago.HttpMlv.__init__(self, '/stream.mjpeg')

    def get(self):
        labeled_frame = WebcamStream.load_frame(
            WebCamera(self.request.params.get("camera", 0))
        )
        self.set_custom_content_type("multipart/x-mixed-replace; boundary=frame")
        self.response.stream = labeled_frame

    @staticmethod
    def load_frame(cam):
        while True:
            yield (b'--frame\r\nContent-Type: image/jpeg'
                   b'\r\n\r\n' + cam.get_frame() + b'\r\n\r\n')


@milvago.expose_web('/')
def index(web):
    web.set_content_type("html")
    return '''
    <html>
        <head>
            <meta charset="utf-8"/>
            <script type="text/javascript">
                function motionjpeg(id) {
                    var image = $(id), src;

                    if (!image.length) return;

                    src = image.attr("src");
                    if (src.indexOf("?") < 0) {
                        image.attr("src", src + "?"); // must have querystring
                    }

                    image.on("load", function() {
                        // this cause the load event to be called "recursively"
                        this.src = this.src.replace(/\?[^\n]*$/, "?") +
                            (new Date()).getTime();
                });
            }
        </script>
        </head>
        <body>
            <iframe src="/stream.mjpeg" height="600" width="800" frameBorder="0"></iframe>
        </body>

    </html>'''

srv = milvago.Milvago(
    [index(), WebcamStream()],
    debug=False,
)
webcam = srv()
