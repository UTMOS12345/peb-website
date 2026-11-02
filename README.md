# peb-website

> The website of PEB Union, a student-led Politics, Economics and Business club at Al-Beruni International Boarding School.

peb-website is a Flask app with the club's public pages (news, articles, interviews, activities, staff, charter) and a small admin panel where club members log in to write and publish posts. Posts are written in Markdown and saved as drafts until they're published.

## Table of Contents

- [Background](#background)
- [Features](#features)
- [Install](#install)
- [Usage](#usage)
- [Project structure](#project-structure)
- [Roadmap](#roadmap)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

PEB Union runs Model UN, peer support, a market simulation and other activities, and publishes news and articles by its members. The club needed one place for all of this that members can update themselves, without editing HTML.

## Features

- **Public pages:** home, about, staff, charter, news, articles, interviews, activities, MUN, peer support, market simulation, contact
- **Posts:** news, articles and interviews written in Markdown (rendered with `markdown2`), with an image or video and a draft/published status
- **Admin panel:** log in, then add, edit and delete posts and staff members
- **Roles:** `admin`, `manager` and `researcher`, each with different permissions
- **JSON API:** `/api/content` and `/api/staff`, which the front-end JavaScript uses to build the pages

## Install

### Dependencies

- Python 3.10+
- SQLite (built into Python)

### Setup

```bash
git clone https://github.com/UTMOS12345/peb-website
cd peb-website
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python seed.py        # creates the database and the admin, manager and researcher accounts
python seed_staff.py  # adds the staff list
```

Change the default passwords in `seed.py` before you run it on a real server.

## Usage

```bash
flask --app app run
```

Open http://127.0.0.1:5000. The admin panel is at `/login`, then `/admin/manage`.

| URL | Page |
|---|---|
| `/` | Home |
| `/news`, `/articles`, `/interviews` | Post lists |
| `/news/<id>` | A single post |
| `/staff`, `/about`, `/charter` | Club information |
| `/activities`, `/mun`, `/peer-support`, `/market-simulation` | Activities |
| `/contact` | Contact |
| `/admin/manage` | Admin dashboard (login required) |

## Project structure

| Path | Role |
|---|---|
| `app.py` | Flask app: `User`, `Staff` and `Post` models, routes, login and role checks |
| `seed.py`, `seed_staff.py` | Create the database, user accounts and staff list |
| `templates/` | Jinja templates for every page and the admin panel |
| `static/js/` | Per-page scripts (`page-news.js`, `page-staff.js`, …) that load data from the API |
| `static/css/styles.css` | Site styles |
| `static/img/` | Logos and background image |

## Roadmap

- [ ] Move `SECRET_KEY` out of `app.py` into an environment variable
- [ ] Remove `static/css/styles.css.bak` from the repo
- [ ] Image uploads in the editor instead of pasting image URLs
- [ ] Search and category filters on the news and articles pages
- [ ] An events calendar for MUN and other activities
- [ ] Send the contact form to the club's email or Telegram
- [ ] Uzbek and Russian versions of the site
- [ ] Deploy with a production server (gunicorn) and a real domain

## Maintainers

[@UTMOS12345](https://github.com/UTMOS12345)

## Contributing

Club members can report problems or suggest pages in [Issues](https://github.com/UTMOS12345/peb-website/issues).

## License

No license has been chosen yet. Until one is added, all rights are reserved © Imomaliyev Maksudali.
