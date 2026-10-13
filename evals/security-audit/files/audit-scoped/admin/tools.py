import os


def backup(request):
    os.system(f"tar czf /backups/{request['form']['name']}.tgz /srv/data")
