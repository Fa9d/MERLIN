# Tuto vidéo — App PRATICIEN / Console d'administration IVIA (version LONGUE)

> **Format cible** : capture d'écran + voix off. Durée estimée : **6 à 8 minutes**.
> **Colonne gauche = ACTIONS À L'ÉCRAN**. **Colonne droite = VOIX OFF**.
> Public : praticien·nes et administrateur·rices de la maison IVIA. Ton posé, précis, professionnel.
>
> **Note de périmètre** : ce tuto couvre la **console d'administration** (`/admin/*`), l'outil de gestion documenté de bout en bout. L'espace praticien clinique (`/praticien/*`) fait l'objet d'un tuto distinct à produire une fois ses écrans finalisés.

**Titre** : « La console IVIA — piloter la maison »
**Objectif** : montrer comment traiter les demandes, ouvrir un dossier, gouverner les analyses et suivre la comptabilité.

---

## Séquençage complet (tournage ↔ voix off)

### 00:00 — Ouverture
| À l'écran | Voix off |
|---|---|
| Page `admin/connexion.html` (« Accès réservé »). | « Voici la console d'administration d'IVIA — la porte réservée qui permet de piloter la maison : les comptes, les demandes, les analyses et la comptabilité. » |

### 00:15 — Connexion admin
| À l'écran | Voix off |
|---|---|
| Saisir courriel + mot de passe, cliquer « Entrer dans la console ». Arrivée sur `admin/index.html`. | « L'accès admin est distinct de la connexion standard : seuls les comptes autorisés entrent ici. Une fois connecté, on arrive sur la console — une grille de tuiles qui donne accès à chaque outil. » |

### 00:35 — Vue d'ensemble
| À l'écran | Voix off |
|---|---|
| Cliquer *Vue d'ensemble* (`vue.html`). Montrer les cartes-statistiques, puis la section « Alertes de vigilance ». | « La *Vue d'ensemble* donne l'état de la maison en un coup d'œil : nombre de comptes, courriels à vérifier, nouvelles demandes, encaissements du mois. En dessous, les *alertes de vigilance* — les situations qui appellent une attention humaine, qu'elles viennent des demandes ou des analyses. » |

### 01:20 — Demandes d'entrée
| À l'écran | Voix off |
|---|---|
| Cliquer *Demandes d'entrée* (`demandes.html`). Montrer une ligne, changer le Statut (menu déroulant), assigner un·e praticien·ne, écrire une note, cliquer « Enregistrer ». Pointer une ligne surlignée en rouge. | « Les *demandes d'entrée* réunissent les personnes arrivées par le seuil public. Pour chacune, on lit le besoin principal, on change le statut — nouvelle, à rappeler, contactée, planifiée, ou vigilance — on assigne un·e praticien·ne, et on ajoute une note de suivi. Les demandes urgentes sont surlignées : elles doivent être escaladées en priorité. » |

### 02:20 — Dossiers clients
| À l'écran | Voix off |
|---|---|
| Cliquer *Dossiers clients* (`dossiers.html`). Filtrer par nom, sélectionner un client. Montrer les cartes Activité/Suivi/Profil, déplier une transcription, montrer une analyse avec sa triade et son statut. | « Les *dossiers clients* réunissent, pour chaque personne, ses enregistrements, ses transcriptions et ses analyses. On filtre par nom ou courriel, on ouvre un dossier, et on retrouve tout : l'activité, le profil, les transcriptions dépliables, et les analyses présentées en triade — ce qui s'observe, une hypothèse, une orientation — avec leur statut, validée ou à valider. » |

### 03:30 — Comptes & accès
| À l'écran | Voix off |
|---|---|
| Cliquer *Comptes & accès* (`comptes.html`). Montrer le tableau, un menu Rôle, la case Admin. Montrer l'« Action groupée » (sans l'appliquer). | « *Comptes & accès* gère les inscriptions : vérification du courriel, rôles — client, praticien·ne, opérateur, superviseur, admin technique — et le droit d'administration. On peut aussi agir en lot : renvoyer un lien, vérifier, suspendre, réactiver. Des garde-fous empêchent de se suspendre ou se supprimer soi-même, et la suppression exige une double confirmation. » |

### 04:30 — Analyses & droits
| À l'écran | Voix off |
|---|---|
| Cliquer *Analyses & droits* (`analyses.html`). Montrer la matrice de capacités par profil (interrupteurs), pointer un badge « sort du serveur ». Puis la section « Reconnaissances professionnelles ». | « *Analyses et droits* gouverne l'exposition des capacités d'analyse selon le profil d'usage. Le moteur analyse toujours à pleine capacité ; ces vannes décident de ce qui est exposé. Un badge *sort du serveur* signale toute capacité qui envoie des données vers un service externe — à réévaluer avant mise en marché. En dessous, les *reconnaissances professionnelles* : un praticien vérifié accède aux inférences complètes, et le droit de transmettre au client exige la reconnaissance de l'instance appropriée. » |

### 05:30 — L'Atelier des lectures
| À l'écran | Voix off |
|---|---|
| Cliquer *Atelier des lectures* (`lectures.html`). Montrer un type de séance et ses interrupteurs Permise/Auto. Puis la section « Exercices » et le formulaire « Nouvel exercice ». | « *L'Atelier des lectures* raffine tout ça par type de séance : quelles lectures sont permises, lesquelles se déclenchent automatiquement après transcription. C'est aussi ici qu'on rédige les *exercices* — des pratiques sobres qu'un praticien peut proposer, jamais prescrire. Un filtre lié à la Loi 21 refuse tout terme non autorisé. » |

### 06:30 — Comptabilité & Économie IA
| À l'écran | Voix off |
|---|---|
| Cliquer *Comptabilité* (`comptabilite.html`), choisir un mois, montrer les cartes (HT, TPS, TVQ, marge) et le grand livre. Puis *Économie IA* (`economie.html`), montrer Bénéfice net et les tableaux par finalité/par séance. | « Côté finances, la *Comptabilité* ventile les encaissements réels — hors taxes, TPS, TVQ, frais Stripe, part praticien et marge IVIA — avec le grand livre détaillé, transaction par transaction. Les paiements de test sont exclus des totaux. Et l'*Économie IA* croise les coûts réels du modèle avec les revenus, par finalité d'analyse et par séance, pour suivre le bénéfice net en temps réel. » |

### 07:20 — Facturation & clôture
| À l'écran | Voix off |
|---|---|
| Cliquer *Facturation* (`facturation.html`), basculer une offre payant/gratuit. Retour à la console `index.html` + logo. | « Enfin, la *Facturation* permet de basculer chaque offre entre payant et gratuit — pratique pour tester un parcours sans paiement. Voilà la console IVIA : un poste de pilotage complet, où chaque décision reste sous regard humain. L'espace clinique du praticien, lui, reste entièrement distinct. » |

---

## Notes de tournage
- **Compte admin de démo** : utiliser un jeu de données test (demandes, comptes, transactions marquées « test ») — surtout ne jamais filmer de vraies données client.
- **Confidentialité** : flouter systématiquement noms, courriels et contenus de transcription réels.
- **Rythme** : la console est dense ; ralentir sur chaque écran, laisser le temps de lire les libellés.
- **Ordre logique** : suivre le flux naturel du travail (demande → dossier → analyse → compta), pas l'ordre de la barre latérale.
- **Séparation des rôles** : insister sur le fait que l'espace praticien clinique ne contient aucun outil d'admin.

## Rappel conformité (à mentionner si pertinent)
Loi 25 (renseignements personnels, données au Canada) · Loi 21 (vocabulaire professionnel encadré).
