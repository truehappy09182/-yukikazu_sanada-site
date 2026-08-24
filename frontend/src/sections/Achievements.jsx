import { useEffect, useState } from "react";
import { apiUrl } from "../api.js";

export default function Achievements() {
  const [achievements, setAchievements] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(apiUrl("/api/achievements"))
      .then((res) => res.json())
      .then(setAchievements)
      .catch(() => setError("実績情報の取得に失敗しました。"));
  }, []);

  return (
    <section id="achievements" className="section section-alt">
      <div className="section-inner">
        <p className="eyebrow">実績</p>
        <h2 className="section-title">これまでの実績</h2>
        {error && <p className="error">{error}</p>}
        <ul className="achievement-list">
          {achievements.map((item) => (
            <li key={item.id}>
              <span className="year">{item.year}</span>
              <div>
                <h3>{item.title}</h3>
                <p>{item.description}</p>
                {item.image_url && (
                  <img
                    className="achievement-image"
                    src={item.image_url}
                    alt={item.title}
                  />
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
