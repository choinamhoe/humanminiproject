import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model

# --- 안개지수 계산 ---
def dew_point_celsius(Tc, RH):
    a = 17.27
    b = 237.7
    gamma = (a * Tc) / (b + Tc) + np.log(np.maximum(RH, 1) / 100.0)
    Td = (b * gamma) / (a - gamma)
    return Td

def compute_fog_index_row(T, RH, W, V):
    Td = dew_point_celsius(T, RH)
    delta = abs(T - Td)
    vis_score = np.clip((2000 - V) / 2000.0, 0, 1)
    rh_score = np.clip((RH - 70) / 30.0, 0, 1)
    wind_score = np.clip((2 - W) / 2.0, 0, 1)
    delta_score = np.clip((2 - delta) / 2.0, 0, 1)
    fog_raw = 100 * (0.4*vis_score + 0.3*rh_score + 0.2*delta_score + 0.1*wind_score)
    return float(np.clip(fog_raw, 0, 100))

# ---------------------------
# 합성 학습 데이터 생성
# ---------------------------
def generate_synthetic_training_data(n_samples=2000, seed=123):
    rng = np.random.default_rng(seed)
    T = 10 + 10*rng.normal(size=n_samples)  # 기온
    RH = np.clip(60 + 20*rng.normal(size=n_samples), 0, 100)  # 습도
    W = np.clip(3 + 2*rng.normal(size=n_samples), 0, 20)      # 풍속
    V = np.clip(10000 + 5000*rng.normal(size=n_samples), 0, 20000)  # 가시거리
    precip_prob = np.clip(5 + 40*rng.normal(size=n_samples), 0, 100)  # 강수 확률
    precipitation = np.clip(2 * rng.normal(size=n_samples), 0, 50)    # 강수량(mm)

    df = pd.DataFrame({
        "temperature": T,
        "humidity": RH,
        "wind_speed": W,
        "visibility": V,
        "precip_prob": precip_prob,
        "precipitation": precipitation
    })

    df["fog_index"] = df.apply(
        lambda r: compute_fog_index_row(r.temperature, r.humidity, r.wind_speed, r.visibility),
        axis=1
    )

    # playable 정의: 강수확률 <30, 강수량 <10mm, 풍속 <10, 안개지수 <40
    df["playable"] = df.apply(
        lambda r: 1 if (r.precip_prob < 30 and r.precipitation < 10 and r.wind_speed < 10 and r.fog_index < 40) else 0,
        axis=1
    )
    return df

# ---------------------------
# ML 학습 (RandomForest)
# ---------------------------
def train_ml_model(weather_df):
    features = ["temperature","humidity","wind_speed","visibility","precip_prob","precipitation","fog_index"]
    target = "playable"

    X = weather_df[features].values
    y = weather_df[target].values

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler().fit(Xtr)
    Xtr_s = scaler.transform(Xtr)

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(Xtr_s, ytr)

    joblib.dump(scaler, "scaler.joblib")
    joblib.dump(clf, "rf_playable.joblib")

    print("✅ ML 모델 학습 완료 — scaler.joblib, rf_playable.joblib 저장됨")
    return clf

# ---------------------------
# DL 학습 (Keras NN)
# ---------------------------
def train_deep_model(weather_df):
    features = ["temperature","humidity","wind_speed","visibility","precip_prob","precipitation","fog_index"]
    target = "playable"

    X = weather_df[features].values.astype(np.float32)
    y = weather_df[target].values.astype(np.float32)

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler().fit(Xtr)
    Xtr_s = scaler.transform(Xtr)
    Xte_s = scaler.transform(Xte)

    model = keras.Sequential([
        layers.Input(shape=(Xtr_s.shape[1],)),
        layers.Dense(64, activation="relu"),
        layers.Dense(32, activation="relu"),
        layers.Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    model.fit(Xtr_s, ytr, epochs=30, batch_size=16, validation_split=0.2, verbose=1)

    model.save("deep_playable.h5")
    joblib.dump(scaler, "scaler_dl.joblib")

    print("✅ DL 모델 학습 완료 — deep_playable.h5, scaler_dl.joblib 저장됨")
    return model

def compute_fog_index_playable_rule(df):
    """
    골프장 단기 예보 DataFrame을 받아서:
    1) 안개 지수 계산
    2) Rule 기반 playable 계산
    3) ML/DL 예측
    4) 최종 playable 결정
    5) summary 생성
    """

    # --- 안개지수 계산 ---
    df["fog_index"] = df.apply(
        lambda r: compute_fog_index_row(r.temperature, r.humidity, r.wind_speed, r.visibility),
        axis=1
    )

    # --- 가시거리 추정 ---
    # 안개지수(fog_index)와 강수량(precipitation) 기반으로 visibility 계산
    # 안개 많고 강수량 많을수록 visibility 감소
    if "precipitation" not in df.columns:
        df["precipitation"] = 0.0
    df["visibility"] = 10000 - (df["fog_index"] * 50) - (df["precipitation"] * 100)
    df["visibility"] = df["visibility"].clip(lower=500)  # 최소 500m

    # --- rule 기반 골프 가능 여부 ---
    # 💡 강수량도 포함 (예: precipitation < 10mm)
    df["playable_rule"] = df.apply(
        lambda r: 1 if (r.precip_prob < 30 and r.precipitation < 10 and r.wind_speed < 10 and r.fog_index < 40) else 0,
        axis=1
    )

    # --- ML/DL 예측용 feature 리스트 ---
    features = ["temperature", "humidity", "wind_speed", "visibility", "precip_prob", "precipitation", "fog_index"]

    # 💡 예측용 df에 precipitation 컬럼이 없으면 0으로 생성
    if "precipitation" not in df.columns:
        df["precipitation"] = 0.0

    # --- ML 예측 ---
    try:
        scaler = joblib.load("scaler.joblib")
        clf = joblib.load("rf_playable.joblib")

        # 디버깅용 출력
        print("ML scaler features:", len(scaler.mean_))
        print("df features:", df[features].shape)

        # feature mismatch 방지
        Xs = df[features].values
        if Xs.shape[1] != len(scaler.mean_):
            raise ValueError(f"Feature mismatch: df has {Xs.shape[1]} features, scaler expects {len(scaler.mean_)}")

        # ML 예측
        Xs_s = scaler.transform(Xs)
        df["playable_prob_ml"] = clf.predict_proba(Xs_s)[:, 1]
        df["playable_ml"] = (df["playable_prob_ml"] >= 0.5).astype(int)
    except Exception as e:
        print("ML 예측 에러:", e)
        df["playable_prob_ml"] = np.nan
        df["playable_ml"] = np.nan

    # --- DL 예측 ---
    try:
        dl_scaler = joblib.load("scaler_dl.joblib")
        dl_model = load_model("deep_playable.h5", compile=False)

        Xdl = df[features].values
        if Xdl.shape[1] != len(dl_scaler.mean_):
            raise ValueError(f"DL feature mismatch: df has {Xdl.shape[1]} features, scaler expects {len(dl_scaler.mean_)}")

        Xdl_s = dl_scaler.transform(Xdl)
        df["playable_prob_dl"] = dl_model.predict(Xdl_s).reshape(-1)
        df["playable_dl"] = (df["playable_prob_dl"] >= 0.5).astype(int)
    except Exception as e:
        print("DL 예측 에러:", e)
        df["playable_prob_dl"] = np.nan
        df["playable_dl"] = np.nan

    # --- 최종 골프 가능 여부 결정 ---
    # rule OR ML OR DL 예측 결과를 사용
    df["final_playable"] = df.apply(
        lambda r: int(bool(r.playable_rule) or bool(r.playable_ml) or bool(r.playable_dl)),
        axis=1
    )

    # --- summary 생성 ---
    summary = []
    for _, r in df.iterrows():
        tstr = r.time.strftime("%Y-%m-%d %H:%M:%S")

        # 멘트 조합
        comments = [
            get_temp_comment(r.temperature),
            get_humidity_comment(r.humidity),
            get_wind_comment(r.wind_speed),
            get_precip_prob_comment(r.precip_prob),
            get_precip_amount_comment(r.precipitation),
            get_visibility_comment(r.visibility)
        ]
        comments = [c for c in comments if c]  # 빈 문자열 제거
        comment_str = " ".join(comments)

        # 최종 요약 문구 (HTML 줄바꿈 적용)
        txt = (
            f"{tstr} — 기온 {r.temperature:.1f}°C, "
            f"습도 {r.humidity:.0f}%, "
            f"풍속 {r.wind_speed:.1f}m/s, "
            f"강수량 {r.precipitation:.1f}mm, "
            f"가시거리 {r.visibility:.0f}m, "
            f"안개지수 {r.fog_index:.1f} "
            f"→ 골프장: {'가능' if r.final_playable==1 else '불가'} "
            f"(ML:{r.playable_prob_ml:.2f}, DL:{r.playable_prob_dl:.2f})"
            "\n"
            f"👉 {comment_str}"
        )
        txt = txt.replace("\n", "<br>")
        summary.append(txt)

    df["summary"] = summary
    df = df.reset_index(drop=True)

    # --- 최종 반환 DataFrame df ---
    # df 컬럼 설명:
    # time              : datetime -> 예측 시간 (한국 시간, tz=Asia/Seoul)
    # temperature       : float    -> 기온(℃)
    # humidity          : float    -> 상대습도(%)
    # wind_speed        : float    -> 풍속(m/s)
    # visibility        : float    -> 가시거리(m), 기본 10000m
    # precip_prob       : float    -> 강수 확률(%), 초단기예보에는 0.0
    # precipitation     : float    -> 1시간 강수량(mm), RN1 기준
    # precip_type       : int      -> 강수 형태, PTY 기준 (0=없음, 1=비, 2=비/눈, 3=눈, 4=소나기)
    # fog_index         : float    -> 안개 지수(0~100, 높을수록 안개 심함)
    # playable_rule     : int      -> Rule 기반 골프 가능 여부 (0=불가, 1=가능)
    # playable_prob_ml  : float    -> ML(RandomForest) 예측 확률(0~1)
    # playable_ml       : int      -> ML(RandomForest) 예측 결과 (0=불가, 1=가능)
    # playable_prob_dl  : float    -> DL(NeuralNetwork) 예측 확률(0~1)
    # playable_dl       : int      -> DL(NeuralNetwork) 예측 결과 (0=불가, 1=가능)
    # final_playable    : int      -> 최종 골프 가능 여부 (0=불가, 1=가능), playable_rule OR playable_ml
    # summary           : str      -> 사람이 읽기 좋은 요약 문자열 (HTML 줄바꿈 <br> 적용)
    # 예시:
    # "2025-09-16 14:00:00 — 기온 26.0°C, 습도 85%, 풍속 2.0m/s, 강수량 7.0mm, 안개지수 12.0 → 골프장: 불가 (ML:0.12, DL:0.05)<br>👉 기온 적당, 바람 약함, 강수 주의"
    return df

# --- 조건별 멘트 함수 정의 ---
def get_temp_comment(t):
    if 18 <= t <= 27:
        return "쾌적한 날씨로 라운딩하기 좋습니다."
    elif 10 <= t <= 17:
        return "약간 선선합니다. 얇은 외투가 필요할 수 있습니다."
    elif 28 <= t <= 32:
        return "다소 더운 날씨, 수분 보충에 신경 쓰세요."
    elif t < 10:
        return "추운 날씨, 방한 준비가 필요합니다."
    elif t > 32:
        return "무더위 주의! 라운딩 시 열사병 예방에 주의하세요."
    return ""

def get_humidity_comment(h):
    if 40 <= h <= 70:
        return "쾌적한 습도로 플레이하기 좋습니다."
    elif 71 <= h <= 85:
        return "습도가 높아 후텁지근할 수 있습니다."
    elif h > 85:
        return "습도가 매우 높아 불쾌지수가 큽니다. 수분 보충 필요합니다."
    return ""

def get_wind_comment(w):
    if 0 <= w <= 2:
        return "바람이 거의 없어 안정적인 플레이가 가능합니다."
    elif 3 <= w <= 5:
        return "약간의 바람이 있어 클럽 선택에 참고하세요."
    elif 6 <= w <= 9:
        return "강한 바람으로 공 방향에 영향이 있습니다. 주의하세요."
    elif w >= 10:
        return "매우 강한 바람, 안전에 유의하세요."
    return ""

def get_precip_prob_comment(p):
    if p < 20:
        return "비 예보는 거의 없어 안심하고 플레이하세요."
    elif 20 <= p <= 50:
        return "소나기 가능성이 있습니다. 대비가 필요합니다."
    elif p > 50:
        return "비가 올 가능성이 큽니다. 우산을 준비하세요."
    return ""

def get_precip_amount_comment(mm):
    if mm == 0:
        return "비가 내리지 않아 쾌적합니다."
    elif 0 < mm <= 2:
        return "약한 비가 올 수 있어 레인커버를 준비하세요."
    elif 2 < mm <= 5:
        return "비가 이어질 수 있으니 플레이에 유의하세요."
    elif mm > 5:
        return "라운딩이 어려울 수 있습니다. 취소 고려 필요합니다."
    return ""

def get_visibility_comment(v):
    if v > 5000:
        return "시야가 좋아 플레이에 문제 없습니다."
    elif 2000 <= v <= 5000:
        return "안개로 인해 시야가 다소 흐립니다."
    elif v < 2000:
        return "안개가 짙어 시야 확보가 어렵습니다. 주의하세요."
    return ""




