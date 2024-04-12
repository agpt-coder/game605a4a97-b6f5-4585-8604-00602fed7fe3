---
date: 2024-04-12T15:37:22.571413
author: AutoGPT <info@agpt.co>
---

# game

Based on the information gathered through our interactions, the vision for the game is detailed as follows: The game is conceptualized as a strategy genre experience, appealing greatly to those interested in critical thinking, planning, and overcoming challenges. Set within a rich medieval fantasy world, this setting allows for immersion in a realm of knights, dragons, and epic quests, providing an escape into a world filled with magic, lore, and historical aesthetics. The gameplay mechanics are envisioned to include both custom character creation and in-game purchases, enhancing player engagement through personalization and offering additional content for an enriched gaming experience. From a technical standpoint, the game will leverage a tech stack consisting of Python and FastAPI for efficient and fast backend services, PostgreSQL for reliable data storage and complex queries, and Prisma ORM for streamlined database operations, all prioritizing performance, security, and scalable architecture. Targeting a broad audience, the game aims to connect players of varying ages, fostering shared experiences among friends and family across generations via engaging gameplay that transcends typical generational divides. Focused on the mobile platform, the game capitalizes on accessibility and innovative gameplay mechanics specific to touch interfaces and mobile devices' portability. This comprehensive project embodies a strategic and immersive gaming experience that reaches a wide audience through its captivating medieval fantasy theme, innovative gameplay, and accessible mobile platform.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'game'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
