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

# --- 합성 학습 데이터 ---
def generate_synthetic_training_data(n_samples=2000, seed=123):
    rng = np.random.default_rng(seed)
    T = 10 + 10*rng.normal(size=n_samples)
    RH = np.clip(60 + 20*rng.normal(size=n_samples), 0, 100)
    W = np.clip(3 + 2*rng.normal(size=n_samples), 0, 20)
    V = np.clip(10000 + 5000*rng.normal(size=n_samples), 0, 20000)
    precip_prob = np.clip(5 + 40*rng.normal(size=n_samples), 0, 100)
    df = pd.DataFrame({
        "temperature": T,
        "humidity": RH,
        "wind_speed": W,
        "visibility": V,
        "precip_prob": precip_prob
    })
    df["fog_index"] = df.apply(
        lambda r: compute_fog_index_row(r.temperature, r.humidity, r.wind_speed, r.visibility),
        axis=1
    )
    df["playable"] = df.apply(
        lambda r: 1 if (r.precip_prob < 30 and r.wind_speed < 10 and r.fog_index < 40) else 0,
        axis=1
    )
    return df

# --- ML 학습 ---
def train_ml_model(weather_df):
    features = ["temperature","humidity","wind_speed","visibility","precip_prob","fog_index"]
    target = "playable"

    X = weather_df[features].values
    y = weather_df[target].values

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler().fit(Xtr)
    Xtr_s = scaler.transform(Xtr)
    Xte_s = scaler.transform(Xte)

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(Xtr_s, ytr)

    joblib.dump(scaler, "scaler.joblib")
    joblib.dump(clf, "rf_playable.joblib")
    return clf

# --- DL 학습 ---
def train_deep_model(weather_df):
    features = ["temperature","humidity","wind_speed","visibility","precip_prob","fog_index"]
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
    return model

def compute_fog_index_playable_rule(df):
    #print(f"compute_fog_index_playable_rule start df : {df}")
    # --- 안개지수 계산 ---
    df["fog_index"] = df.apply(
        lambda r: compute_fog_index_row(r.temperature, r.humidity, r.wind_speed, r.visibility),
        axis=1
    )
    #print(f"compute_fog_index_playable_rule after compute_fog_index_row df : {df}")
    # --- rule 기반 골프 가능 여부 ---
    df["playable_rule"] = df.apply(
        lambda r: 1 if (r.precip_prob<30 and r.wind_speed<10 and r.fog_index<40) else 0,
        axis=1
    )
    #print(f"compute_fog_index_playable_rule after playable_rule df : {df["playable_rule"]}")
    features = ["temperature","humidity","wind_speed","visibility","precip_prob","fog_index"]

    # --- ML 예측 ---
    try:
        scaler = joblib.load("scaler.joblib")
        clf = joblib.load("rf_playable.joblib")
        Xs = scaler.transform(df[features].values)
        df["playable_prob_ml"] = clf.predict_proba(Xs)[:,1]  # ML 예측 확률 (0~1)
        df["playable_ml"] = (df["playable_prob_ml"]>=0.5).astype(int)  # ML 예측 결과 (0=불가,1=가능)
    except:
        df["playable_prob_ml"] = np.nan
        df["playable_ml"] = np.nan
    #print(f"compute_fog_index_playable_rule after ML 예측 df : {df}")
    # --- DL 예측 ---
    try:
        dl_scaler = joblib.load("scaler_dl.joblib")
        dl_model = load_model("deep_playable.h5", compile=False)
        Xdl = dl_scaler.transform(df[features].values)
        df["playable_prob_dl"] = dl_model.predict(Xdl).reshape(-1)  # DL 예측 확률 (0~1)
        df["playable_dl"] = (df["playable_prob_dl"]>=0.5).astype(int)  # DL 예측 결과 (0=불가,1=가능)
    except:
        df["playable_prob_dl"] = np.nan
        df["playable_dl"] = np.nan
    
    #print(f"compute_fog_index_playable_rule after DL 예측 df : {df}")
    # --- 최종 골프 가능 여부 결정 ---
    df["final_playable"] = df.apply(
        lambda r: int(bool(r.playable_rule) or bool(r.playable_ml)),
        axis=1
    )

    #print(f"compute_fog_index_playable_rule after 최종 골프 가능 여부 결정 df : {df}")

    # --- summary 문자열 생성 ---
    summary = []
    for _, r in df.iterrows():
        tstr = r.time.strftime("%Y-%m-%d %H:%M:%S")
        txt = f"{tstr} — 기온 {r.temperature:.1f}°C, 습도 {r.humidity:.0f}%, 풍속 {r.wind_speed:.1f}m/s, 안개지수 {r.fog_index:.1f} → 골프장: {'가능' if r.final_playable==1 else '불가'} (ML:{r.playable_prob_ml:.2f})"
        summary.append(txt)
    
    df["summary"] = summary
    #print(f"compute_fog_index_playable_rule after summary 문자열 summary : {summary}")
    df = df.reset_index(drop=True)

    # --- 반환값 컬럼 설명 ---
    """
    df (DataFrame) 컬럼:
        id                : int   -> 순번 (1부터 시작)
        time              : datetime -> 예측 시간 (한국 시간, tz=Asia/Seoul)
        temperature       : float -> 기온(℃)
        humidity          : float -> 상대습도(%)
        wind_speed        : float -> 풍속(m/s)
        visibility        : float -> 가시거리(m), 기본 10000m
        precip_prob       : float -> 강수 확률(%)
        fog_index         : float -> 안개 지수(0~100, 높을수록 안개 심함)
        playable_rule     : int   -> Rule 기반 골프 가능 여부 (0=불가,1=가능)
        playable_prob_ml  : float -> ML(RandomForest) 예측 확률(0~1)
        playable_ml       : int   -> ML(RandomForest) 예측 결과 (0=불가,1=가능)
        playable_prob_dl  : float -> DL(NeuralNetwork) 예측 확률(0~1)
        playable_dl       : int   -> DL(NeuralNetwork) 예측 결과 (0=불가,1=가능)
        final_playable    : int   -> 최종 골프 가능 여부 (0=불가,1=가능), playable_rule OR playable_ml

    summary (list of str):
        각 시간별 날씨 정보 및 골프 가능 여부를 사람이 읽기 좋은 문자열 형태
        예시:
        "2025-09-13 14:00:00 — 기온 25.0°C, 습도 65%, 풍속 4.0m/s, 안개지수 12.0 → 골프장: 가능 (ML:0.92)"
    """
    return df