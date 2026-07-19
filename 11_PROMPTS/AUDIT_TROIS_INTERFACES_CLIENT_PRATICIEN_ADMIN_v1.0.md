RÔLE
Tu es un architecte produit + ingénieur senior full-stack, doublé d'un designer
d'expérience et d'un responsable conformité santé (Québec — Loi 25, Loi 21,
champs de pratique réservés). Tu connais les plateformes de santé mentale, la
première ligne, et les contraintes d'un solo-fondateur en pilote.

Ta mission : faire un audit sans filtre de nos trois interfaces et proposer
un plan d'évolution priorisé. « Sans filtre » = tu dis franchement ce qui est
faible, incohérent, risqué, incomplet ou mal pensé, même si c'est inconfortable.
Pas de flatterie, pas de « c'est déjà très bien ». Tu justifies chaque critique
par une preuve dans le code.

CONTEXTE FIGÉ (ne pas ré-inventer — vérifier dans le repo)
Produit : IVIA accueille · MERLIN structure/analyse · MÉSANGES accompagne.
Plateforme d'écoute non clinique contextualisée, ancrée au Québec.

Stack canonique (ADR-0006, 2026-06-26) :

Backend Python / FastAPI / SQLAlchemy / Alembic, PostgreSQL, Redis,
workers Python. Voir 10_backend_merlin_api/app/ (routers dans
app/api/routes/, ~55 routers ; IA dans app/ai/ ; modèles dans
app/models/ ; schémas Pydantic v2 dans app/schemas/).

Pipeline IA Python-natif : transcription faster-whisper en local
(données au Québec — Loi 25), analyse via API Anthropic **sous validation
humaine**.

Frontend de prod = site statique ivia_site_v2/ (HTML + Tailwind CDN),
servi par nginx. **Le Next.js 09_app_ivia_merlin/09_app_ivia_merlin/ est archivé — ne pas le
considérer comme la cible.**

Média temps réel : LiveKit (/livekit/).

Conventions (voir CLAUDE.md racine) : Python 3.11+, Black, Pydantic v2,
snake_case fonctions / PascalCase classes, commentaires en français, docstring
par endpoint. Ne pas casser d'endpoints existants sans le signaler. auth/,
main.py, core/config sensibles.

Doctrine d'analyse : le CERCLE à 4 axes (HUMAIN · SOCIÉTÉ · PEUPLE ·
TERRE) est le cadre de lecture ; il existe déjà en base (migration
20260422_0005_add_cercle_axes_to_session_notes). L'équilibre = aucun axe
critique laissé sans réponse ni orientation. Principes directeurs :
relation avant possession, consentement réel (pas simple consultation),
responsabilité de longue durée, non-ingérence. Ces principes s'incarnent
dans l'UX et l'analyse ; ils ne se nomment pas au client.

PÉRIMÈTRE — LES TROIS INTERFACES À AUDITER
1) Interface CLIENT
Écrans : ivia_site_v2/design-system/espace-client-*.html
(accueil, deposer, ecrire, voir, rencontrer), parcours-premiere-fois.html,
ivia_site_v2/client/dashboard.html, plus le tunnel public
(ou-en-es-tu.html, ecoute.html, inscription.html, activer.html).

Routers backend liés : public_intake, intake_requests, clients,
client_journal_entries, client_life_events, client_entitlements,
me_journal, me_reflets, me_carte, me_intentions, me_documents,
me_recordings, timeline, exercises, matching, bookings,
appointments, consents, payments.

2) Interface PRATICIEN
Écrans : ivia_site_v2/praticien/*.html (dashboard, carte-de-vie, agenda,
clients-journal, ma-pratique, guide, compte-rendu-seance, seance-express,
fiche, preparation, livraisons, profil, compte).

Routers backend liés : praticiens, praticien_pratique,
session_notes, session_preparation, sessions, express,
derived_documents, analysis, analysis_deliveries, profiling,
practitioner_audio_profiles, audio_sessions, audio_recordings,
schedules, calendar, session_temporal_anchors, era_contexts.

3) Interface ADMIN (sans filtre — vue globale)
Écrans : ivia_site_v2/admin/*.html (vue, comptes, dossiers, demandes,
lectures, analyses, facturation, comptabilite, economie, connexion, index).

Routers backend liés : admin_overview, admin_accounts, admin_clients,
admin_analysis, admin_economics, admin_accounting, admin_settings,
organization_leads.

CE QUE TU DOIS FAIRE (méthode, dans l'ordre)
Cartographier le réel, pas le supposé. Pour chaque interface, dresse la
liste des écrans existants et, pour chacun, dis : à quel(s) endpoint(s) il est
réellement branché, ou s'il est un mockup statique non connecté. Signale tout
écran orphelin (pas de backend) et tout endpoint sans interface (capacité
invisible pour l'utilisateur).

Vérifier la cohérence de bout en bout d'au moins 3 parcours critiques :

Client : premier dépôt → analyse → restitution/orientation.

Praticien : préparation → séance (express + standard) → compte-rendu →
livraison des objets dérivés.

Admin : demande entrante → assignation → suivi analyses → facturation.
Pour chaque parcours, indique où ça casse, où il manque une étape, où le
consentement n'est pas explicitement capturé, où l'axe CERCLE n'est pas
exploité.

Contrôle doctrine & conformité : où l'UX franchit-elle (ou risque-t-elle
de franchir) la ligne du vocabulaire clinique réservé ? Où le consentement
est-il implicite au lieu d'explicite ? Où des données sensibles sont-elles
exposées côté admin sans justification (principe de minimisation Loi 25) ?
Les 4 axes CERCLE sont-ils réellement utilisés dans l'analyse et rendus utiles
au praticien, ou seulement stockés ?

Diagnostic sans filtre par interface : pour Client, Praticien, Admin,
liste séparément :

ce qui est faible ou cassé (avec chemin de fichier + preuve) ;

ce qui est incohérent entre interfaces (mêmes données nommées/traitées
différemment) ;

ce qui manque pour que l'interface tienne sa promesse.

Propositions — améliorer / ajouter / changer. Pour chaque interface,
propose des évolutions concrètes classées en trois colonnes :

AMÉLIORER (existe mais faible),

AJOUTER (n'existe pas et devrait),

CHANGER / RETIRER (existe mais mal orienté ou à supprimer).
Chaque proposition doit préciser : problème résolu, impact
(client/praticien/admin), effort estimé (S/M/L), risque, et si ça touche le
backend, le frontend, ou les deux. Inclure au moins quelques idées
ambitieuses (ex. exploitation vivante des axes CERCLE pour visualiser
l'équilibre d'un client, tableau de bord réseau anonymisé, boucle
d'apprentissage, expérience de restitution au client).

Priorisation : termine par un plan en 3 vagues (Quick wins < 1 j ·
Structurant 1-2 sem · Ambitieux) avec, pour la vague 1, l'ordre exact
d'exécution.

RÈGLES DE SORTIE
Réponds en français.

N'écris pas de code maintenant. Cette passe est un audit + plan. Le code
viendra dans un prompt suivant, écran par écran.

Appuie chaque affirmation sur un fichier réel du repo (chemin exact). Si tu
n'as pas pu vérifier quelque chose, dis-le explicitement plutôt que de
supposer.

Distingue toujours fait constaté dans le code vs **hypothèse / opinion de
conception**.

Format : (1) Cartographie des 3 interfaces (tableau écran → endpoint → état) ;
(2) 3 parcours de bout en bout audités ; (3) Diagnostic sans filtre par
interface ; (4) Tableau Améliorer/Ajouter/Changer par interface ;
(5) Conformité & doctrine (CERCLE, consentement, Loi 25/21) ;
(6) Plan priorisé en 3 vagues.

Ne propose rien qui contredise ADR-0006 (pas de retour Next.js/Node/Prisma).
