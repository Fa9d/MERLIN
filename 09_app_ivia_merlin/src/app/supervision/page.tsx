import Link from "next/link";

export default function SupervisionPage() {
  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="wordmark">MERLIN / Supervision</div>
        <nav className="nav">
          <Link href="/">Accueil</Link>
          <Link href="/operator">Operateur</Link>
          <Link href="/admin">Admin</Link>
        </nav>
      </header>

      <main className="section">
        <div className="section-header">
          <div className="eyebrow">SCR-201 a SCR-203</div>
          <h2>Supervision et validation V1</h2>
          <p>
            Cette couche est distincte de la production. Elle servira a relire
            les derives IA, valider les sorties sensibles et consulter l&apos;audit
            sans contaminer le dossier de production.
          </p>
        </div>

        <article className="card">
          <ul>
            <li>Validation des sorties IA critiques</li>
            <li>Consultation de l&apos;audit</li>
            <li>Pas d&apos;exposition de la couche research</li>
          </ul>
        </article>
      </main>
    </div>
  );
}
