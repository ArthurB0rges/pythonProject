from flask_sqlalchemy import SQLAlchemy

# Aula 11 (revisão do ORM) — Os modelos compartilham esta instância, ligada ao Flask em create_app().
db = SQLAlchemy()
