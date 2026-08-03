#!/usr/bin/env python3
# 안내판(공개용) 구역명 기준으로 data.js 생성. 위치는 시공도면 그리드 좌표로 배치.
import json

KX = 53900 / (0.82 - 0.175)
KY = 30750 / (0.745 - 0.235)
def mx(f): return round((f - 0.175) * KX)
def my(f): return round((f - 0.235) * KY)
TEX = dict(x0=mx(0.15), x1=mx(0.83), y0=my(0.185), y1=my(0.755))

def R(name, eng, zone, fx0, fx1, fy0, fy1, round_=False, nowall=False, dome=False):
    return dict(name=name, eng=eng, zone=zone, round=round_, nowall=nowall, dome=dome,
                x0=mx(fx0), x1=mx(fx1), y0=my(fy0), y1=my(fy1))

# ── 2F : 사우나/락커 층 (피난안내도 기준) ──
F2 = [
    R("남성 사우나","Men's Sauna","msauna",0.155,0.315,0.24,0.575),
    R("여성 사우나","Women's Sauna","wsauna",0.66,0.83,0.40,0.68),
    R("리셉션","Reception","core",0.40,0.465,0.235,0.30,nowall=True),
    R("사무실","Office","service",0.465,0.51,0.235,0.30),
    R("기계실","Machine Room","service",0.58,0.66,0.285,0.40),
    R("실외기(외부)","Outdoor Unit","service",0.80,0.85,0.24,0.36),
    R("남성 회원 신발장","Men's Member Shoes","msauna",0.35,0.42,0.30,0.335),
    R("여성 회원 신발장","Women's Member Shoes","wsauna",0.47,0.53,0.30,0.335),
    R("남성 신발장","Men's Shoe Locker","msauna",0.35,0.44,0.335,0.42),
    R("여성 신발장","Women's Shoe Locker","wsauna",0.47,0.55,0.335,0.42),
    R("여성 휴게실","Women's Lounge","wsauna",0.52,0.60,0.45,0.52),
    R("엘리베이터","Elevator","core",0.35,0.53,0.44,0.60,nowall=True),
    R("비상계단","","stair",0.398,0.432,0.475,0.555),
    R("비상계단","","stair",0.498,0.532,0.475,0.555),
    R("남성 파우더룸","Men's Powder","msauna",0.16,0.245,0.605,0.70),
    R("남성 락커룸","Men's Locker","msauna",0.28,0.49,0.605,0.70),
    R("여성 락커룸","Women's Locker","wsauna",0.50,0.66,0.605,0.70),
    R("여성 파우더룸","Women's Powder","wsauna",0.72,0.83,0.62,0.70),
]

# ── 3F : 찜질 스파 (플로어 가이드 기준) ──
F3 = [
    R("불가마","Bulgama Sauna","theme",0.19,0.255,0.24,0.345,round_=True,dome=True),
    R("소금방","Salt Sauna","theme",0.265,0.345,0.28,0.375),
    R("미니 동굴","Mini Cave","theme",0.255,0.345,0.38,0.45),
    R("핀란드식 사우나","Finnish Sauna","theme",0.40,0.52,0.29,0.34),
    R("핀란드 가든","Finland Garden","garden",0.40,0.585,0.34,0.47,nowall=True),
    R("라운지","Lounge","amenity",0.155,0.30,0.45,0.64),
    R("안마기","Massage Chairs","amenity",0.36,0.44,0.47,0.55),
    R("아케이드존","Arcade Zone","amenity",0.36,0.50,0.55,0.62,nowall=True),
    R("비상계단","","stair",0.398,0.432,0.475,0.555),
    R("비상계단","","stair",0.498,0.532,0.475,0.555),
    R("키즈 놀이방","Kids Play Room","amenity",0.60,0.70,0.47,0.60),
    R("웰니스센터 피트니스","Wellness Fitness","amenity",0.70,0.795,0.36,0.62),
    R("플레이캠핑존","Play Camping Zone","amenity",0.795,0.85,0.36,0.62),
    R("스낵바","BLUE Snack","amenity",0.315,0.375,0.62,0.70),
    R("게르마늄 맥반석방","Elvan Stone Sauna","theme",0.40,0.47,0.62,0.70),
    R("아이스방","Ice Sauna","theme",0.47,0.515,0.62,0.70),
    R("피톤치드 편백방","Cypress Sauna","theme",0.515,0.585,0.62,0.70),
    R("푸드코트","Food Court","amenity",0.60,0.78,0.62,0.70),
    R("지압 테라피","Foot Massage","amenity",0.32,0.44,0.71,0.75),
    R("풋 스파","Foot Spa","amenity",0.44,0.55,0.71,0.75),
]

# ── 이동로(복도) 중심선: 구역 사이 빈 공간을 지나는 주 동선 [x0,y0,x1,y1] mm ──
def Cc(fx0,fy0,fx1,fy1): return [mx(fx0),my(fy0),mx(fx1),my(fy1)]
C2=[  # 2F
    Cc(0.16,0.435,0.83,0.435),  # 상부 동서 복도
    Cc(0.16,0.602,0.83,0.602),  # 하부 동서 복도
    Cc(0.44,0.30,0.44,0.60),    # 중앙 남북 스파인 (엘리베이터 아래 락커룸으로는 내려가지 않음)
    Cc(0.30,0.435,0.30,0.602),
    Cc(0.63,0.435,0.63,0.602),
]
C3=[  # 3F
    Cc(0.16,0.47,0.85,0.47),
    Cc(0.16,0.605,0.85,0.605),
    Cc(0.55,0.29,0.55,0.71),
    Cc(0.34,0.47,0.34,0.71),
    Cc(0.66,0.36,0.66,0.71),
]

data = dict(
    grid=dict(
        X={"X1":mx(0.175),"X2":mx(0.284),"X3":mx(0.3605),"X4":mx(0.4755),
           "X5":mx(0.590),"X6":mx(0.705),"X7":mx(0.82)},
        Y={"Y5":my(0.235),"Y4":my(0.288),"Y3":my(0.447),"Y2":my(0.607),"Y1":my(0.745)},
        spanX=53900, spanY=30750),
    tex=TEX,
    # 도면 실제 외곽 치수(공칭값). cum=X1/Y5 기준 누적 mm
    dims=dict(
        Xcum=[0,9100,15500,25100,34700,44300,53900],
        Xspan=[9100,6400,9600,9600,9600,9600], Xtotal=53900,
        Ycum=[0,3200,12800,22400,30750],
        Yspan=[3200,9600,9600,8350], Ytotal=30750),
    floors={
        "2F": dict(z=0, tex="assets/plan_2F.jpg", rooms=F2, corr=C2),
        "3F": dict(z=4200, tex="assets/plan_3F.jpg", rooms=F3, corr=C3),
    },
    # 2F↔3F 연결계단: 2F 남성사우나 벽면(신발장 앞) → 3F 소금방·핀란드식사우나 통로
    connectors=[ dict(x0=mx(0.30), y0=my(0.335), x1=mx(0.372), y1=my(0.315), w=2200) ],
)
with open("data.js","w",encoding="utf-8") as f:
    f.write("window.SPA_DATA = "); json.dump(data, f, ensure_ascii=False); f.write(";\n")
print("2F zones:",len(F2)," 3F zones:",len(F3))
