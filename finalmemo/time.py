from datetime import datetime
import time

current_utc_time = round(datetime.utcnow().timestamp() * 1000)
"""
게시물 작성 시간을 DB넣을 때는 이후에 상황에 맞게 가공하기 쉬운 형태로 넣는 것이 좋다.
따라서, timestamp()를 이용해 타임스탬프형식으로 넣는 것이 좋다.

datetime.utcnow()는 현재의 utc시간을 반환한다. 
datetime.utcnow().timestamp()는 초를 반환하므로 
이를 밀리초단위로 변환해주기 위해 1000을 곱하고 
소숫점을 없애기 위해 round()를 사용했다.

'db에 current_utc_time을 저장하자'
"""
value = current_utc_time
now_timestamp = time.time()
offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
value = datetime.fromtimestamp(int(value / 1000)) + offset # 1000을 나누는 이유는 밀리초를 다시 초로 변환하기 위함
print(value.strftime('%Y-%m-%d %H:%M:%S')) # 2022-01-25 18:59:45

"""
strftime()을 이용해 시간 정보 객체를 원하는 양식으로 양식화 한다.
참고: https://python.bakyeono.net/chapter-11-3.html#1133-%EC%8B%9C%EA%B0%84-%EC%A0%95%EB%B3%B4%EB%A5%BC-%EB%AC%B8%EC%9E%90%EC%97%B4%EB%A1%9C-%EB%82%98%ED%83%80%EB%82%B4%EA%B8%B0
"""