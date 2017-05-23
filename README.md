A mirror of JR Train status on Google App Engine
====================

https://jr-delay.appspot.com/


Deploy
--------------------
```bash
git clone https://github.com/curipha/gae-jr-delay.git
cd gae-jr-delay/
gcloud --quiet datastore create-indexes index.yaml
gcloud --quiet app deploy app.yaml cron.yaml
```

### Snippets for developing

#### Remove unused datastore indexes
```bash
gcloud --quiet datastore cleanup-indexes index.yaml
```

#### Deploy new version
```bash
gcloud --quiet app deploy
```

#### Deploy new cron
```bash
gcloud --quiet app deploy cron.yaml
```

Icon
--------------------
`train.png` and `train_b.png` is originally distributed at [Material icons - Material Design](https://material.io/icons/#ic_train) under the Apache License Version 2.0.

`www/favicon.ico` is created from `train_b.png`.
