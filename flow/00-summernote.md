## summernote
```html
<textarea class="form-control" rows="8" id="summernote" name="contents" placeholder="내용을 입력하세요.."></textarea>
```
```jsx
$(document).ready(function() {
  $('#summernote').summernote();
});
```
일단 이렇게만 하면 끝이다.  
근데 좌측상단에 이상한거 뜨는거는 이렇게없앤다.

```jsx
$('#summernote').summernote({
        height: 300,
        minHeight: null,
        maxHeight: null,
        lang : 'ko-KR',
        popover: {
            image: [],
            link: [],
            air: []
        },
```

view.html에서 아래와 같이 해주자
```html
<td colspan="2"><div style="min-height:200px;">{% autoescape false %}{{result.contents}}{% endautoescape %}</div></td>
```

### 이미지 업로드
섬머노트 textarea에 이미지가 첨부되면 이 이벤트를 감지해서  
이미지를 서버에 전송.  
전송이 완료되면 해당 이미지의 주소를 리턴(textarea로!)  
주소만 img 태그를 써서 링크를 거는 방식으로 동작하게 만들자!  

```jsx
$('#summernote').summernote({
    ...
        callbacks: {
            onImageUpload: function(image) {
                // uploadImage(image[0]); // 하나일때
                for(let i=0; i < image.length; i++) {
                    uploadImage(image[i]);
                }
            }
        }
```

```jsx
function uploadImage(image) {
    var data = new FormData(); // formdata를 처리하기위한 객체
    data.append("image", image);
    $.ajax({
        url: "{{url_for('board.upload_image')}}",
        cache: false, // cache 가 true 이면 캐싱된 데이터로 처리될 수 있어 데이터 전송이 되지 않을수 있어 false
        contentType: false, // 기본값이 application/x-www-form-urlencoded 인데 파일전송시에는 multipart/form-data 로 보내야 하기 때문에 false
        processData: false, //POST 형태의 데이터를 전달할때는 query string 형태의 GET 방식으로 보내면 안되기 때문에 false
        data: data,
        type: "post",
        success: function(url) {
            var image = $('<img>').attr('src', url).css("max-width", "900px");
            $('#summernote').summernote("insertNode", image[0]);
        },
        error: function(data) {
            alert(data);
        }
    });
}
```
이미지 하나만 잘 업로드 된다. 두개 첨부하면 두번째꺼는 base64로 들어감.

```python
BOARD_IMAGE_PATH = "C:\Users\cgkim449\study\images"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['BOARD_IMAGE_PATH'] = BOARD_IMAGE_PATH
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024 # 15메가

if not os.path.exists(app.config["BOARD_IMAGE_PATH"]): # 중요한건 아니지만 도커할때 일케하면 편함
    os.mkdir(app.config["BOARD_IMAGE_PATH"])
```

```python
from string import digits, ascii_uppercase, ascii_lowercase
import random

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS 

def rand_generator(length=8):
    chars = ascii_lowercase + ascii_uppercase + digits # 모든 문자가 chars에 담김!
    return ''.join(random.sample(chars, length)) # chars 전체에서 length만큼 뽑아낸다

@blueprint.route("/upload_image", methods=["POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = "{}_{}.jpg".format(str(int(datetime.now().timestamp()) * 1000), rand_generator())
            savefilepath = os.path.join(app.config["BOARD_IMAGE_PATH"], filename) # 절대경로 리턴
            file.save(savefilepath)
            return url_for("board.board_images", filename=filename)

from flask import send_from_directory

@blueprint.route('/images/<filename>')
def board_images(filename):
    return send_from_directory(app.config['BOARD_IMAGE_PATH'], filename) # 내가 만든 images 폴더가 프로젝트 폴더(flow)밖에 있기 때문에 send_from_directory를 써줘야한다! 인자는 절대경로랑 파일명!
```