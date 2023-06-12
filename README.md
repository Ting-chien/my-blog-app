# my-blog-app

## Prequisite

```bash
pip install --upgrade pip
```

## Installation

```bash
$ pip install -U pip
$ pip install -r requirements.txt
```

## Usage

```bash
$ flask run
```

## Migration

1. Init migration

```bash
$ flask db init
```

2. Generate migrate script

```bash
$ flask db migrate -m "Migrate message"
```

3. Upgrade database

```bash
$ flask db upgrade
```