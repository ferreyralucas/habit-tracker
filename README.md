# Django Template

### About this template:
- 🐳 Dockerized project.
- 💎 Integrated with Django Rest Framework.
- 🏮 Integrated with redis.
- 🍳 Integrated with celery.
- 📂 Integrated with postgres.
- ☁️ Integrated with boto3 and the according configuration to upload the static files to AWS.
- 🏥 Healthcheck configured.
- 💾 Logging configured.
- 🧹 Ready to be used with pre-commit, flake8 and isort.
- 🗃️ Requirements divided under three different categories: base, dev and test. This way allows you to only build what you need (e.g. only installing the base dependencies on a production environment).
- 🥤 Settings divided in three different files: base, dev and production. This way you can use unsecure configurations in a development environment that you don't are supposed to use in production.
- 🎈 To handle the states of your models without leaving a mess you can use the `FiniteStateMachine` class.

---

### How to use it:
- ♻️ Clone the repo and run it with `docker compose up`.
- 🎨 Create all your apps under the `apps` folder. Don't forget to add the corresponding urls under the `config/urls.py` file.
