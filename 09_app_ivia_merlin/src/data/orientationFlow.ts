/* ──────────────────────────────────────────────────────────────────────────
   IVIA — Parcours d'orientation public
   Fichier de configuration : aucune donnée persistée, aucun appel réseau.
   La structure est lue par <OrientationFlow /> pour bâtir l'expérience
   mobile-first « une question à la fois » avec progression et portrait
   final non médical.

   Doctrine : aide à préparer une conversation et à orienter, pas un
   diagnostic. Les axes prioritaires servent à colorer le portrait, jamais
   à étiqueter la personne.
   ────────────────────────────────────────────────────────────────────────── */

export type DimensionKey =
  | "territoire"
  | "corps"
  | "etats"
  | "liens"
  | "temporalite"
  | "rythmes"
  | "heritage"
  | "social"
  | "numerique"
  | "autonomie";

export type VoieKey =
  | "personne"
  | "collectivite"
  | "praticien"
  | "comprendre";

export const DIMENSION_LABELS: Record<DimensionKey, string> = {
  territoire: "Territoire & terrain vivant",
  corps: "Corps & métabolisme",
  etats: "États intérieurs",
  liens: "Liens & famille",
  temporalite: "Temporalité & répétitions",
  rythmes: "Sommeil & rythmes",
  heritage: "Héritages & transgénérationnel",
  social: "Pression sociale & culturelle",
  numerique: "Numérique & attention",
  autonomie: "Autonomie & action",
};

export type OptionChoice = {
  id: string;
  label: string;
  hint?: string;
  dims?: DimensionKey[];
};

export type Step = {
  id: string;
  kind: "single" | "multi" | "text" | "intensity";
  /** Voie(s) pour laquelle cette étape doit apparaître. `all` = toutes. */
  voies: VoieKey[] | "all";
  question: string;
  helper?: string;
  options?: OptionChoice[];
  /** Pour les champs texte : placeholder. */
  placeholder?: string;
  /** Pour les questions optionnelles, autorise un saut. */
  optional?: boolean;
};

/* ── Étape 0 : voie ───────────────────────────────────────────────────── */
export const VOIE_STEP: Step = {
  id: "voie",
  kind: "single",
  voies: "all",
  question: "Qu'est-ce qui vous amène ici ?",
  helper:
    "Quatre portes, une même maison. Vous pourrez changer d'avis à tout moment.",
  options: [
    {
      id: "personne",
      label: "Pour moi-même",
      hint: "Je veux déposer ce que je vis et mieux le comprendre.",
    },
    {
      id: "collectivite",
      label: "Pour une collectivité",
      hint: "Une famille, une équipe, un organisme, une communauté.",
    },
    {
      id: "praticien",
      label: "Pour ma pratique",
      hint: "Je veux structurer ma préparation, mes interprétations, mon suivi.",
    },
    {
      id: "comprendre",
      label: "Pour comprendre IVIA",
      hint: "Lire l'approche, sans engager une démarche tout de suite.",
    },
  ],
};

/* ── Étapes communes (personne, collectivité) ─────────────────────────── */
export const STEPS_PERSONNE: Step[] = [
  {
    id: "territoire-ancrage",
    kind: "multi",
    voies: ["personne", "collectivite"],
    question: "Où se passe votre vie en ce moment ?",
    helper:
      "Commencer par le territoire et le terrain vivant. Cochez ce qui résonne.",
    options: [
      {
        id: "qc-urbain",
        label: "Ville ou banlieue au Québec",
        dims: ["territoire"],
      },
      {
        id: "qc-region",
        label: "Région, village, milieu rural",
        dims: ["territoire"],
      },
      {
        id: "qc-nordique",
        label: "Nord du Québec ou territoire éloigné",
        dims: ["territoire"],
      },
      {
        id: "diaspora",
        label: "Hors du Québec, mais lié·e à ce territoire",
        dims: ["territoire"],
      },
      {
        id: "deracine",
        label: "En transition de lieu, peu d'ancrage présentement",
        dims: ["territoire", "etats"],
      },
      {
        id: "nature",
        label: "Lien régulier avec la nature, les saisons",
        dims: ["territoire", "rythmes"],
      },
    ],
  },
  {
    id: "situation-libre",
    kind: "text",
    voies: ["personne", "collectivite"],
    question: "Dans vos mots, qu'est-ce qui demande à être nommé ?",
    helper:
      "Quelques lignes suffisent. Aucune donnée n'est enregistrée à cette étape : ce texte sert uniquement à préparer votre portrait dans cette fenêtre.",
    placeholder:
      "Ex. Je me sens épuisé·e depuis l'automne, mes nuits sont fragmentées, je n'arrive plus à me poser…",
    optional: true,
  },
  {
    id: "dimensions",
    kind: "multi",
    voies: ["personne", "collectivite"],
    question: "Qu'est-ce qui est touché en ce moment ?",
    helper:
      "Cochez les dimensions qui vous parlent. Il n'y a pas de bonne ou de mauvaise réponse.",
    options: [
      { id: "d-corps", label: "Corps, énergie, métabolisme", dims: ["corps"] },
      { id: "d-rythmes", label: "Sommeil, repas, rythmes", dims: ["rythmes", "corps"] },
      { id: "d-emotions", label: "Émotions, états intérieurs", dims: ["etats"] },
      { id: "d-mental", label: "Mental, pensées qui tournent", dims: ["etats", "temporalite"] },
      { id: "d-liens", label: "Relations, famille, proches", dims: ["liens"] },
      { id: "d-heritage", label: "Héritages, transmissions, transgénérationnel", dims: ["heritage", "liens"] },
      { id: "d-social", label: "Pression sociale, économique, culturelle", dims: ["social"] },
      { id: "d-num", label: "Numérique, attention, liens artificiels", dims: ["numerique"] },
      { id: "d-autonomie", label: "Capacité d'agir, autonomie", dims: ["autonomie"] },
      { id: "d-territoire", label: "Lien au territoire, à l'environnement", dims: ["territoire"] },
    ],
  },
  {
    id: "temporalite",
    kind: "single",
    voies: ["personne", "collectivite"],
    question: "Depuis combien de temps cela demande de l'attention ?",
    options: [
      { id: "t-recent", label: "Quelques semaines", dims: ["temporalite"] },
      { id: "t-mois", label: "Plusieurs mois", dims: ["temporalite"] },
      { id: "t-annee", label: "Une année ou plus", dims: ["temporalite"] },
      {
        id: "t-cycle",
        label: "Cela revient par vagues, par cycles",
        dims: ["temporalite", "rythmes"],
      },
      {
        id: "t-toujours",
        label: "Cela semble présent depuis longtemps",
        dims: ["temporalite", "heritage"],
      },
    ],
  },
  {
    id: "intensite",
    kind: "intensity",
    voies: ["personne", "collectivite"],
    question: "Comment décririez-vous l'intensité présentement ?",
    helper:
      "Cette échelle ne sert pas à mesurer une gravité clinique. Elle aide simplement à doser la suite.",
    options: [
      { id: "i-1", label: "Léger, je veux surtout clarifier" },
      { id: "i-2", label: "Présent, mais gérable" },
      { id: "i-3", label: "Fatiguant, cela pèse" },
      { id: "i-4", label: "Lourd, je me sens dépassé·e" },
      {
        id: "i-5",
        label: "Très lourd, ou crise immédiate",
        hint: "Voir le rappel urgence à la fin.",
      },
    ],
  },
];

/* ── Étapes praticien ─────────────────────────────────────────────────── */
export const STEPS_PRATICIEN: Step[] = [
  {
    id: "p-statut",
    kind: "single",
    voies: ["praticien"],
    question: "Comment décririez-vous votre statut professionnel ?",
    helper:
      "Chaque statut est nommé et respecté. IVIA n'efface ni ne hiérarchise.",
    options: [
      { id: "ps-diplome", label: "Diplômé·e d'un ordre ou d'une formation reconnue" },
      { id: "ps-formation", label: "En formation ou en transition de pratique" },
      { id: "ps-hors-ordre", label: "Pratique complémentaire, hors ordre" },
      { id: "ps-autre", label: "Autre / je préfère préciser plus tard" },
    ],
  },
  {
    id: "p-besoins",
    kind: "multi",
    voies: ["praticien"],
    question: "Qu'est-ce qui appellerait une structure plus claire ?",
    options: [
      { id: "pb-preparation", label: "Préparation des rencontres" },
      { id: "pb-interpretation", label: "Interprétation des séances" },
      { id: "pb-feedback", label: "Boucle de feedback éthique" },
      { id: "pb-correspondances", label: "Lecture des correspondances vivantes" },
      { id: "pb-limites", label: "Nommer mes limites et mon cadre" },
      { id: "pb-continuite", label: "Continuité d'un suivi sur plusieurs séances" },
    ],
  },
  {
    id: "p-pratique",
    kind: "text",
    voies: ["praticien"],
    question: "Pouvez-vous décrire votre pratique en quelques mots ?",
    helper:
      "Approche, public habituel, contexte de travail. Ce texte n'est pas enregistré.",
    placeholder:
      "Ex. Travailleuse sociale en CIUSSS, je reçois beaucoup d'adolescents en post-pandémie…",
    optional: true,
  },
];

/* ── Étapes collectivité ──────────────────────────────────────────────── */
export const STEPS_COLLECTIF: Step[] = [
  {
    id: "c-type",
    kind: "single",
    voies: ["collectivite"],
    question: "De quel collectif s'agit-il ?",
    options: [
      { id: "ct-famille", label: "Famille, fratrie, lien intime" },
      { id: "ct-organisme", label: "Organisme communautaire" },
      { id: "ct-praticiens", label: "Groupe de praticiens" },
      { id: "ct-territoriale", label: "Communauté territoriale" },
      { id: "ct-terrain", label: "Équipe de terrain, milieu de soin ou de service" },
      { id: "ct-transition", label: "Milieu humain en transition (deuil, fusion, refonte)" },
    ],
  },
];

/* ── Étape comprendre ─────────────────────────────────────────────────── */
export const STEPS_COMPRENDRE: Step[] = [
  {
    id: "co-curiosite",
    kind: "multi",
    voies: ["comprendre"],
    question: "Qu'est-ce qui vous intrigue dans IVIA ?",
    options: [
      { id: "cc-doctrine", label: "La doctrine : IVIA, MERLIN, MÉSANGES" },
      { id: "cc-territoire", label: "L'ancrage au territoire québécois" },
      { id: "cc-correspondances", label: "Les correspondances vivantes" },
      { id: "cc-ia", label: "L'usage prudent de l'intelligence artificielle" },
      { id: "cc-souverainete", label: "La souveraineté des données" },
      { id: "cc-praticiens", label: "Le lien avec les praticiens" },
    ],
  },
];

/* ── Construction dynamique du parcours ───────────────────────────────── */
export function buildSteps(voie: VoieKey | null): Step[] {
  if (!voie) return [VOIE_STEP];
  switch (voie) {
    case "personne":
      return [VOIE_STEP, ...STEPS_PERSONNE];
    case "collectivite":
      return [VOIE_STEP, ...STEPS_COLLECTIF, ...STEPS_PERSONNE];
    case "praticien":
      return [VOIE_STEP, ...STEPS_PRATICIEN];
    case "comprendre":
      return [VOIE_STEP, ...STEPS_COMPRENDRE];
  }
}

/* ── Résultat / portrait ──────────────────────────────────────────────── */
export type Answers = Record<string, string[] | string>;

export type PortraitLayer = {
  key: DimensionKey;
  label: string;
  score: number;
};

export type PortraitCTA = {
  label: string;
  href: string;
  tone: "ink" | "argile" | "sage" | "cream";
  hint: string;
};

export type Portrait = {
  voie: VoieKey;
  phrase: string;
  layers: PortraitLayer[];
  urgent: boolean;
  cta: PortraitCTA;
};

const VOIE_PHRASES: Record<VoieKey, string> = {
  personne:
    "Vous arrivez pour vous-même. Voici trois couches qui ressortent de ce que vous venez de partager.",
  collectivite:
    "Vous arrivez pour un milieu vivant. Voici trois couches qui ressortent dans ce que ce collectif traverse.",
  praticien:
    "Vous arrivez avec une pratique. Voici trois axes où IVIA pourrait soutenir votre préparation et votre interprétation.",
  comprendre:
    "Vous arrivez pour comprendre. Voici trois entrées qui correspondent à ce qui vous intrigue.",
};

const VOIE_CTA: Record<VoieKey, PortraitCTA> = {
  personne: {
    label: "Commencer mon espace privé",
    href: "/demarche",
    tone: "ink",
    hint: "Un espace pour déposer, à votre rythme, sous consentement.",
  },
  collectivite: {
    label: "Ouvrir un espace commun",
    href: "#collectivites-vivantes",
    tone: "argile",
    hint: "Lire ce qui se cartographie pour un collectif, sans imposer une lecture unique.",
  },
  praticien: {
    label: "Découvrir l'espace praticien",
    href: "/espace-praticien",
    tone: "sage",
    hint: "Un miroir structuré pour votre préparation et votre interprétation.",
  },
  comprendre: {
    label: "Lire l'approche",
    href: "#approche",
    tone: "cream",
    hint: "Comprendre la maison du vivant, sans engagement.",
  },
};

const COMPRENDRE_DIMENSION_MAP: Record<string, DimensionKey> = {
  "cc-doctrine": "autonomie",
  "cc-territoire": "territoire",
  "cc-correspondances": "liens",
  "cc-ia": "numerique",
  "cc-souverainete": "autonomie",
  "cc-praticiens": "liens",
};

export function buildPortrait(answers: Answers): Portrait | null {
  const voie = (answers.voie as string) as VoieKey | undefined;
  if (!voie) return null;

  const scores: Record<DimensionKey, number> = {
    territoire: 0,
    corps: 0,
    etats: 0,
    liens: 0,
    temporalite: 0,
    rythmes: 0,
    heritage: 0,
    social: 0,
    numerique: 0,
    autonomie: 0,
  };

  const allSteps = buildSteps(voie);
  for (const step of allSteps) {
    if (!step.options) continue;
    const raw = answers[step.id];
    const selected = Array.isArray(raw) ? raw : raw ? [raw] : [];
    for (const optId of selected) {
      const opt = step.options.find((o) => o.id === optId);
      if (!opt) continue;
      if (opt.dims) {
        for (const dim of opt.dims) {
          scores[dim] += 1;
        }
      }
      if (voie === "comprendre" && COMPRENDRE_DIMENSION_MAP[optId]) {
        scores[COMPRENDRE_DIMENSION_MAP[optId]] += 1;
      }
    }
  }

  /* Pour la voie praticien, on dérive les axes principaux des besoins. */
  if (voie === "praticien") {
    const besoins = (answers["p-besoins"] as string[]) ?? [];
    if (besoins.includes("pb-preparation")) scores.autonomie += 2;
    if (besoins.includes("pb-interpretation")) scores.etats += 2;
    if (besoins.includes("pb-feedback")) scores.temporalite += 2;
    if (besoins.includes("pb-correspondances")) scores.liens += 2;
    if (besoins.includes("pb-limites")) scores.autonomie += 1;
    if (besoins.includes("pb-continuite")) scores.temporalite += 1;
  }

  const sorted: PortraitLayer[] = (Object.keys(scores) as DimensionKey[])
    .map((key) => ({
      key,
      label: DIMENSION_LABELS[key],
      score: scores[key],
    }))
    .filter((l) => l.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);

  /* Fallback : si aucun signal, proposer l'entrée territoire. */
  const layers: PortraitLayer[] =
    sorted.length > 0
      ? sorted
      : [
          { key: "territoire", label: DIMENSION_LABELS.territoire, score: 1 },
          { key: "etats", label: DIMENSION_LABELS.etats, score: 1 },
          { key: "autonomie", label: DIMENSION_LABELS.autonomie, score: 1 },
        ];

  const intensite = answers["intensite"] as string | undefined;
  const urgent = intensite === "i-5";

  return {
    voie,
    phrase: VOIE_PHRASES[voie],
    layers,
    urgent,
    cta: VOIE_CTA[voie],
  };
}
