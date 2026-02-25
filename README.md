# Resumer rapidement ses fichiers grâce à l'IA

# Installation

```
git clone "https://github.com/OscarPARDON/AI_Doc_Summarizer"
cd AI_Doc_Summarizer
```

Puis dans *backend/settings.py*, trouvez la constante APIKEY et renseignez-y une clé API Genia (Google). \
[Obtenir une clé API GenIA gratuitement](https://aistudio.google.com/api-keys)

Une fois cela effectué, démarrez l'application

```
docker compose up
```

# Démonstration

## Etape 1 : Ajouter son document 
Ajoutez votre document par glisser déposer, ou en cliquant à l'endroit indiqué pour ouvrir l'explorateur de fichier.
Une notification située en bas à droite vous informera du bon déroulement de l'opération.

## Etape 2 : Attendez votre resumé 
En parallèle, le volet latéral va s'ouvrir, attendez un instant pour y trouver votre fichier. Cliquez ensuite simplement sur l'onglet de votre fichier pour l'ouvrir.

## Etape 3 : Consultez votre résumé 
Une fois le chargement terminé, le resumé complet s'affichera devant vos yeux.
Vous trouverez alors de nombreuses informations utiles sur le documents tel que un résumé rapide, la langue d'origine, le type de document et des mots clés.

<img width="1025" height="632" alt="Exemple de resumé" src="https://github.com/user-attachments/assets/4f2bc152-18f5-4a0d-b004-98ccc85f18ba" />

*Exemple de resultat obtenu pour le pdf du* [rapport de Deutsche Bank sur les préoccupations récentes liées à l'IA](https://prod1.www.dbresearch.com/PROD/RI-PROD/PDFVIEWER.calias?pdfViewerPdfUrl=PROD0000000000618988&rwnode=REPORT).


# Technologies

* Environement Frontend : VueJS
  * Gestion des stores : Pinia
  * Requêtes API : Axios
  * Gestion [TUS](https://tus.io/) côté client : Tus-js-client
    
* Environnement Backend : FastAPI
  * Gestion de la base de donnée : Sqlite3
  * Gestion de [TUS](https://tus.io/) côté server : tuspyserver
  * Detection des extensions fichiers : libmagic1 
  * Librairie pour lecture des PDF : pypdf
  * Librairie pour lecture des Html : BeautifulSoup
  * Librairie pour lecture des docx : docx
  * Librairie pour lecture des emails : email
  * Intégration IA : genia (Intégration Python d'API vers gemini)

 # Améliorations

 Ceci n'étant qu'un prototype réalisé rapidement, de nombreuses améliorations sont nécéssaires, voici les principales :
 * Réduction des dépendances
 * Mise en place d'un volume docker pour la redondance des données et d'un système de base de donnée plus robuste.
 * Amélioration  de la sécurité (Authentification, Config middleware, ...)
 * Implémentation d'une solution IA pro
 * Logging avancé et gestion des erreurs
 * Création de tests

# Process
La logique détaillé derrière le traitement des fichiers.

## Etape 1 : Récupération et envoi du fichier
Un ecouteur détécte les changements sur le input type file, si un nouveau fichier y est placé, le fichier est passé au service d'Upload avec TUS.

```
export default function uploadFile(file, options = {}) {
  const { onSuccess, onError, onProgress } = options;
  
  var upload = new tus.Upload(file, {
    endpoint: 'http://localhost:8000/files/',
    retryDelays: [0, 3000, 5000, 10000, 20000],
    metadata: {
      filename: file.name,
      filetype: file.type,
    },
    onError: function (error) {
      console.log('Upload Failure: ' + error);
      if (onError) onError(error);
    },
    onProgress: function (bytesUploaded, bytesTotal) {
      var percentage = ((bytesUploaded / bytesTotal) * 100).toFixed(2);
      console.log(bytesUploaded, bytesTotal, percentage + '%');
      if (onProgress) onProgress(percentage);
    },
    onSuccess: function () {
      const jobStore = useJobStore();
      const urlStr = upload.url;
      const uuid = new URL(urlStr).pathname.split('/').filter(Boolean).pop();
      
      jobStore.savePendingJob(uuid, "En cours de traitement : Document importé avec succès", upload.file.name);
      console.log('Download %s from %s', upload.file.name, upload.url);
      
      if (onSuccess) onSuccess(uuid);
    },
  });
  
  upload.start();
}
```
Ce service permet plusieurs choses :
* Envoyer le fichier de manière propre (creation d'un uuid, chunking, retry)
* Suivre le déroulement de l'Upload
* Déclencher le comportement adapté (Reussite ou erreur)

Le service va communiquer avec la couche TUS côté server : tuspyserver \
Il sagit d'un router FastAPI, modifié pour pouvoir traiter les requêtes TUS. \
Il va compléter la couche TUS côté frontend, en s'assurant que le fichier est bien reçu et enregistré dans un répértoire temporaire.
Tout comme du côté frontend, c'est lui qui va déclencher la suite du traitement si l'upload est un succès.

```
tus_router = create_tus_router(
    files_dir="/tmp/files", # path to store files
    max_size=128_000_000, # max upload size in bytes (128mo)
    days_to_keep=1, # retention period
    on_upload_complete= on_upload_complete # function triggered when the upload is completed
)
```

## Etape 2 : Traitement du fichier et polling

**Côté backend :**\
Le router TUS déclenche la suite du traitement.
Un 'job' de traitement du fichier va alors être créé avec un ID unique, il sera mis à jour au fur et à mesure du traitement du fichier (scrapping du contenu, traitemnt du contenu par IA).
Ce job contient des informations sur le status du traitement, puis le resultat du traitement lorsque celui-ci arrive à son terme.
Un endpoint permet de suivre le status, et de récupérer le resultat des jobs.

```
@jobs_router.get("/{job_id}")
async def follow_job_status(job_id: str):
    db_cnx = sqlite3.connect(DBDIR)
    db_cnx.row_factory = sqlite3.Row

    job = get_job(db_cnx, uuid=job_id)
    db_cnx.close()

    if job:
        return JSONResponse(status_code=HTTP_200_OK, content={
            "uuid": job["uuid"],
            "status": job["status"],
            "result": job["result"]
        })

    return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": "Job not found"})

```

**Côté frontend :**\
Le traitement du fichier va être ajouté dans la liste des 'jobs' en cours. Un service réalise régulièrement des requêtes pour mettre à jour le status du job (Polling), jusqu'a qu'il obtienne le resutat du traitement du fichier. Le job est alors déplacé dans la liste des jobs terminés et son resultat peut être affiché.

```
startPendingJobsPolling(intervalMs = 10 * 1000) {
      if (intervalId) clearInterval(intervalId);
      this.pendingJobsRefresh();
      intervalId = setInterval(() => {
        this.pendingJobsRefresh();
      }, intervalMs);
    },

    stopPendingJobsPolling() {
      if (intervalId) clearInterval(intervalId);
    }
  }
});
```
