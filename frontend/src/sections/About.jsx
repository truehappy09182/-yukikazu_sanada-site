import { useEffect, useState } from "react";
import { apiUrl } from "../api.js";

export default function About() {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(apiUrl("/api/profile"))
      .then((res) => res.json())
      .then(setProfile)
      .catch(() => setError("プロフィールの取得に失敗しました。"));
  }, []);

  return (
    <section id="about" className="section hero-section">
      <div className="section-inner">
        {error && <p className="error">{error}</p>}
        {!profile && !error && <p>読み込み中...</p>}
        {profile && (
          <div className="profile-card">
            <img src={profile.photo_url} alt={profile.name} className="profile-photo" />
            <div className="profile-body">
              <p className="eyebrow">自己紹介</p>
              <h1>{profile.name}</h1>
              <p className="catchphrase">{profile.catchphrase}</p>
              <p className="bio">{profile.bio}</p>
              {profile.qualifications?.length > 0 && (
                <p className="qualifications">
                  資格
                  <br />
                  {profile.qualifications.join("、")}
                </p>
              )}
              <a href="#contact" className="cta-button">
                お問い合わせ
              </a>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
