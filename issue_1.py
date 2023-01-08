import postgres_login
from servers import Servers


servers = Servers(postgres_login.host, postgres_login.database, postgres_login.user, postgres_login.password)
servers.save()
