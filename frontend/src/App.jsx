import Nav from "./components/Nav.jsx";
import About from "./sections/About.jsx";
import Products from "./sections/Products.jsx";
import Achievements from "./sections/Achievements.jsx";
import Contact from "./sections/Contact.jsx";
import "./App.css";

export default function App() {
  return (
    <div className="app">
      <Nav />
      <main>
        <About />
        <Products />
        <Achievements />
        <Contact />
      </main>
      <footer className="footer">
        <p>&copy; 2026 真田ユキカズ English Lessons. All rights reserved.</p>
      </footer>
    </div>
  );
}
