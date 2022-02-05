# fileupload
```html
<form name="form" method="POST" action="{{url_for('board.board_write')}}" onsubmit="return CheckWriteForm();" enctype="multipart/form-data">
...
<div class="custom-file">
        <input type="file" class="custom-file-input" id="customFile" name="attachfile">
        <label class="custom-file-label" for="customFile">파일선택</label>
    </div>
```
enctype 중요.  

```python
@blueprint.route("/write", methods=["GET", "POST"])
@login_required
def board_write():
    if session["id"] is None or session["id"] == "":
        return redirect(url_for("member_login"))

    if request.method == "POST":
        filename = None
        if "attachfile" in request.files:
            file = request.files["attachfile"]
            """
            이렇게 할수있다. 근데 파일명이 굉장히 중요하다.
            플라스크 공식 문서를 보면 secure_filename()을 쓰라고 권고하고 있다.
            https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
            secure_filename() 이걸 왜사용해야되는지 나옴.

            근데 문제는 secure_filename()가 아스키 코드로 변환함 그래서 우리가 함수로 만들자
            """
            if file and allowed_file(file.filename):
                filename = check_filename(file.filename)
                file.save(os.path.join(app.config["BOARD_ATTACH_FILE_PATH"], filename))

        name = request.form.get("name")
        writer_id = session.get("id")
        title = request.form.get("title")
        contents = request.form.get("contents")

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        board = mongo.db.board

        post = {
            "writer_id": writer_id,
            "name": session["name"],
            "title": title,
            "contents": contents,
            "view": 0,
            "pubdate": current_utc_time,
        }

        if filename is not None:
            post["attachfile"] = filename

        print(post)
        x = board.insert_one(post)

        flash("정상적으로 작성 되었습니다.")
        return redirect(url_for("board.board_view", idx=x.inserted_id))
    else:
        return render_template("write.html", title="글작성", name=session["name"])


```
함수를 우리가 만들자
```python 
import re # 정규식 쓸라고
import os

def check_filename(filename):
    reg = re.compile(r'[^A-Za-z0-9_.가-힝-]')
    for sep in os.path.sep, os.path.altsep: # os.path.sep는 \\ 이고, os.path.altsep는 / 이다.
        if sep:
            filename = filename.replace(sep, ' ')
            print(filename)
            filename = str(reg.sub('', '_'.join(filename.split()))).strip('._')
    return filename
```