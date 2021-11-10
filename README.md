# Teckzite 2020 admin panel
Web site used as Admin panel in Teckzite 2020 (Feb 13-15).

**Teckzite :** A national level tech fest conducted by [SDCAC](https://intranet.rguktn.ac.in/sdcac/) in [RGUKT Nuzvid](https://rguktn.ac.in/).

## Requirements :
1. Linux (ubuntu)
2. Python 3
3. MySQL

## Setup :
1. `pip install -r requirements.txt`
2. Configure the panel/config.py
3. Creating Database (tz2020) on mysql
4. Edit the line 47 on tz2020-schema.sql
```mysql
INSERT INTO `admins` VALUES (1,'<User name>','<Password Hash>','<Name>','<Mail Address>','<Phone num>','<ID num>',0,'',0);
```
To generate a password hash
```py
from panel.funcs import Hash
print(Hash('<password>'))
```
5. Then dump the sql file into created database.
6. Save the ssl certicate and private key as `certificate.crt` and `private.key`
7. `./run_server.sh`
8. `./run_server.sh --temp` for Site under construction message, in case of any edits.

## Notes
1. After creating the dev account using line 4 in `setup`, Then with that `dev account` ,we create the hierarchy (admin, event org, etc)
2. `dev account` with priority 0 , have all core functionalities. It is only for web site managers. Others can have admin account.

## Designed by
1. Ajay Shankar K {me} [github](https://github.com/D1r3Wolf/) [twitter](https://twitter.com/D1r3Wolf_)
2. Akash G {Sud0u53r} [github](https://github.com/Sud0u53r/) [twitter](https://twitter.com/Sud0u53r)
