# Push to GitHub - Quick Guide

## 3 commandes pour pusher le projet

### 1. Initialiser Git
```bash
cd "/home/bilal/Bureau/CloudSecOps-Scanner"

git init
git add .
git commit -m "Initial commit: CloudSecOps Scanner

Multi-cloud security scanning tool with:
- Python/FastAPI backend
- Docker containerization
- Terraform IaC for GCP
- GitHub Actions CI/CD
- Multi-cloud support (GCP/AWS/Azure)"
```

### 2. Créer le repository sur GitHub

**Option A - Avec GitHub CLI (recommandé):**
```bash
gh repo create CloudSecOps-Scanner --public --source=. --remote=origin --description "Multi-cloud security scanning and compliance automation tool"
```

**Option B - Manuellement:**
1. Allez sur https://github.com/new
2. Repository name: `CloudSecOps-Scanner`
3. Description: `Multi-cloud security scanning and compliance automation tool`
4. Public
5. Ne PAS initialiser avec README
6. Create repository

Puis:
```bash
git remote add origin https://github.com/5Otien/CloudSecOps-Scanner.git
git branch -M main
```

### 3. Push
```bash
git push -u origin main
```

---

## Vérifications avant de pusher

### Fichiers à vérifier
- [ ] README.md existe et est complet
- [ ] LICENSE existe (MIT)
- [ ] .gitignore est présent
- [ ] Pas de credentials dans le code
- [ ] requirements.txt à jour

### Test rapide
```bash
# Vérifier que Python fonctionne
python src/scanner.py --help

# Vérifier qu'il n'y a pas d'erreurs de syntaxe
python -m py_compile src/scanner.py
```

---

## Après le push

### Ajouter des badges au README
Une fois pushé, vous pouvez ajouter ces badges en haut du README:

```markdown
[![CI](https://github.com/5Otien/CloudSecOps-Scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/5Otien/CloudSecOps-Scanner/actions)
```

### Activer GitHub Actions
Les workflows GitHub Actions se lancent automatiquement au premier push.
Vérifiez: https://github.com/5Otien/CloudSecOps-Scanner/actions

### Créer un release (optionnel)
```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

---

## URL du repository

Après push, votre projet sera accessible à:
**https://github.com/5Otien/CloudSecOps-Scanner**

Ajoutez cette URL dans votre CV et portfolio !

---

## Commandes complètes (copier-coller)

```bash
cd "/home/bilal/Bureau/CloudSecOps-Scanner"

git init
git add .
git commit -m "Initial commit: CloudSecOps Scanner

Multi-cloud security scanning tool with:
- Python/FastAPI backend
- Docker containerization
- Terraform IaC for GCP
- GitHub Actions CI/CD
- Multi-cloud support (GCP/AWS/Azure)"

gh repo create CloudSecOps-Scanner --public --source=. --remote=origin --description "Multi-cloud security scanning and compliance automation tool"

git push -u origin main

echo "✅ Projet pushé sur GitHub !"
echo "URL: https://github.com/5Otien/CloudSecOps-Scanner"
```
