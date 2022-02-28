import os
import uuid

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash

from app import db, create_app
from app.models.Permissions import Permissions
from app.models.Roles import Roles
from app.models.Users import Users

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    # print(Users.find_by_id(1).get_permissions())
    perm=Permissions.get_all_permission()
    user = Users(
        email="a.cherki@esi-sba.dz",
        uid=uuid.uuid4().hex[:10].upper(),
        password=generate_password_hash("1234567")
    )
    user.save()
    Roles().add(name='admin')
    user.attach_role('admin')
    for p in perm:
        Roles.get_by_name('admin').attach_permission(p)
    # Permissions.add(name='can do things', perm_name='can_do')
    # Roles.get_by_name('admin').attach_permission('can_do')


if __name__ == '__main__':
    manager.run()
