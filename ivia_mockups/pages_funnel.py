"""Funnel client complet — de l'inscription au paiement à l'enregistrement.
Aligné sur PROTOCOLE_CONSENTEMENT_CLIENT.md (Loi 25 art 12) et CGU_CLIENTS.md (art 5).
"""
from pathlib import Path
import sys

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from build_pages import page, CLIENT_NAV, FOOTER_CLIENT  # noqa: E402

OUT = ROOT / "client"


# Navigation minimale pour le funnel : on retire les onglets distrayants,
# on garde une option « Déjà inscrit » et un retour discret à l'accueil.
FUNNEL_NAV = [("index.html", "Accueil")]
FUNNEL_ACTIONS = '<a href="connexion.html" class="btn btn--ghost btn--sm">Déjà inscrit·e</a>'


# CSS partagé pour tous les écrans funnel : carte centrale, jauge de progression
FUNNEL_CSS = """
  body { background: linear-gradient(180deg, var(--color-creme) 0%, var(--color-creme-warm) 100%); }
  .funnel { max-width: 640px; margin-inline: auto; padding-block: var(--space-12) var(--space-16); }
  .funnel--wide { max-width: 880px; }
  .funnel__progress { margin-bottom: var(--space-8); }
  .funnel__steps { display: flex; gap: var(--space-2); list-style: none; padding: 0; margin: 0 0 var(--space-3); }
  .funnel__steps li { flex: 1; height: 4px; background: var(--color-divider); border-radius: 2px; transition: background var(--transition); }
  .funnel__steps li.is-done { background: var(--color-mousse); }
  .funnel__steps li.is-current { background: var(--color-aubergine); }
  .funnel__step-label { font-size: var(--text-xs); letter-spacing: 0.16em; text-transform: uppercase; color: var(--color-text-muted); }
  .funnel__title { font-family: var(--font-display); font-size: var(--text-2xl); margin-block: var(--space-3) var(--space-3); }
  .funnel__title em { font-style: italic; color: var(--color-rose); }
  .funnel__intro { font-family: var(--font-serif); font-size: var(--text-lg); color: var(--color-text-muted); margin-bottom: var(--space-8); max-width: 56ch; }

  .funnel__card { background: var(--color-surface); border: 1px solid var(--color-divider); border-radius: var(--radius-xl); padding: var(--space-8); box-shadow: var(--shadow-sm); }
  .funnel__card + .funnel__card { margin-top: var(--space-4); }

  .form__group { display: flex; flex-direction: column; gap: var(--space-2); margin-bottom: var(--space-5); }
  .form__group:last-child { margin-bottom: 0; }
  .form__label { font-family: var(--font-ui); font-size: var(--text-sm); font-weight: 500; color: var(--color-text); }
  .form__hint { font-size: var(--text-xs); color: var(--color-text-muted); font-family: var(--font-serif); }
  .form__input, .form__select, .form__textarea {
    width: 100%;
    padding: var(--space-3) var(--space-4);
    border: 1px solid var(--color-divider);
    border-radius: var(--radius-md);
    background: var(--color-creme);
    font-family: var(--font-ui);
    font-size: var(--text-base);
    color: var(--color-text);
    transition: border-color var(--transition);
  }
  .form__input:focus, .form__select:focus, .form__textarea:focus {
    outline: none; border-color: var(--color-aubergine);
    box-shadow: 0 0 0 3px rgba(42, 31, 45, 0.08);
  }
  .form__textarea { resize: vertical; min-height: 96px; font-family: var(--font-serif); }
  .form__radio-group, .form__check-group { display: flex; flex-direction: column; gap: var(--space-2); }
  .form__radio, .form__check { display: flex; gap: var(--space-3); align-items: flex-start; padding: var(--space-3); border: 1px solid var(--color-divider); border-radius: var(--radius-md); cursor: pointer; transition: all var(--transition); }
  .form__radio:hover, .form__check:hover { border-color: var(--color-rose); background: var(--color-surface-warm); }
  .form__radio input, .form__check input { margin-top: 4px; flex-shrink: 0; accent-color: var(--color-aubergine); }
  .form__radio strong, .form__check strong { display: block; margin-bottom: 2px; font-family: var(--font-ui); font-size: var(--text-sm); }
  .form__radio span, .form__check span { font-family: var(--font-serif); font-size: var(--text-sm); color: var(--color-text-muted); display: block; }

  .funnel__actions { display: flex; justify-content: space-between; align-items: center; gap: var(--space-4); margin-top: var(--space-8); }
  .funnel__back { font-family: var(--font-serif); font-size: var(--text-sm); color: var(--color-text-muted); text-decoration: none; }
  .funnel__back:hover { color: var(--color-aubergine); }

  .consent-niveau { padding: var(--space-5); border-left: 3px solid; border-radius: 0 var(--radius-md) var(--radius-md) 0; background: var(--color-surface-warm); margin-bottom: var(--space-4); }
  .consent-niveau--n1 { border-color: var(--color-aubergine); }
  .consent-niveau--n2 { border-color: var(--color-mousse); }
  .consent-niveau--n3 { border-color: var(--color-glacier); }
  .consent-niveau__tag { font-size: var(--text-xs); letter-spacing: 0.16em; text-transform: uppercase; color: var(--color-text-muted); margin-bottom: var(--space-2); }
  .consent-niveau__tag em { font-style: normal; color: var(--color-rose-deep); }
  .consent-niveau h3 { font-family: var(--font-display); font-size: var(--text-lg); margin-bottom: var(--space-3); }
  .consent-niveau p { font-family: var(--font-serif); font-size: var(--text-sm); color: var(--color-text); margin-bottom: var(--space-3); }
  .consent-niveau__choices { display: flex; gap: var(--space-3); flex-wrap: wrap; }
  .consent-niveau__choices label { display: flex; gap: var(--space-2); align-items: center; padding: var(--space-2) var(--space-4); border: 1px solid var(--color-divider); border-radius: var(--radius-full); background: var(--color-surface); cursor: pointer; font-size: var(--text-sm); }
  .consent-niveau__choices input[type="radio"] { accent-color: var(--color-aubergine); }
  .consent-niveau__choices label:has(input:checked) { background: var(--color-aubergine); color: var(--color-creme); border-color: var(--color-aubergine); }

  .praticien-card { display: grid; grid-template-columns: 80px 1fr auto; gap: var(--space-5); padding: var(--space-5); border: 1px solid var(--color-divider); border-radius: var(--radius-lg); background: var(--color-surface); transition: all var(--transition); cursor: pointer; }
  .praticien-card:has(input:checked) { border-color: var(--color-aubergine); background: var(--color-surface-warm); box-shadow: var(--shadow-sm); }
  .praticien-card + .praticien-card { margin-top: var(--space-3); }
  .praticien-card__avatar { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, var(--color-rose), var(--color-abricot)); display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-size: var(--text-lg); color: var(--color-creme); }
  .praticien-card__avatar--mousse { background: linear-gradient(135deg, var(--color-mousse), var(--color-glacier)); }
  .praticien-card__avatar--lavande { background: linear-gradient(135deg, var(--color-lavande), var(--color-prune)); }
  .praticien-card__body h3 { font-family: var(--font-display); font-size: var(--text-base); margin-bottom: 4px; }
  .praticien-card__body .voie { font-size: var(--text-xs); letter-spacing: 0.12em; text-transform: uppercase; color: var(--color-rose-deep); margin-bottom: var(--space-2); }
  .praticien-card__body p { font-family: var(--font-serif); font-size: var(--text-sm); color: var(--color-text-muted); }
  .praticien-card__price { text-align: right; font-family: var(--font-display); font-size: var(--text-xl); color: var(--color-aubergine); }
  .praticien-card__price small { display: block; font-family: var(--font-serif); font-size: var(--text-xs); color: var(--color-text-muted); font-style: italic; margin-top: 4px; }
  .praticien-card input[type="radio"] { position: absolute; opacity: 0; }

  .checkout-grid { display: grid; grid-template-columns: 1fr 320px; gap: var(--space-6); align-items: start; }
  @media (max-width: 800px) { .checkout-grid { grid-template-columns: 1fr; } }
  .checkout-summary { padding: var(--space-6); background: var(--color-aubergine); color: var(--color-creme); border-radius: var(--radius-lg); position: sticky; top: var(--space-4); }
  .checkout-summary h3 { font-family: var(--font-display); margin-bottom: var(--space-4); color: var(--color-creme); }
  .checkout-summary__line { display: flex; justify-content: space-between; padding-block: var(--space-2); border-bottom: 1px solid rgba(240,233,220,0.15); font-family: var(--font-serif); font-size: var(--text-sm); }
  .checkout-summary__line:last-of-type { border: none; }
  .checkout-summary__total { display: flex; justify-content: space-between; padding-top: var(--space-4); margin-top: var(--space-4); border-top: 1px solid rgba(240,233,220,0.3); font-family: var(--font-display); font-size: var(--text-xl); }
  .checkout-summary__note { font-family: var(--font-serif); font-style: italic; font-size: var(--text-xs); opacity: 0.75; margin-top: var(--space-4); }
  .checkout-stripe-row { display: flex; justify-content: center; align-items: center; gap: var(--space-3); margin-top: var(--space-3); padding: var(--space-3); background: var(--color-surface-warm); border-radius: var(--radius-md); font-family: var(--font-ui); font-size: var(--text-xs); color: var(--color-text-muted); }
  .pay-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); }

  .verify__visuel { width: 96px; height: 96px; margin: 0 auto var(--space-6); border-radius: 50%; background: linear-gradient(135deg, var(--color-rose), var(--color-abricot)); display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-size: 2.5rem; color: var(--color-creme); box-shadow: var(--shadow-md); }
  .verify__code-input { display: flex; gap: var(--space-2); justify-content: center; margin-block: var(--space-6); }
  .verify__code-input input { width: 56px; height: 64px; text-align: center; font-family: var(--font-display); font-size: var(--text-2xl); border: 1px solid var(--color-divider); border-radius: var(--radius-md); background: var(--color-creme); }
  .verify__code-input input:focus { outline: none; border-color: var(--color-aubergine); }

  .success__check { width: 120px; height: 120px; margin: 0 auto var(--space-6); border-radius: 50%; background: var(--color-mousse); display: flex; align-items: center; justify-content: center; }
  .success__check svg { width: 56px; height: 56px; stroke: var(--color-creme); stroke-width: 3; fill: none; }

  .ethics-banner { margin-top: var(--space-12); padding: var(--space-5); background: rgba(240, 233, 220, 0.5); border-left: 3px solid var(--color-rose); border-radius: 0 var(--radius-md) var(--radius-md) 0; font-family: var(--font-serif); font-style: italic; font-size: var(--text-sm); color: var(--color-text-muted); }
"""


def progress(steps, current_idx, label):
    """Génère la jauge de progression du funnel.
    steps : liste de labels courts ; current_idx : 0-based.
    """
    items = []
    for i, _ in enumerate(steps):
        if i < current_idx:
            cls = "is-done"
        elif i == current_idx:
            cls = "is-current"
        else:
            cls = ""
        items.append(f'      <li class="{cls}"></li>')
    items_html = "\n".join(items)
    return f"""<div class="funnel__progress">
    <ul class="funnel__steps">
{items_html}
    </ul>
    <p class="funnel__step-label">Étape {current_idx + 1} sur {len(steps)} · {label}</p>
  </div>"""


# Les 7 étapes du funnel — partagées par toutes les pages pour cohérence
ETAPES = ["Inscription", "Vérification", "Vous identifier", "Consentements", "Choix de la personne", "Paiement", "Enregistrement"]


# ============================================================ ÉTAPE 1 : INSCRIPTION
def build_inscription():
    body = f"""<main class="container">
  <section class="funnel">
    {progress(ETAPES, 0, "Inscription")}
    <p class="funnel__step-label">Au sein de l'être — En actes.</p>
    <h1 class="funnel__title">Bienvenue. <em>Posons-nous.</em></h1>
    <p class="funnel__intro">
      Avant tout, créons votre espace personnel. C'est le seul endroit où vos enregistrements
      et vos retours seront accessibles — par vous d'abord, et par la personne qui vous écoute.
    </p>

    <div class="funnel__card">
      <form>
        <div class="form__group">
          <label class="form__label" for="prenom">Prénom</label>
          <input class="form__input" type="text" id="prenom" placeholder="Comment souhaitez-vous être nommé·e ?" autocomplete="given-name">
          <span class="form__hint">Ce que vous écrivez ici sera utilisé pour vous adresser la parole — pas votre nom légal complet, sauf si vous le voulez.</span>
        </div>

        <div class="form__group">
          <label class="form__label" for="courriel">Courriel</label>
          <input class="form__input" type="email" id="courriel" placeholder="vous@exemple.ca" autocomplete="email">
          <span class="form__hint">Vous recevrez un courriel de vérification dans les minutes qui suivent.</span>
        </div>

        <div class="form__group">
          <label class="form__label" for="mdp">Mot de passe</label>
          <input class="form__input" type="password" id="mdp" placeholder="Au moins 10 caractères" autocomplete="new-password">
          <span class="form__hint">Choisissez quelque chose dont vous vous souviendrez. Vous pourrez aussi vous connecter par lien-courriel si vous préférez.</span>
        </div>

        <div class="form__group">
          <label class="form__check" style="cursor:pointer;">
            <input type="checkbox" required>
            <span style="display:block;">
              <strong style="display:block; margin-bottom:4px;">J'ai lu et j'accepte les conditions de base</strong>
              <span style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted);">
                Les <a href="#" style="color:var(--color-aubergine);">CGU</a> et la <a href="#" style="color:var(--color-aubergine);">politique de confidentialité (Loi 25)</a>.
                Vous pourrez tout retirer plus tard depuis vos préférences.
              </span>
            </span>
          </label>
        </div>

        <div class="funnel__actions">
          <a href="index.html" class="funnel__back">← Retour à l'accueil</a>
          <a href="verifier-courriel.html" class="btn btn--primary">Créer mon espace</a>
        </div>
      </form>
    </div>

    <div class="ethics-banner">
      Vos renseignements sont chiffrés au repos et en transit. IVIA n'est pas un service d'urgence
      et ne pose pas de diagnostic. Si vous êtes en danger immédiat, composez le 9-1-1.
    </div>
  </section>
</main>"""
    html = page(
        "Créer mon espace · IVIA", "Créez votre espace personnel pour vous enregistrer en toute confidentialité.",
        FUNNEL_NAV, "index.html", FUNNEL_ACTIONS, body, css_extra=FUNNEL_CSS,
    )
    (OUT / "inscription.html").write_text(html, encoding="utf-8")


# ============================================================ ÉTAPE 2a : ATTENTE COURRIEL
def build_verifier_courriel():
    body = f"""<main class="container">
  <section class="funnel">
    {progress(ETAPES, 1, "Vérification courriel")}

    <div class="funnel__card" style="text-align:center;">
      <div class="verify__visuel">✉</div>
      <h1 class="funnel__title">Un courriel <em>vous attend.</em></h1>
      <p class="funnel__intro" style="margin-inline:auto;">
        Nous avons envoyé un lien de vérification à <strong>vous@exemple.ca</strong>.
        Cliquez le lien pour confirmer votre adresse, ou collez le code à 6 chiffres ci-dessous.
      </p>

      <div class="verify__code-input">
        <input type="text" maxlength="1" value="4" inputmode="numeric">
        <input type="text" maxlength="1" value="9" inputmode="numeric">
        <input type="text" maxlength="1" value="2" inputmode="numeric">
        <input type="text" maxlength="1" value="" inputmode="numeric">
        <input type="text" maxlength="1" value="" inputmode="numeric">
        <input type="text" maxlength="1" value="" inputmode="numeric">
      </div>

      <a href="approfondissement.html" class="btn btn--primary">Vérifier le code</a>

      <p class="form__hint" style="margin-top:var(--space-6);">
        Vous n'avez rien reçu dans les 5 minutes ?
        <a href="#" style="color:var(--color-aubergine);">Renvoyer le courriel</a>
        · ou
        <a href="#" style="color:var(--color-aubergine);">vérifier votre adresse</a>
      </p>
    </div>

    <div class="funnel__actions" style="justify-content:center;">
      <a href="inscription.html" class="funnel__back">← Modifier mon adresse courriel</a>
    </div>
  </section>
</main>"""
    html = page(
        "Vérifier mon courriel · IVIA", "Confirmez votre adresse courriel pour activer votre espace IVIA.",
        FUNNEL_NAV, "index.html", FUNNEL_ACTIONS, body, css_extra=FUNNEL_CSS,
    )
    (OUT / "verifier-courriel.html").write_text(html, encoding="utf-8")


# ============================================================ ÉTAPE 3 : APPROFONDISSEMENT
def build_approfondissement():
    body = f"""<main class="container">
  <section class="funnel funnel--wide">
    {progress(ETAPES, 2, "Pour mieux vous identifier")}
    <h1 class="funnel__title">Quelques mots — <em>à votre rythme.</em></h1>
    <p class="funnel__intro">
      Ces réponses servent uniquement à orienter votre demande vers la personne qui pourra le mieux
      vous écouter. Aucune obligation de tout remplir aujourd'hui — vous pourrez compléter plus tard.
    </p>

    <form>
      <div class="funnel__card">
        <h2 style="font-family:var(--font-display); font-size:var(--text-xl); margin-bottom:var(--space-6);">Vous, en quelques repères</h2>

        <div class="form__group">
          <label class="form__label" for="age">Votre âge</label>
          <select class="form__select" id="age">
            <option>Choisir une tranche</option>
            <option>14 — 17 ans (consentement parental requis)</option>
            <option>18 — 25 ans</option>
            <option selected>26 — 35 ans</option>
            <option>36 — 50 ans</option>
            <option>51 — 65 ans</option>
            <option>66 ans et plus</option>
            <option>Préfère ne pas répondre</option>
          </select>
        </div>

        <div class="form__group">
          <label class="form__label" for="ville">Votre ville ou région</label>
          <input class="form__input" type="text" id="ville" placeholder="Ex. Montréal, Sherbrooke, Côte-Nord..." value="Montréal">
          <span class="form__hint">Permet de proposer une personne de votre fuseau ou de votre région.</span>
        </div>

        <div class="form__group">
          <label class="form__label">Comment préférez-vous être contacté·e ?</label>
          <div class="form__radio-group">
            <label class="form__radio"><input type="radio" name="contact" checked><span><strong>Courriel</strong>Pour le résumé écrit et la planification du rappel.</span></label>
            <label class="form__radio"><input type="radio" name="contact"><span><strong>Appel téléphonique</strong>Si vous préférez la voix au texte.</span></label>
            <label class="form__radio"><input type="radio" name="contact"><span><strong>Les deux</strong>Selon ce qui est demandé.</span></label>
          </div>
        </div>
      </div>

      <div class="funnel__card">
        <h2 style="font-family:var(--font-display); font-size:var(--text-xl); margin-bottom:var(--space-6);">Ce qui vous amène</h2>

        <div class="form__group">
          <label class="form__label">Quelle voie résonne le plus avec vous, en ce moment ?</label>
          <span class="form__hint" style="margin-bottom:var(--space-3);">Une seule, plusieurs, ou aucune si vous ne savez pas — c'est très bien.</span>
          <div class="form__check-group">
            <label class="form__check"><input type="checkbox"><span><strong>Fréquence</strong>Tout semble dense, accéléré, désaccordé. Vous cherchez à retrouver un rythme habitable.</span></label>
            <label class="form__check"><input type="checkbox" checked><span><strong>Sommeil</strong>Le repos vous échappe ou se déforme. Vous voulez nommer ce qui s'y joue.</span></label>
            <label class="form__check"><input type="checkbox"><span><strong>Connaissance</strong>Vous portez une question qui ne se laisse pas trancher seul·e. Vous avez besoin d'un repère pour clarifier.</span></label>
            <label class="form__check"><input type="checkbox"><span><strong>Je ne sais pas encore</strong>Une personne d'IVIA peut vous aider à situer ce qui se présente.</span></label>
          </div>
        </div>

        <div class="form__group">
          <label class="form__label" for="description">En quelques phrases — qu'est-ce qui vous amène aujourd'hui ?</label>
          <textarea class="form__textarea" id="description" rows="4" placeholder="Pas besoin d'être structuré·e. Une émotion, une situation, une question. Ce que vous écrirez restera entre vous et la personne qui vous écoutera.">Depuis trois semaines, le sommeil arrive en deux temps. Je m'endors vite, puis quelque chose me rappelle vers 3h, et je ne retrouve pas le fil avant 5h. Pas d'alarme dans la journée — juste cette zone qui ne se referme plus.</textarea>
        </div>

        <div class="form__group">
          <label class="form__label">Depuis quand est-ce que cela dure ?</label>
          <div class="form__radio-group">
            <label class="form__radio"><input type="radio" name="duree"><span>Quelques jours</span></label>
            <label class="form__radio"><input type="radio" name="duree" checked><span>Quelques semaines</span></label>
            <label class="form__radio"><input type="radio" name="duree"><span>Plusieurs mois</span></label>
            <label class="form__radio"><input type="radio" name="duree"><span>Plus d'un an</span></label>
            <label class="form__radio"><input type="radio" name="duree"><span>Difficile à dire</span></label>
          </div>
        </div>

        <div class="form__group">
          <label class="form__label" for="essais">Avez-vous déjà essayé d'autres voies pour cela ?</label>
          <textarea class="form__textarea" id="essais" rows="3" placeholder="Médecin, accompagnement, lecture, méditation, rien encore — tout est valable.">Tisanes du soir, lecture avant de dormir. Pas vu de médecin. Je voulais voir si le fait d'en parler à voix haute débloquait quelque chose.</textarea>
        </div>
      </div>

      <div class="funnel__card">
        <h2 style="font-family:var(--font-display); font-size:var(--text-xl); margin-bottom:var(--space-6);">Pour le rappel personnalisé</h2>
        <p style="font-family:var(--font-serif); color:var(--color-text-muted); margin-bottom:var(--space-5);">
          Après votre enregistrement et la lecture de votre résumé écrit, la personne qui vous a écouté·e
          vous appellera pour un échange de 10 minutes. Quand êtes-vous joignable, en général ?
        </p>

        <div class="form__group">
          <label class="form__label">Disponibilités préférées</label>
          <div class="form__check-group">
            <label class="form__check"><input type="checkbox"><span><strong>Matin (8h — 12h)</strong>Jours ouvrables</span></label>
            <label class="form__check"><input type="checkbox" checked><span><strong>Midi (12h — 14h)</strong>Jours ouvrables</span></label>
            <label class="form__check"><input type="checkbox"><span><strong>Après-midi (14h — 17h)</strong>Jours ouvrables</span></label>
            <label class="form__check"><input type="checkbox" checked><span><strong>Soir (17h — 20h)</strong>Jours ouvrables</span></label>
            <label class="form__check"><input type="checkbox"><span><strong>Fin de semaine</strong>Samedi ou dimanche</span></label>
          </div>
        </div>
      </div>

      <div class="funnel__actions">
        <a href="verifier-courriel.html" class="funnel__back">← Étape précédente</a>
        <a href="consentements.html" class="btn btn--primary">Continuer</a>
      </div>
    </form>

    <div class="ethics-banner">
      Tout ce que vous écrivez ici est chiffré et accessible uniquement à la personne qui vous écoutera.
      Vous pouvez modifier ou supprimer ces réponses à tout moment depuis votre espace.
    </div>
  </section>
</main>"""
    html = page(
        "Mieux vous identifier · IVIA", "Quelques repères pour orienter votre demande vers la bonne personne.",
        FUNNEL_NAV, "index.html", FUNNEL_ACTIONS, body, css_extra=FUNNEL_CSS,
    )
    (OUT / "approfondissement.html").write_text(html, encoding="utf-8")


# ============================================================ ÉTAPE 4 : CONSENTEMENTS LOI 25
def build_consentements():
    body = f"""<main class="container">
  <section class="funnel funnel--wide">
    {progress(ETAPES, 3, "Vos consentements")}
    <h1 class="funnel__title">Le consentement, <em>par étapes.</em></h1>
    <p class="funnel__intro">
      La Loi 25 du Québec exige un consentement séparé pour chaque finalité d'usage de vos données.
      IVIA va plus loin : vous décidez niveau par niveau. Tous sont révocables à tout moment depuis vos préférences.
    </p>

    <form>
      <div class="consent-niveau consent-niveau--n1">
        <p class="consent-niveau__tag">Niveau 1 · <em>obligatoire pour utiliser le service</em></p>
        <h3>Enregistrement audio et production de votre résumé</h3>
        <p>
          Pour vous offrir un résumé écrit après votre enregistrement, IVIA conserve votre audio
          de manière sécurisée pendant <strong>30 jours</strong>, puis le détruit de manière irréversible.
          Votre transcription est conservée <strong>90 jours</strong> sous forme pseudonymisée, puis détruite à son tour.
        </p>
        <p style="font-style:italic;">Sans ce consentement, le service audio asynchrone ne peut pas fonctionner.</p>
        <div class="consent-niveau__choices">
          <label><input type="radio" name="n1" checked> Oui, j'accepte l'enregistrement</label>
          <label><input type="radio" name="n1"> Non, je préfère sans enregistrement</label>
        </div>
      </div>

      <div class="consent-niveau consent-niveau--n2">
        <p class="consent-niveau__tag">Niveau 2 · <em>optionnel</em></p>
        <h3>Contribution à la recherche IVIA (anonymisée)</h3>
        <p>
          IVIA travaille à mieux comprendre les rythmes de l'accompagnement émotionnel.
          Si vous le souhaitez, des <strong>signaux anonymisés</strong> de vos enregistrements (pas vos paroles —
          des métadonnées structurées qui ne permettent pas de vous identifier) peuvent contribuer à ce travail.
        </p>
        <p style="font-style:italic;">Votre service n'est pas affecté si vous refusez. Révocable à tout moment.</p>
        <div class="consent-niveau__choices">
          <label><input type="radio" name="n2"> Oui, je contribue</label>
          <label><input type="radio" name="n2" checked> Non merci</label>
        </div>
      </div>

      <div class="consent-niveau consent-niveau--n3">
        <p class="consent-niveau__tag">Niveau 3 · <em>optionnel — plus restrictif</em></p>
        <h3>Contribution au modèle IA propriétaire IVIA</h3>
        <p>
          IVIA développe un modèle d'intelligence artificielle propre, hébergé au Québec, pour améliorer la qualité des analyses.
          Si vous le souhaitez, environ <strong>10 % de vos enregistrements</strong> (sélection automatique des signaux les plus riches)
          peuvent contribuer à son entraînement.
        </p>
        <p style="font-style:italic;">
          Ce modèle ne pourra jamais retrouver ce que vous avez dit, ni vous identifier, ni révéler des enregistrements individuels.
          Il apprend des patterns généraux, pas des histoires personnelles. Applicable seulement si Niveau 2 accepté.
        </p>
        <div class="consent-niveau__choices">
          <label><input type="radio" name="n3"> Oui, je contribue</label>
          <label><input type="radio" name="n3" checked> Non merci</label>
        </div>
      </div>

      <div class="funnel__card" style="background:rgba(141, 169, 184, 0.08); border-color:var(--color-glacier);">
        <p style="font-family:var(--font-serif); color:var(--color-text); margin:0;">
          <strong>Vos droits Loi 25 sont garantis.</strong>
          Vous pouvez à tout moment consulter, modifier ou retirer chacun de ces consentements depuis
          <em>Mon espace → Mes préférences → Mes consentements</em>. La révocation est aussi facile que l'accord.
        </p>
      </div>

      <div class="funnel__actions">
        <a href="approfondissement.html" class="funnel__back">← Étape précédente</a>
        <a href="choix-praticien.html" class="btn btn--primary">Continuer</a>
      </div>
    </form>
  </section>
</main>"""
    html = page(
        "Mes consentements · IVIA", "Trois niveaux de consentement séparés selon la Loi 25 du Québec.",
        FUNNEL_NAV, "index.html", FUNNEL_ACTIONS, body, css_extra=FUNNEL_CSS,
    )
    (OUT / "consentements.html").write_text(html, encoding="utf-8")


# ============================================================ ÉTAPE 5 : CHOIX PRATICIEN
def build_choix_praticien():
    body = f"""<main class="container">
  <section class="funnel funnel--wide">
    {progress(ETAPES, 4, "Choix de la personne qui vous écoutera")}
    <h1 class="funnel__title">Trois personnes <em>répondent</em> à votre voie.</h1>
    <p class="funnel__intro">
      D'après vos repères (voie Sommeil, Montréal, suivi sur quelques semaines), trois écoutant·e·s sont disponibles.
      Le tarif comprend l'écoute, le résumé écrit et le rappel personnalisé de 10 minutes.
    </p>

    <form>
      <label class="praticien-card" style="position:relative;">
        <input type="radio" name="prat" checked>
        <div class="praticien-card__avatar">ML</div>
        <div class="praticien-card__body">
          <h3>Maïté Lavoie-Therrien</h3>
          <p class="voie">Voie Sommeil · Voie Fréquence · Montréal</p>
          <p>Écoute douce, présence stable. Approche centrée sur les rythmes de la nuit et les états de transition. Disponible pour rappel sous 48 h.</p>
        </div>
        <div class="praticien-card__price">
          95 $
          <small>tarif annoncé</small>
        </div>
      </label>

      <label class="praticien-card" style="position:relative;">
        <input type="radio" name="prat">
        <div class="praticien-card__avatar praticien-card__avatar--mousse">EG</div>
        <div class="praticien-card__body">
          <h3>Étienne Grondin-Côté</h3>
          <p class="voie">Voie Connaissance · Voie Sommeil · Québec</p>
          <p>Écoute analytique, repères structurés. Convient si vous portez une question complexe et cherchez un appui pour la clarifier.</p>
        </div>
        <div class="praticien-card__price">
          85 $
          <small>tarif annoncé</small>
        </div>
      </label>

      <label class="praticien-card" style="position:relative;">
        <input type="radio" name="prat">
        <div class="praticien-card__avatar praticien-card__avatar--lavande">NT</div>
        <div class="praticien-card__body">
          <h3>Nicole Tremblay-Roy</h3>
          <p class="voie">Voie Sommeil · Voie Fréquence · Saguenay</p>
          <p>Approche corporelle et sensorielle, ancrée dans le souffle. Pratique de longue date. Délai de réponse plus long (3 — 5 jours).</p>
        </div>
        <div class="praticien-card__price">
          105 $
          <small>tarif annoncé</small>
        </div>
      </label>

      <p style="font-family:var(--font-serif); font-style:italic; color:var(--color-text-muted); text-align:center; margin-block:var(--space-6); font-size:var(--text-sm);">
        Le tarif est défini par chaque écoutant·e selon son expérience.
        Il est annoncé clairement avant tout paiement (article 5.2 de nos CGU).
      </p>

      <div class="funnel__actions">
        <a href="consentements.html" class="funnel__back">← Étape précédente</a>
        <a href="paiement.html" class="btn btn--primary">Continuer vers le paiement</a>
      </div>
    </form>
  </section>
</main>"""
    html = page(
        "Choix de l'écoutant·e · IVIA", "Sélectionnez la personne qui vous écoutera selon votre voie.",
        FUNNEL_NAV, "index.html", FUNNEL_ACTIONS, body, css_extra=FUNNEL_CSS,
    )
    (OUT / "choix-praticien.html").write_text(html, encoding="utf-8")


# ============================================================ ÉTAPE 6 : PAIEMENT
def build_paiement():
    body = f"""<main class="container">
  <section class="funnel funnel--wide">
    {progress(ETAPES, 5, "Paiement sécurisé")}
    <h1 class="funnel__title">Paiement <em>sécurisé.</em></h1>
    <p class="funnel__intro">
      Le paiement est traité par Stripe — IVIA ne stocke jamais votre numéro de carte.
      Tout est en dollars canadiens, taxes en sus le cas échéant.
    </p>

    <div class="checkout-grid">
      <form>
        <div class="funnel__card">
          <h2 style="font-family:var(--font-display); font-size:var(--text-xl); margin-bottom:var(--space-6);">Carte de crédit</h2>

          <div class="form__group">
            <label class="form__label" for="cc-num">Numéro de carte</label>
            <input class="form__input" type="text" id="cc-num" placeholder="1234 5678 9012 3456" autocomplete="cc-number" inputmode="numeric">
          </div>

          <div class="pay-grid-2">
            <div class="form__group">
              <label class="form__label" for="cc-exp">Expiration</label>
              <input class="form__input" type="text" id="cc-exp" placeholder="MM / AA" autocomplete="cc-exp" inputmode="numeric">
            </div>
            <div class="form__group">
              <label class="form__label" for="cc-cvv">CVV</label>
              <input class="form__input" type="text" id="cc-cvv" placeholder="123" autocomplete="cc-csc" inputmode="numeric">
            </div>
          </div>

          <div class="form__group">
            <label class="form__label" for="cc-nom">Nom sur la carte</label>
            <input class="form__input" type="text" id="cc-nom" placeholder="Camille Tremblay" autocomplete="cc-name">
          </div>

          <div class="form__group" style="margin-top:var(--space-6); margin-bottom:0;">
            <label class="form__check" style="cursor:pointer;">
              <input type="checkbox" checked>
              <span style="display:block;">
                <strong style="display:block; margin-bottom:4px;">J'accepte la politique d'annulation</strong>
                <span style="font-family:var(--font-serif); font-size:var(--text-sm); color:var(--color-text-muted);">
                  Annulation gratuite avant l'envoi de l'enregistrement.
                  Une fois l'audio envoyé, le service est considéré comme entamé.
                  <a href="#" style="color:var(--color-aubergine);">Détails</a>.
                </span>
              </span>
            </label>
          </div>
        </div>

        <div class="checkout-stripe-row">
          <span aria-hidden="true">🔒</span>
          <span>Paiement chiffré par <strong style="color:var(--color-aubergine);">Stripe</strong> · PCI-DSS Niveau 1 · Aucune donnée carte n'est conservée par IVIA</span>
        </div>

        <div class="funnel__actions">
          <a href="choix-praticien.html" class="funnel__back">← Modifier le choix</a>
          <a href="confirmation-paiement.html" class="btn btn--primary">Payer 95 $ et continuer</a>
        </div>
      </form>

      <aside class="checkout-summary">
        <h3>Votre demande</h3>
        <div class="checkout-summary__line"><span>Écoute audio asynchrone</span><span>—</span></div>
        <div class="checkout-summary__line"><span>Avec Maïté Lavoie-Therrien</span><span>—</span></div>
        <div class="checkout-summary__line"><span>Voie Sommeil</span><span>—</span></div>
        <div class="checkout-summary__line"><span>Résumé écrit</span><span>inclus</span></div>
        <div class="checkout-summary__line"><span>Rappel personnalisé 10 min</span><span>inclus</span></div>
        <div class="checkout-summary__total"><span>Total</span><span>95 $</span></div>
        <p class="checkout-summary__note">Tarif fixé par l'écoutant·e (CGU 5.2). Devise CAD. Taxes en sus si applicables.</p>
      </aside>
    </div>
  </section>
</main>"""
    html = page(
        "Paiement · IVIA", "Paiement sécurisé par Stripe pour finaliser votre demande d'écoute.",
        FUNNEL_NAV, "index.html", FUNNEL_ACTIONS, body, css_extra=FUNNEL_CSS,
    )
    (OUT / "paiement.html").write_text(html, encoding="utf-8")


# ============================================================ ÉTAPE 7 : CONFIRMATION
def build_confirmation_paiement():
    body = f"""<main class="container">
  <section class="funnel">
    {progress(ETAPES, 6, "Tout est prêt")}

    <div class="funnel__card" style="text-align:center;">
      <div class="success__check">
        <svg viewBox="0 0 24 24"><path d="M5 12 L10 17 L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <h1 class="funnel__title">C'est confirmé. <em>À vous.</em></h1>
      <p class="funnel__intro" style="margin-inline:auto;">
        Paiement reçu. Maïté Lavoie-Therrien a été avertie. Vous pouvez maintenant déposer votre enregistrement —
        à votre rythme, sans contrainte de durée stricte (jusqu'à 15 minutes).
      </p>

      <div style="display:flex; flex-direction:column; gap:var(--space-3); margin-block:var(--space-6); text-align:left; padding:var(--space-5); background:var(--color-surface-warm); border-radius:var(--radius-lg);">
        <div style="display:flex; gap:var(--space-3);"><span style="font-family:var(--font-display); color:var(--color-mousse);">✓</span><span style="font-family:var(--font-serif); font-size:var(--text-sm);">Reçu de paiement envoyé à <strong>vous@exemple.ca</strong></span></div>
        <div style="display:flex; gap:var(--space-3);"><span style="font-family:var(--font-display); color:var(--color-mousse);">✓</span><span style="font-family:var(--font-serif); font-size:var(--text-sm);">Maïté recevra votre audio dès l'envoi · réponse écrite sous 48 h ouvrables</span></div>
        <div style="display:flex; gap:var(--space-3);"><span style="font-family:var(--font-display); color:var(--color-mousse);">✓</span><span style="font-family:var(--font-serif); font-size:var(--text-sm);">Rappel personnalisé de 10 minutes planifié après votre lecture du résumé</span></div>
      </div>

      <a href="audio-async.html" class="btn btn--primary" style="margin-bottom:var(--space-4);">Commencer l'enregistrement</a>
      <p class="form__hint">
        Pas prêt·e à enregistrer maintenant ?
        <a href="dashboard.html" style="color:var(--color-aubergine);">Le faire plus tard depuis mon espace</a>
      </p>
    </div>

    <div class="ethics-banner">
      Vous pouvez interrompre, recommencer ou annuler à tout moment avant l'envoi.
      Rien n'est transmis tant que vous ne confirmez pas l'envoi.
    </div>
  </section>
</main>"""
    html = page(
        "Confirmation de paiement · IVIA", "Votre paiement est confirmé — vous pouvez commencer l'enregistrement.",
        FUNNEL_NAV, "index.html", FUNNEL_ACTIONS, body, css_extra=FUNNEL_CSS,
    )
    (OUT / "confirmation-paiement.html").write_text(html, encoding="utf-8")


# ============================================================ CONNEXION (utilisateur existant)
def build_connexion():
    body = f"""<main class="container">
  <section class="funnel">
    <p class="funnel__step-label">Au sein de l'être — En actes.</p>
    <h1 class="funnel__title">Bon retour. <em>Connectez-vous.</em></h1>
    <p class="funnel__intro">
      Retrouvez vos résumés, votre journal et vos préférences.
    </p>

    <div class="funnel__card">
      <form>
        <div class="form__group">
          <label class="form__label" for="login-email">Courriel</label>
          <input class="form__input" type="email" id="login-email" placeholder="vous@exemple.ca" autocomplete="email">
        </div>

        <div class="form__group">
          <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <label class="form__label" for="login-mdp">Mot de passe</label>
            <a href="#" style="font-size:var(--text-xs); color:var(--color-aubergine);">Oublié</a>
          </div>
          <input class="form__input" type="password" id="login-mdp" placeholder="Votre mot de passe" autocomplete="current-password">
        </div>

        <a href="dashboard.html" class="btn btn--primary" style="width:100%; margin-top:var(--space-3);">Se connecter</a>

        <p style="text-align:center; margin-block:var(--space-4); font-family:var(--font-serif); color:var(--color-text-muted); font-size:var(--text-sm);">— ou —</p>

        <a href="#" class="btn btn--ghost" style="width:100%;">Recevoir un lien de connexion par courriel</a>
      </form>
    </div>

    <p style="text-align:center; margin-top:var(--space-6); font-family:var(--font-serif); color:var(--color-text-muted);">
      Pas encore de compte ?
      <a href="inscription.html" style="color:var(--color-aubergine); font-weight:500;">Créer mon espace</a>
    </p>

    <div class="ethics-banner">
      IVIA n'est pas un service d'urgence et ne pose pas de diagnostic.
      Si vous êtes en danger immédiat, composez le 9-1-1.
    </div>
  </section>
</main>"""
    html = page(
        "Connexion · IVIA", "Connectez-vous à votre espace IVIA.",
        FUNNEL_NAV, "index.html", FUNNEL_ACTIONS, body, css_extra=FUNNEL_CSS,
    )
    (OUT / "connexion.html").write_text(html, encoding="utf-8")


def build():
    build_inscription()
    build_verifier_courriel()
    build_approfondissement()
    build_consentements()
    build_choix_praticien()
    build_paiement()
    build_confirmation_paiement()
    build_connexion()


if __name__ == "__main__":
    build()
    print("✓ funnel construit")
