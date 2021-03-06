from fabric.api import run, env, cd, sudo, get

KEY_FILENAME = '/home/james/.ssh/openstates_master.pem'

def staging():
    env.hosts = ['ubuntu@staging.openstates.org']
    env.key_filename = KEY_FILENAME

def production():
    env.hosts = ['ubuntu@openstates.org']
    env.key_filename = KEY_FILENAME

def update():
    sudo('cd ~openstates/src/openstates && git pull', user='openstates')
    sudo('cd ~openstates/src/billy && git pull', user='openstates')

def restart_uwsgi():
    sudo('restart uwsgi')

def restart_nginx():
    sudo('/etc/init.d/nginx restart')

def _venv(cmd):
    sudo('source ~openstates/site-venv/bin/activate && ' + cmd)

def get_leg_ids_csv(state):
    with cd('~openstates/src/openstates/'):
        _venv('billy-dump-missing-leg-ids ' +
              state)
        get('/ext/openstates/src/openstates/%s_missing_leg_ids.csv' % state,
            '%s_missing_leg_ids.csv' % state)
