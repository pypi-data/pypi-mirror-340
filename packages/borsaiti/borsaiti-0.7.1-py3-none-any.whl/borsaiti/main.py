
import ssl
import certifi
import os
import time
import json
import random
import threading
import warnings
import soundcard as sc
import soundfile as sf
from mtranslate import translate
import ollama
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

try:
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
except:
    ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = "374giayfaud738q"
kullanici_key = None

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "data.json")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def set_api(key):
    global kullanici_key
    if key != API_KEY:
        raise ValueError("❌ Geçersiz API anahtarı!")
    kullanici_key = key
    print("✅ API key doğrulandı!")

def get_verification_code(email, client_id, refresh_token):
    print("📩 Hotmail hesabı kontrol ediliyor...")
    try:
        headers = {
            "Authorization": f"Bearer {refresh_token}"
        }
        url = "https://graph.microsoft.com/v1.0/me/messages?$orderby=receivedDateTime desc&$top=5"
        r = requests.get(url, headers=headers)
        items = r.json().get("value", [])
        for item in items:
            if "code" in item["subject"].lower():
                code = ''.join(filter(str.isdigit, item["subject"]))
                if len(code) >= 6:
                    return code[:6]
    except Exception as e:
        print(f"❌ Kod çekme hatası: {e}")
    return None

def baslat():
    global kullanici_key
    if kullanici_key != API_KEY:
        raise PermissionError("❌ API doğrulanmadı!")

    ayarlar = load_data()

    print("\n[1] Kişiselleştir")
    print("[2] Devam Et")
    secim = input("Seçim yap (1/2): ").strip()

    if secim == "1":
        ayarlar["refresh_token"] = input("🔁 Refresh token: ").strip()
        ayarlar["client_id"] = input("🧾 Client ID: ").strip()
        ayarlar["kick_email"] = input("📧 Kick mail: ").strip()
        ayarlar["kick_pass"] = input("🔑 Kick şifre: ").strip()
        save_data(ayarlar)
        print("✅ Bilgiler kaydedildi. Tekrar başlatın.")
        return

    profile_path = os.path.join(os.getcwd(), f"borsaiti_chrome_profile_{random.randint(1000,9999)}")
    os.makedirs(profile_path, exist_ok=True)
    options = uc.ChromeOptions()
    options.user_data_dir = profile_path
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"❌ Chrome başlatılamadı: {e}")
        return

    driver.get("https://kick.com")
    print("✅ Kick.com açıldı, giriş yapılıyor...")

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log In')]"))).click()
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(ayarlar["kick_email"])
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(ayarlar["kick_pass"])
        driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]").click()
        print("✅ Giriş bilgileri gönderildi.")

        time.sleep(5)
        if "code" in driver.page_source.lower():
            kod = get_verification_code(ayarlar["kick_email"], ayarlar["client_id"], ayarlar["refresh_token"])
            if kod:
                input_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @inputmode='numeric']"))
                )
                input_box.send_keys(kod)
                driver.find_element(By.XPATH, "//button").click()
                print("🔐 Kod girildi ve onaylandı.")
    except Exception as e:
        print(f"⚠️ Giriş sırasında hata: {e}")
        return

    chat_input_xpath = input("✏️ Sohbet kutusunun XPath'ini gir: ")
    send_button_xpath = input("📤 Gönderme butonunun XPath'ini gir: ")

    SAMPLE_RATE = 48000
    RECORD_SEC = 10
    use_file_index = 1
    system_prompt = {
        "role": "system",
        "content": (
            "You are an AI assistant in a Kick livestream. Speak in a short, natural, human way. "
            "Be very casual and realistic. Reply in 1 short sentence only. No robotic tone."
        )
    }
    chat_history = []
    follow_up_questions = [
        "Senin düşüncen ne bu konuda?",
        "Sence bu yayında ne eksik?",
        "Chat buna ne diyor?",
        "Sen olsan ne yapardın?",
        "Daha iyisi nasıl olurdu sence?"
    ]

    def build_prompt(user_input):
        chat_history.append({"role": "user", "content": user_input})
        return [system_prompt] + chat_history[-5:]

    def start_ai():
        nonlocal use_file_index
        while True:
            file_current = f"out{use_file_index}.wav"
            file_to_delete = f"out{(use_file_index % 3) + 1}.wav"
            print(f"🎧 Masaüstü sesi dinleniyor ({file_current})...")
            try:
                with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
                    data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
                    sf.write(file_current, data[:, 0], samplerate=SAMPLE_RATE)
                    time.sleep(0.2)
            except Exception as e:
                print(f"🎙️ Kayıt hatası: {e}")
                continue

            try:
                if os.path.exists(file_to_delete):
                    time.sleep(0.3)
                    os.remove(file_to_delete)
            except Exception as e:
                print(f"🗑️ Dosya silme hatası: {e}")

            try:
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                with sr.AudioFile(file_current) as source:
                    audio = recognizer.record(source)
                turkish_text = recognizer.recognize_google(audio, language="tr-TR")
                print("🧑 (Sen):", turkish_text)
            except Exception as e:
                print(f"❌ Ses tanıma hatası: {e}")
                use_file_index = (use_file_index % 3) + 1
                continue

            translated_text = translate(turkish_text, "en", "tr")
            prompt = build_prompt(translated_text)
            response = ollama.chat(model="gemma:2b", messages=prompt)
            english_reply = response["message"]["content"].strip().split(".")[0].strip() + "."
            translated_reply = translate(english_reply, "tr", "en")

            if random.random() < 0.1:
                translated_reply += " " + random.choice(follow_up_questions)

            delay = random.randint(15, 110)
            print(f"⌛ Cevap {delay} sn sonra geliyor...")
            time.sleep(delay)
            print("🤖 (AI):", translated_reply)
            chat_history.append({"role": "assistant", "content": english_reply})

            try:
                message_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, chat_input_xpath))
                )
                ActionChains(driver).move_to_element(message_input).click().send_keys(translated_reply).perform()
                send_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, send_button_xpath))
                )
                send_button.click()
                print("📤 Gönderildi!")
            except Exception as msg_err:
                print(f"❗ Mesaj gönderme hatası: {msg_err}")

            use_file_index = (use_file_index % 3) + 1

    print("🕒 AI sistemi 60 saniye sonra devreye girecek...")
    threading.Timer(60, start_ai).start()
