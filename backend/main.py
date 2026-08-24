import json
import os
import socket
import urllib.error
import urllib.request

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

load_dotenv()

# RenderのランタイムはIPv6での外部接続に対応していないため、
# 名前解決をIPv4のみに強制する（未対応のままだと ENETUNREACH で失敗する）
_original_getaddrinfo = socket.getaddrinfo


def _getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
    return _original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)


socket.getaddrinfo = _getaddrinfo_ipv4_only

app = FastAPI(title="English Teacher Site API")

_extra_origins = [
    origin.strip()
    for origin in os.environ.get("FRONTEND_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", *_extra_origins],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Profile(BaseModel):
    name: str
    catchphrase: str
    bio: str
    photo_url: str
    qualifications: list[str] = []


class Product(BaseModel):
    id: int
    platform: str  # "coconala" | "note"
    title: str
    description: str
    price: str
    url: str | None = None


class PlatformInfo(BaseModel):
    key: str
    name: str
    description: str
    url: str


class Achievement(BaseModel):
    id: int
    title: str
    description: str
    year: str
    image_url: str | None = None


class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str


PROFILE = Profile(
    name="真田 ユキカズ",
    catchphrase="偏差値46からTOEIC800点へ。失敗経験を武器にする英語講師",
    bio=(
        "学生時代は英語が大の苦手で、偏差値46。TOEICのスコアも伸び悩み、"
        "30万円のコーチングを受けても思うような結果は出ませんでした。"
        "それでも学習法を根本から見直し、2年でTOEIC800点を達成。"
        "「自分と同じように英語学習で苦労する人をなくしたい」という思いを胸に、"
        "現在は英語講師 兼 コーチとして、自身の失敗経験を活かした指導を行っています。"
    ),
    photo_url="/profile.jpg",
    qualifications=["TOEIC805"],
)

PLATFORMS = [
    PlatformInfo(
        key="coconala",
        name="ココナラ",
        description="マンツーマン・グループレッスンなど、対面型のサービスはココナラで提供しています。",
        url="https://coconala.com/",
    ),
    PlatformInfo(
        key="note",
        name="note",
        description="学習ロードマップや教材はnoteで販売しています。",
        url="https://note.com/",
    ),
]

PRODUCTS = [
    Product(
        id=1,
        platform="coconala",
        title="700の壁突破へ！TOEICコーチングします",
        description="TOEIC300〜700点台の方向けのビデオチャットコーチング。自分に合った学習法の発見やスコアアップをサポートします。",
        price="¥1,000 / 30分",
        url="https://coconala.com/services/3201320",
    ),
    Product(
        id=2,
        platform="coconala",
        title="プロ英語講師が英検をレッスンします",
        description="英検5級〜準2級の過去問対策を個別指導。顔出し不要のビデオチャットで、独学者やお子さんの学習支援にも対応します。",
        price="¥1,500 / 50分",
        url="https://coconala.com/services/3873689",
    ),
    Product(id=3, platform="note", title="TOEIC800点までの学習ロードマップ", description="偏差値46から2年でTOEIC800点を達成した学習法をまとめた教材です。", price="¥980", url="https://note.com/truehappy/n/nb9f95e54de34"),
]

ACHIEVEMENTS = [
    Achievement(
        id=1,
        title="TOEIC 550点 → 620点達成(Y様)",
        description=(
            "「ご紹介いただいたTOEICアプリと、学習方法に関する細やかなアドバイスのおかげで、"
            "スコアを550点から620点まで伸ばすことができました。サポートいただき大変感謝しています。"
            "今後もさらなるスコアアップを目指して頑張ります。」"
        ),
        year="2026",
        image_url="/achievement-1.jpg",
    ),
]

CONTACT_MESSAGES: list[ContactMessage] = []

CONTACT_NOTIFY_EMAIL = os.environ.get("CONTACT_NOTIFY_EMAIL", "truehappy09182@gmail.com")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
RESEND_FROM_EMAIL = os.environ.get("RESEND_FROM_EMAIL", "onboarding@resend.dev")


def send_contact_notification(message: ContactMessage) -> None:
    if not RESEND_API_KEY:
        print(
            "RESEND_API_KEY が未設定のため、お問い合わせ通知メールの送信をスキップしました。"
            " backend/.env を設定してください。"
        )
        return

    payload = json.dumps(
        {
            "from": f"English Teacher Site <{RESEND_FROM_EMAIL}>",
            "to": [CONTACT_NOTIFY_EMAIL],
            "reply_to": message.email,
            "subject": f"【サイトお問い合わせ】{message.name} 様より",
            "text": (
                f"お名前: {message.name}\n"
                f"メールアドレス: {message.email}\n\n"
                f"メッセージ:\n{message.message}\n"
            ),
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; english-teacher-site/1.0)",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as res:
        if res.status >= 300:
            raise RuntimeError(f"Resend API error: {res.status}")


@app.get("/api/profile", response_model=Profile)
def get_profile():
    return PROFILE


@app.get("/api/products", response_model=list[Product])
def get_products():
    return PRODUCTS


@app.get("/api/platforms", response_model=list[PlatformInfo])
def get_platforms():
    return PLATFORMS


@app.get("/api/achievements", response_model=list[Achievement])
def get_achievements():
    return ACHIEVEMENTS


@app.post("/api/contact", status_code=201)
def post_contact(message: ContactMessage):
    if not message.message.strip():
        raise HTTPException(status_code=400, detail="メッセージを入力してください。")
    CONTACT_MESSAGES.append(message)
    try:
        send_contact_notification(message)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"お問い合わせ通知メールの送信に失敗しました: {exc} - {detail}")
    except Exception as exc:
        print(f"お問い合わせ通知メールの送信に失敗しました: {exc}")
    return {"ok": True}
