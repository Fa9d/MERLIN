import "./styles.css";

export default function HomePage() {
  return (
    <div className="home-page">
      <div className="home-shell">
        <header className="home-topbar">
          <a className="home-brand" href="/">
            IVIA
          </a>
          <nav className="home-nav">
            <a href="/#pour-qui">Pour qui</a>
            <a href="/#comment">Comment ça fonctionne</a>
            <a href="/#tarifs">Tarifs</a>
            <a href="/rendez-vous">Prendre rendez-vous</a>
          </nav>
        </header>

        <main className="home-main">
          <section className="home-section home-hero">
            <div className="home-hero-copy">
              <p className="home-kicker">IVIA</p>
              <h1 className="home-title">
                Quand tout se mélange,
                <br />
                commencez par être entendu.
              </h1>
              <p className="home-subtitle">
                Un espace d&apos;écoute pour nommer ce que vous vivez,
                <br />
                situer ce qui pèse le plus,
                <br />
                et repartir avec une suite concrète.
              </p>
              <div className="home-actions">
                <a className="home-button home-button-primary" href="/rendez-vous">
                  Prendre rendez-vous
                </a>
                <a className="home-button home-button-secondary" href="/#comment">
                  Comment ça fonctionne
                </a>
              </div>
              <div className="home-trustline">
                <p>Séances à 65 $ · Adultes · Non urgent</p>
                <p>Confidentialité assurée · Pas de diagnostic</p>
              </div>
            </div>

            <aside className="home-hero-aside">
              <div className="home-hero-panel">
                <div className="home-hero-panel-line" />
                <p className="home-hero-panel-text">
                  Vous n&apos;avez pas besoin de savoir exactement ce que vous
                  cherchez pour commencer.
                </p>
                <div className="home-trustline">
                  <p>65 $ · En ligne · Confidentiel</p>
                </div>
              </div>
            </aside>
          </section>

          <section className="home-section">
            <div className="home-recognition-wrap">
              <div className="home-recognition">
                <p>
                  Vous n&apos;avez pas toujours besoin
                  <br />
                  d&apos;une réponse immédiate.
                </p>
                <p>
                  Parfois ce dont vous avez besoin en premier,
                  <br />
                  c&apos;est d&apos;un espace pour poser ce que vous portez.
                </p>
                <p>
                  Pas être redirigé. Pas recevoir un diagnostic.
                  <br />
                  Pas vous faire dire quoi faire.
                </p>
                <p>
                  Juste être entendu — vraiment —
                  <br />
                  puis repartir avec quelque chose de plus clair
                  <br />
                  que lorsque vous êtes arrivé.
                </p>
                <p>C&apos;est ce qu&apos;IVIA propose.</p>
              </div>
            </div>
          </section>

          <section className="home-section home-block" id="pour-qui">
            <h2 className="home-section-title">IVIA est fait pour vous si…</h2>
            <ul className="home-list">
              <li>
                Vous traversez une période difficile et vous ne savez pas par où
                commencer.
              </li>
              <li>
                Vous portez quelque chose de lourd, mais vous n&apos;êtes pas en
                crise.
              </li>
              <li>
                Vous avez déjà essayé d&apos;en parler autour de vous, mais ça ne
                suffit plus.
              </li>
              <li>
                Vous hésitez à consulter un professionnel — vous ne savez pas si
                c&apos;est nécessaire, ni lequel.
              </li>
              <li>
                Vous voulez comprendre ce que vous vivez avant de décider quoi
                faire.
              </li>
            </ul>

            <div className="home-block">
              <h3 className="home-subheading">IVIA n&apos;est pas fait pour vous si…</h3>
              <ul className="home-list">
                <li>
                  Vous êtes en danger immédiat → composez le{" "}
                  <a className="home-link-inline" href="tel:911">
                    911
                  </a>{" "}
                  ou le{" "}
                  <a className="home-link-inline" href="tel:3114">
                    3114
                  </a>
                  .
                </li>
                <li>
                  Vous avez besoin d&apos;un diagnostic médical ou d&apos;une
                  prescription.
                </li>
              </ul>
            </div>
          </section>

          <section className="home-section home-block">
            <h2 className="home-section-title">
              Après une séance IVIA, vous repartez avec :
            </h2>
            <div className="home-cards">
              <article className="home-card">
                <h3>Une situation mieux nommée</h3>
                <p>
                  Ce qui était flou devient plus lisible.
                  <br />
                  Pas une vérité définitive —
                  <br />
                  une lecture plus claire de ce que vous vivez.
                </p>
              </article>

              <article className="home-card">
                <h3>Un niveau de vigilance situé</h3>
                <p>
                  Est-ce que ça demande une attention urgente ?
                  <br />
                  Est-ce que vous pouvez souffler ?
                  <br />
                  Vous le saurez mieux.
                </p>
              </article>

              <article className="home-card">
                <h3>Une prochaine étape concrète</h3>
                <p>
                  Pas une liste de conseils génériques.
                  <br />
                  Une suite adaptée à votre réalité —
                  <br />
                  vers qui vous tourner, quoi faire, dans quel ordre.
                </p>
              </article>

              <article className="home-card">
                <h3>Une mémoire de votre parcours</h3>
                <p>
                  Si vous revenez, IVIA se souvient.
                  <br />
                  Pas besoin de tout réexpliquer.
                  <br />
                  Le suivi est continu, utile, et vous appartient.
                </p>
              </article>
            </div>
          </section>

          <section className="home-section home-block" id="comment">
            <h2 className="home-section-title">
              Simple. Sans attente. À votre rythme.
            </h2>
            <div className="home-steps">
              <article className="home-step">
                <div className="home-step-number">①</div>
                <div>
                  <h3>Vous décrivez ce que vous cherchez</h3>
                  <p>
                    Un court formulaire — 2 minutes.
                    <br />
                    Pas de dossier médical, pas d&apos;historique à remplir.
                  </p>
                </div>
              </article>

              <article className="home-step">
                <div className="home-step-number">②</div>
                <div>
                  <h3>Vous choisissez un créneau</h3>
                  <p>
                    Les séances durent 60 à 75 minutes.
                    <br />
                    En ligne, depuis chez vous.
                  </p>
                </div>
              </article>

              <article className="home-step">
                <div className="home-step-number">③</div>
                <div>
                  <h3>Vous êtes entendu</h3>
                  <p>
                    Un espace structuré, bienveillant, confidentiel.
                    <br />
                    Une écoute qui aide à mettre de l&apos;ordre, pas à juger.
                  </p>
                </div>
              </article>

              <article className="home-step">
                <div className="home-step-number">④</div>
                <div>
                  <h3>Vous repartez avec quelque chose</h3>
                  <p>
                    Une synthèse de séance. Une prochaine étape claire.
                    <br />
                    Et si vous revenez, on repart de là où vous en êtes.
                  </p>
                </div>
              </article>
            </div>
          </section>

          <section className="home-section home-pricing" id="tarifs">
            <h2 className="home-section-title">Transparent. Sans surprise.</h2>
            <div className="home-table-wrap">
              <table className="home-table">
                <thead>
                  <tr>
                    <th>Séance</th>
                    <th>Durée</th>
                    <th>Prix</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Séance unique</td>
                    <td>60–75 min</td>
                    <td>65 $</td>
                  </tr>
                  <tr>
                    <td>Forfait 4 séances</td>
                    <td>60–75 min chacune</td>
                    <td>240 $ (60 $/séance)</td>
                  </tr>
                  <tr>
                    <td>Forfait 8 séances</td>
                    <td>60–75 min chacune</td>
                    <td>440 $ (55 $/séance)</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="home-pricing-notes">
              <p>Paiement sécurisé avant la séance.</p>
              <p>Annulation gratuite jusqu&apos;à 24 h avant.</p>
              <p>
                Aucun remboursement d&apos;assurance — IVIA n&apos;est pas un
                service médical.
              </p>
            </div>
          </section>

          <section className="home-section home-block">
            <h2 className="home-section-title">On préfère être clairs.</h2>
            <article className="home-frame">
              <p>
                IVIA n&apos;est pas un service de psychothérapie,
                <br />
                ni un service médical.
                <br />
                IVIA ne pose pas de diagnostic
                <br />
                et ne prescrit pas de traitement.
                <br />
                IVIA ne remplace pas un psychologue,
                <br />
                un médecin ou un service d&apos;urgence
                <br />
                lorsque ceux-ci sont nécessaires.
              </p>
              <br />
              <p>
                Ce que nous faisons : écoute structurée,
                <br />
                clarification de situation,
                <br />
                orientation accompagnée,
                <br />
                continuité de parcours.
              </p>
              <br />
              <p>
                Si votre situation demande plus que ça,
                <br />
                nous vous aiderons à trouver
                <br />
                la bonne porte d&apos;entrée.
              </p>
            </article>
          </section>

          <section className="home-section home-block">
            <h2 className="home-section-title">Quelques mots sur notre approche</h2>
            <article className="home-signature">
              <p>
                IVIA est propulsé par MERLIN —
                <br />
                un moteur documentaire et méthodologique
                <br />
                qui structure l&apos;écoute, organise la mémoire
                <br />
                de parcours et produit une synthèse utile
                <br />
                après chaque séance.
              </p>
              <br />
              <p>
                Notre travail repose sur une idée simple :
                <br />
                beaucoup de personnes ne manquent pas
                <br />
                seulement d&apos;aide —
                <br />
                elles manquent d&apos;abord de clarté.
              </p>
              <br />
              <p className="home-signature-quote">
                IN VIVO IN ACTU — Au sein de l&apos;être, en acte.
              </p>
            </article>
          </section>

          <section className="home-section">
            <article className="home-final">
              <h2 className="home-final-title">
                Vous n&apos;avez pas besoin de savoir exactement
                <br />
                ce que vous cherchez pour commencer.
              </h2>
              <a className="home-button home-button-primary" href="/rendez-vous">
                Prendre rendez-vous
              </a>
              <p className="home-note">65 $ · En ligne · Confidentiel</p>
            </article>
          </section>
        </main>
      </div>
    </div>
  );
}
