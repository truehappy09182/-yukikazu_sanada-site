import { useState } from "react";
import { apiUrl } from "../api.js";

const initialForm = { name: "", email: "", message: "" };

export default function Contact() {
  const [form, setForm] = useState(initialForm);
  const [status, setStatus] = useState(null); // "sending" | "sent" | "error"

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("sending");
    try {
      const res = await fetch(apiUrl("/api/contact"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error("送信に失敗しました。");
      setStatus("sent");
      setForm(initialForm);
    } catch {
      setStatus("error");
    }
  };

  return (
    <section id="contact" className="section">
      <div className="section-inner">
        <p className="eyebrow">お問い合わせ</p>
        <h2 className="section-title">お問い合わせ</h2>
        <form className="contact-form" onSubmit={handleSubmit}>
          <label>
            お名前
            <input type="text" name="name" value={form.name} onChange={handleChange} required />
          </label>
          <label>
            メールアドレス
            <input type="email" name="email" value={form.email} onChange={handleChange} required />
          </label>
          <label>
            メッセージ
            <textarea name="message" rows="6" value={form.message} onChange={handleChange} required />
          </label>
          <button type="submit" disabled={status === "sending"}>
            {status === "sending" ? "送信中..." : "送信する"}
          </button>
          {status === "sent" && <p className="success">お問い合わせありがとうございます。</p>}
          {status === "error" && <p className="error">送信に失敗しました。もう一度お試しください。</p>}
        </form>
      </div>
    </section>
  );
}
