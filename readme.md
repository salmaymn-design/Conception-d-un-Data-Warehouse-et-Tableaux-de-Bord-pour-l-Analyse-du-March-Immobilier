# 🏠 Darkom Data Warehouse Project

## 📌 Description

Ce projet consiste à construire un pipeline ETL complet pour les annonces immobilières de Darkom.ma.

Le flux de traitement est :

CSV → Staging → Clean → Data Warehouse → Power BI

---

## 📂 Structure du projet

```text
BRIEFS10/
│
├── data/
│   └── darkom_annonces.csv
│
├── staging/
│   └── load_raw.py
│
├── clean/
│   └── clean_raw.py
│
├── warhouse/
│   └── load_warhouse.py
│
├── .env
├── requirements.txt
├── main.py
└── README.md
```

---

## ⚙️ Technologies utilisées

- Python
- PostgreSQL
- Pandas
- SQLAlchemy
- Power BI
- DAX

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone <repository_url>
cd BRIEFS10
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer PostgreSQL

Créer la base de données :

```sql
CREATE DATABASE darkom_dwh;
```

---

## 🔐 Configuration

Créer un fichier `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=darkom_dwh
DB_USER=postgres
DB_PASSWORD=1234
```

---

## 📥 Étape 1 : Staging Layer

Chargement des données brutes depuis le fichier CSV :

```bash
python staging/load_raw.py
```

Table créée :

```text
staging.staging_darkom
```

---

## 🧹 Étape 2 : Clean Layer

Nettoyage des données :

- Suppression des doublons
- Gestion des valeurs nulles
- Détection des outliers
- Standardisation des données
- Création des variables dérivées

```bash
python clean/clean_raw.py
```

Table créée :

```text
clean.clean_darkom
```

---

## 🏗️ Étape 3 : Data Warehouse

Création du modèle dimensionnel :

- Dimensions
- Table de faits
- Relations

```bash
python warhouse/load_warhouse.py
```

Schéma créé :

```text
bi_schema
```

---

## ▶️ Exécution complète

Lancer tout le pipeline :

```bash
python main.py
```

---

## 📊 Dashboards Power BI

### Dashboard 1
Vue globale du marché immobilier

- Nombre total d'annonces
- Prix moyen
- Surface moyenne
- Répartition par ville
- Répartition par type de bien

### Dashboard 2
Analyse des prix

- Prix moyen
- Prix moyen par m²
- Catégories de prix
- Analyse par ville
- Analyse par type de bien

### Dashboard 3
Analyse géographique

- Carte du Maroc
- Prix moyen par ville
- Top quartiers

### Dashboard 4
Analyse des tendances

- Évolution des prix
- Croissance des annonces
- Analyse saisonnière

---

## 👩‍💻 Réalisé par

Salma EL Yamani

Projet Data Warehouse & Business Intelligence