# [INF6150 - Génie logiciel: conduite de projets informatiques](https://etudier.uqam.ca/cours?sigle=INF6150)-E23 - UNIVENT

![Version](https://img.shields.io/badge/version-hiver2023-success?style=flat)
![License](https://img.shields.io/badge/license-Apache2.0-green?style=flat)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=Python&logoColor=white)
![Version](https://img.shields.io/badge/version-3.9|3.10-3776AB?style=flat&)
![JavaScript](https://img.shields.io/badge/AJAX-JavaScript-F7DF1E?style=flat&logo=JavaScript&logoColor=white)
![Flask](https://img.shields.io/badge/framework-Flask-000000?style=flat&logo=Flask&logoColor=white)
![SQLite3](https://img.shields.io/badge/db-SQLite3-003B57?style=flat&logo=SQLite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/CSS-Bootstrap-7952B3?style=flat&logo=Bootstrap&logoColor=white)

#### Auteurs :

- Oussama EL-FIGHA | ELFO74030209
- Nicolas Plante | PLAN83020108
- Neil Ridene | RIDN30129504
- Keven Jude Anténor | ANTK08129003
- Adje, Kouassi Emmanuel | ADJK19049905
- Djaha Hermann | DJAM21128107

#### Product Owner :

- Éric Lavallée | lavallee.eric@uqam.ca

#### Courriels :

- el-figha.oussama@courriel.uqam.ca
- ridene.neil@courrier.uqam.ca
- adje.kouassi_emmanuel@courrier.uqam.ca
- antenor.keven_jude@courrier.uqam.ca
- plante.nicolas.4@courrier.uqam.ca
- djaha.monemon_junior_hermann@courrier.uqam.ca

## **📝 Titre et description du projet**

### UNIVENT

Ce projet vise à développer une plateforme web dédiée à l'UQAM et ses
associations étudiantes, inspirée de sites tels qu'Eventbrite ou Ticketmaster.
L'objectif principal est de permettre aux étudiants et au personnel de
l'université de créer, de promouvoir et de vendre des billets pour une variété
d'événements universitaires. Cela comprend, des conférences, des ateliers, des
concerts, des événements sportifs et des réunions sociales. La plateforme
fournira un espace centralisé pour tous les événements liés à l'UQAM,
améliorant ainsi la visibilité et l'accessibilité pour tous les membres de la
communauté universitaire.

## 🌀 Clone du projet

Si vous voulez cloner le projet à partir de Gitlab, suivez les instructions
suivantes :

1. Assurez-vous que Git est installé sur votre ordinateur. Si ce n'est pas le
   cas, vous pouvez le télécharger et l'installer depuis le site officiel de
   Git : [Git - Downloads](https://git-scm.com/downloads)
2. Ouvrez votre terminal ou votre invite de commande.
3. Accédez au répertoire dans lequel vous souhaitez cloner le projet en
   utilisant la commande "cd" (change directory) :
4. Clonez le projet en utilisant la commande "git clone" suivie de l'URL du
   dépôt :

```bash
git clone https://gitlab.info.uqam.ca/ridene.neil/univent.git
```

5. Patientez jusqu'à ce que le clonage soit terminé.

Une fois que le clonage est terminé, vous devriez avoir une copie locale du
projet sur votre ordinateur.

## 📋 Prérequis

Pour installer et exécuter cette application Flask, vous aurez besoin de :

- Python 3.9 ou version ultérieure
- Flask et ses dépendances

## 🔧 Installation

### Activation de l'environnement virtuel

1. Ouvrez un terminal ou une invite de commande.

2. Accédez au répertoire de votre projet cloné en utilisant la commande `cd`

3. Assurez-vous d'avoir Python 3 installé sur votre machine en exécutant la
   commande suivante :

   ```bash
   python3 --version
   ```

   Si vous n'avez pas Python 3 installé, vous pouvez le télécharger à partir du
   site
   officiel : [Download Python | Python.org](https://www.python.org/downloads/)

4. Installez le package `virtualenv` si vous ne l'avez pas déjà. Cela vous
   permettra de créer des environnements virtuels. Exécutez la commande
   suivante :

   ```bash
   pip install virtualenv
   ```

   ou

   ```bash
   pip3 install virtualenv
   ```

5. Créez un nouvel environnement virtuel dans le répertoire de votre projet.
   Exécutez la commande suivante :

   ```bash
   python -m venv venv
   ```

   ou

   ```bash
   python3 -m venv venv
   ```

   Cela créera un nouvel environnement virtuel appelé "**venv**" dans votre
   dossier de projet.

6. Activez l'environnement virtuel. La méthode d'activation varie en fonction
   du système d'exploitation :

    - Sur Windows :

      ```powershell
      venv\Scripts\activate
      ```

    - Sur macOS et Linux :

      ```bash
      source venv/bin/activate
      ```

   Une fois l'environnement virtuel activé, votre invite de commande devrait
   indiquer le nom de l'environnement virtuel, par exemple `(venv)`.

### Installation des dépendances

Installez les dépendances du projet à l'aide du fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

Maintenant, votre environnement virtuel est prêt et vous pouvez commencer à
développer ou à exécuter votre application Flask. N'oubliez pas de désactiver
l'environnement virtuel lorsque vous avez terminé en exécutant la
commande `deactivate`.

### Partir l'App

1. Assurez-vous que l'environnement virtuel que vous avez créé est activé. Si
   ce n'est pas le cas, activez-le en suivant les instructions précédente.

2. Définissez la variable d'environnement `FLASK_APP` pour indiquer à Flask le
   fichier qui contient votre application. Le fichier principal de mon
   application Flask est nommé `app.py`.

    * Sur Windows :

      ```powershell
      set FLASK_APP=app.py
      ```

    * Sur macOS et Linux :

      ```bash
      export FLASK_APP=app.py
      ```

3. Enfin, démarrez votre application Flask en exécutant la commande suivante :

   ```bash
   flask run
   ```

### Tests dans un fureteur

1. Flask démarrera un serveur de développement local et affichera l'URL à
   laquelle l'application est accessible, généralement `http://127.0.0.1:5000/`
   ou `http://localhost:5000/`.
2. Ouvrez un navigateur web et accédez à l'URL affichée pour voir l'application
   Flask en fonctionnement.

### Informations pour developpeurs

DockerHub : https://hub.docker.com
username : univentuqam
mdp : qeKKPE*e#yF6ha

