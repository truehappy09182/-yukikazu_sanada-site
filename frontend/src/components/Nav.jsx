const links = [
  { to: "#about", label: "自己紹介" },
  { to: "#products", label: "商品紹介" },
  { to: "#achievements", label: "実績" },
  { to: "#contact", label: "お問い合わせ" },
];

export default function Nav() {
  return (
    <header className="nav">
      <a href="#about" className="nav-brand">
        真田ユキカズ<span className="nav-brand-sub">English Lessons</span>
      </a>
      <nav>
        {links.map((link) => (
          <a key={link.to} href={link.to}>
            {link.label}
          </a>
        ))}
      </nav>
    </header>
  );
}
