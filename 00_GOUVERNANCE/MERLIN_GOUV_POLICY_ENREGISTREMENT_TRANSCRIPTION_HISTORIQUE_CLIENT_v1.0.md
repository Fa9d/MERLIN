# MERLIN - Politique enregistrement transcription historique client (v1)

Date: 2026-04-19
Statut: draft
Objet: definir ce que MERLIN peut enregistrer, transcrire, conserver et relire dans les seances clients sans glisser vers un pseudo-dossier clinique non gouverne

---

## 1) Principe directeur

MERLIN doit traiter l'enregistrement, la transcription et l'historique client comme des operations a risque.

Le risque n'est pas seulement technique.
Il est aussi:
- ethique;
- juridique;
- reputionnel;
- operationnel;
- epistemique.

Risque principal:

`si MERLIN conserve trop, il peut se retrouver a fabriquer un quasi-dossier clinique sans cadre professionnel, sans necessite reelle, et avec une masse de donnees sensibles disproportionnee.`

Decision de base:

`MERLIN conserve moins que ce qu'il pourrait techniquement conserver.`

---

## 2) Hierarchie de capture

MERLIN distingue trois niveaux de capture.

### Niveau A - Note structur ee

C'est le niveau par defaut.

Contenu:
- motif principal;
- drapeaux rouges oui/non;
- niveau de risque percu;
- besoin dominant;
- orientation recommandee;
- limites rappelees;
- prochaine action.

Doctrine:

`Par defaut, MERLIN conserve une note structuree, pas un verbatim complet.`

### Niveau B - Transcription texte

C'est un niveau exceptionnel.

Autorisation:
- seulement si une utilite claire est definie;
- seulement avec consentement explicite;
- seulement si la politique de retention est claire.

Doctrine:

`Une transcription complete ne doit pas etre le mode de conservation par defaut.`

### Niveau C - Enregistrement audio / video brut

C'est le niveau le plus sensible.

Autorisation:
- uniquement sur base de consentement explicite distinct;
- uniquement si la finalite est forte et definie;
- uniquement avec stockage, acces et suppression gouvernes.

Doctrine:

`L'enregistrement brut doit etre l'exception, pas la norme.`

---

## 3) Politique recommandee par defaut

Je recommande pour MERLIN:

1. `pas d'enregistrement audio ou video par defaut`
2. `pas de transcription complete par defaut`
3. `note de seance structuree par defaut`
4. `historique client limite aux elements utiles a la continuite`

Autrement dit:

`memoire utile oui`

`surcaptation non`

---

## 4) Consentement

MERLIN doit distinguer trois consentements differents.

### Consentement 1 - Consentement a la seance

La personne accepte:
- la nature de la rencontre;
- les limites de MERLIN;
- le fait qu'il ne s'agit pas d'un acte clinique reserve.

### Consentement 2 - Consentement a la note

La personne comprend que MERLIN garde:
- une note breve de seance;
- orientee vers la continuite;
- et non un verbatim integral.

### Consentement 3 - Consentement a l'enregistrement / transcription

Ce consentement doit etre distinct, explicite et separable.

Il doit dire clairement:
- ce qui est enregistre;
- pourquoi;
- pour combien de temps;
- qui y a acces;
- comment la suppression fonctionne.

Regle:

`Aucun enregistrement ou transcription integrale ne doit reposer sur un consentement implicite ou flou.`

---

## 5) Ce qui doit etre conserve dans l'historique client

L'historique client MERLIN ne doit pas etre un journal total.

Il doit rester centre sur la continuite utile.

Champs recommandes:
- identifiant client;
- date de seance;
- type de seance;
- motif principal;
- drapeaux rouges oui/non;
- niveau de risque percu;
- besoin dominant;
- orientation recommandee;
- prochaine action;
- alertes de bascule si aggravation;
- date de derniere mise a jour.

Peut aussi etre conserve si necessaire:
- preferences de communication;
- ressources deja essayees;
- refus explicites de certaines portes d'entree;
- facteurs pratiques majeurs comme cout, transport, acces.

Ne doit pas etre conserve par defaut:
- details intimes sans utilite de continuite;
- verbatim emotionnel complet;
- confidences non utiles au parcours;
- speculation operateur;
- theorie personnelle sur la personne.

---

## 6) Regle de minimisation

Chaque element conserve doit repondre a cette question:

`Est-ce que cette information sera utile a la continuite, a la securite ou a la qualite de l'orientation?`

Si la reponse est non:
- ne pas la conserver.

Si la reponse est peut-etre:
- preferer une note plus courte.

---

## 7) Dur ees de retention recommandees

Je recommande de distinguer trois couches.

### A. Audio / video brut

Retention recommande e:
- tres courte;
- ou pas de conservation du tout;
- suppression rapide apres transformation en note utile.

Doctrine recommandee:

`si audio ou video existe, il doit etre supprime rapidement apres production de la note ou de la transcription utile, sauf raison explicite et documentee de le conserver.`

### B. Transcription complete

Retention recommande e:
- courte a moyenne;
- seulement si justifiee;
- jamais illimitee par inertie.

### C. Note structuree et historique utile

Retention recommande e:
- plus longue;
- parce qu'elle sert a la continuite;
- mais avec revue periodique et purge des elements devenus inutiles.

Important:

`MERLIN ne doit pas confondre memoire de travail et conservation indefinie.`

---

## 8) Separation des couches

MERLIN doit separer:

1. `donnees de contact`
2. `notes de seance structurees`
3. `transcriptions exceptionnelles`
4. `enregistrements bruts`
5. `analytics et statistiques anonymisees`

Pourquoi:
- pour limiter l'acces;
- pour limiter les dommages si fuite;
- pour mieux gerer la suppression;
- pour eviter qu'un operateur lise plus que necessaire.

---

## 9) Acces et principe du besoin d'en connaitre

Tout le monde n'a pas besoin d'avoir acces a tout.

Principe:

`un operateur ne doit acceder qu'a ce qui est utile a la seance suivante et a la securite`

Par defaut:
- acces a la note structuree;
- pas d'acces systematique au brut;
- pas d'acces systematique a une transcription complete.

---

## 10) Historique client recommande

Je recommande un historique tres lisible, sous forme de fiche chronologique courte:

- date
- type de seance
- besoin dominant
- niveau de risque
- orientation donnee
- issue ou suivi connu

Exemple:

```text
2026-04-19 | standard | detresse anxieuse persistante | non urgent | psychologue via CLSC | en attente de demarche
2026-05-02 | standard | confusion de parcours | non urgent | 811 + preparation de demande | a recontacter si blocage
2026-05-10 | bascule urgence | idees suicidaires avec plan | critique | urgence psychiatrique | bascule immediate
```

Ce format suffit souvent beaucoup mieux qu'un dossier narratif massif.

---

## 11) Transcription: oui, mais pour quoi?

Une transcription complete n'est acceptable que si sa fonction est definie.

Fonctions admissibles possibles:
- supervision interne explicite;
- controle qualite;
- formation;
- retour au client si demande explicite;
- audit d'incident;
- extraction structuree vers note et historique.

Fonctions non admissibles:
- tout garder par confort;
- `au cas ou`;
- surveillance diffuse sans doctrine;
- accumulation non lue.

---

## 12) Enregistrement: doctrine prudente

Ma recommandation concrete pour MERLIN est la suivante:

### Option prudente forte

- pas d'enregistrement par defaut
- note structuree uniquement
- transcription seulement en cas special

### Option prudente intermediaire

- enregistrement possible uniquement si la personne consent explicitement
- conversion rapide en note
- suppression rapide du brut

Entre les deux, je recommande aujourd'hui:

`Option prudente forte`

Parce que votre cadre actuel est:
- premiere ligne;
- non clinique reservee;
- sensible;
- fonde sur la clarification et l'orientation.

Ce cadre ne justifie pas une captation maximale.

---

## 13) Ce que MERLIN doit dire au client

Formulation recommandee:

`Nous gardons une note breve et utile de la seance pour assurer la continuite et ne pas vous faire tout recommencer a chaque fois. Nous n'enregistrons pas ni ne transcrivons integralement par defaut. Si un enregistrement ou une transcription complete etait envisage, cela ferait l'objet d'un consentement explicite distinct.`

Si enregistrement exceptionnel:

`Avant d'enregistrer, je veux etre clair sur ce qui serait enregistre, pourquoi, pendant combien de temps, qui y aurait acces, et comment cela pourrait etre supprime. Rien n'est fait sans votre accord explicite.`

---

## 14) Le vrai danger a eviter

Le danger n'est pas seulement la fuite de donnees.

Le vrai danger est aussi:
- de transformer une seance d'orientation en dispositif de captation;
- de creer une illusion de dossier therapeutique;
- de stocker des details sensibles que vous ne devriez pas porter;
- de rendre le client dependant d'un historique trop intime;
- de rigidifier la relation par une memoire trop lourde.

---

## 15) Decision active

MERLIN adopte la doctrine suivante:

`Par defaut: note structuree, historique utile, pas d'enregistrement brut, pas de transcription complete.`

`Exception: enregistrement ou transcription seulement sur consentement explicite distinct, avec finalite, acces, retention et suppression definis.`

`Historique client: court, utile, centre sur continuite, securite et orientation, jamais pseudo-clinique.`
