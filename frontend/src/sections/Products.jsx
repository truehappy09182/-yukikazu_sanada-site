import { useEffect, useState } from "react";
import { apiUrl } from "../api.js";

export default function Products() {
  const [products, setProducts] = useState([]);
  const [platforms, setPlatforms] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      fetch(apiUrl("/api/products")).then((res) => res.json()),
      fetch(apiUrl("/api/platforms")).then((res) => res.json()),
    ])
      .then(([productsData, platformsData]) => {
        setProducts(productsData);
        setPlatforms(platformsData);
      })
      .catch(() => setError("商品情報の取得に失敗しました。"));
  }, []);

  return (
    <section id="products" className="section">
      <div className="section-inner">
        <p className="eyebrow">商品紹介</p>
        <h2 className="section-title">レッスンメニュー</h2>
        {error && <p className="error">{error}</p>}
        <div className="platform-groups">
          {platforms.map((platform) => (
            <div key={platform.key} className="platform-group">
              <div className="platform-header">
                <div>
                  <h3 className="platform-name">{platform.name}</h3>
                  <p className="platform-description">{platform.description}</p>
                </div>
              </div>
              <div className="card-grid">
                {products
                  .filter((product) => product.platform === platform.key)
                  .map((product) => (
                    <div key={product.id} className="card">
                      <h4>{product.title}</h4>
                      <p>{product.description}</p>
                      <p className="price">{product.price}</p>
                      {product.url && (
                        <a href={product.url} target="_blank" rel="noreferrer" className="card-link">
                          詳細を見る →
                        </a>
                      )}
                    </div>
                  ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
