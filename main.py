import socketio # 서버 연결 도구 가져오기
import asyncio # 알 필요 없는 것
from pydobot import Dobot # 도봇 연결 도구 가져오기

sio = socketio.AsyncClient() # 서버 연결 도구 변수로 생성

def getCon():
    x, y, z, r, j1, j2, j3, j4 = device.pose()
    return [x,y,z]

def convert_position(x, y):
    # x와 y에 대해 180도 회전된 선형 변환 공식 적용
    real_x = max_x - (x * (max_x - (min_x)) / 19)
    real_y = max_y - (y * (max_y - min_y) / 19)
    return real_x, real_y


###중요!!!
# 포트가 바뀔수있어서 그때 확인해줘야함
device = Dobot(port="COM4") # 도봇을 연결해서 변수로 생성

max_x, min_x, max_y, min_y = [70, -60, 360, 230]
# while True:
#     device.move_to(min_x, min_y, 49, 0, wait=True) # 다시 돌아가기, 100 은 높이
#     device.move_to(min_x, max_y, 49, 0, wait=True) # 다시 돌아가기, 100 은 높이
#     device.move_to(max_x, max_y, 49, 0, wait=True) # 다시 돌아가기, 100 은 높이
#     device.move_to(max_x, min_y, 49, 0, wait=True) # 다시 돌아가기, 100 은 높이

# while True:
#     for i in range(0, 19):
#         device.move_to(
#             convert_position(0, i)[0],
#             convert_position(0,i)[1],
#             100,0, True
#         )
#     for j in range(0, 19):
#         device.move_to(
#             convert_position(j, 0)[0],
#             convert_position(j,0)[1],
#             100,0, True
#         )
device.move_to(0, 200, 108, 0, wait=True) # 다시 돌아가기, 100 은 높이

# 서버에서 로봇팔을 움직이기 위해 보내는 함수
@sio.on('set_pos')
async def on_pos(data):
    # TODO : 도봇 움직이기
    x, y = data # 데이터에서 x y 가져오기
    real_x, real_y = convert_position(x, y) # 실제 로봇팔이 가야할 위치 계산하기
    print(data)
    print(x,y)
    print(real_x, real_y)
    device.move_to(real_x, real_y, 108, 0 ,wait=True) # 도봇 움직이기, 50은 높이
    device.move_to(real_x, real_y, 93, 0) # 도봇 움직이기, 50은 높이
    device.move_to(real_x, real_y, 108, 0 ,wait=True) # 도봇 움직이기, 50은 높이
    device.move_to(0, 200, 108, 0, wait=True) # 다시 돌아가기, 100 은 높이

######## 아래부터 볼 필요 없는 구간들

# 서버 연결시 실행되는 함수
@sio.event
async def connect():
    print("서버에 정상적으로 연결되었습니다.")

# 서버에 연결하고 대기하는 메인 함수
async def main():
    await sio.connect('http://thinkode.kr:3000')
    await sio.wait()

asyncio.run(main())
device.close()
