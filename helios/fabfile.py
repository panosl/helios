set(
	fab_hosts = ['login.solhost.org'],
	fab_host = 'login.solhost.org',
	fab_port = '6114',
	fab_user = 'phaethon',

	app_name = 'helios',
	repo = '/var/www/phaethon/bzr/helios',
	branch = '/var/www/phaethon/checkouts',
)


def bzr_checkout():
	run('cd $(branch); bzr co $(repo) $(app_name)')

def bzr_push():
	local('bzr push sftp://$(fab_user)@$(fab_host):$(fab_port)/$(repo)')

def bzr_pull():
	run('cd $(branch)/$(app_name); bzr pull $(repo)')

def symlink():
	run('cd /var/www/phaethon/python-local/; ln -s /var/www/phaethon/checkouts/$(branch)/$(app_name)/$(app_name)/ $(app_name)')

def initial_deploy():
	bzr_push()
	bzr_pull()
	symlink()

def deploy():
	bzr_push()
	bzr_pull()
