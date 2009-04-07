set(
	fab_hosts = ['192.168.2.44'],
	fab_user = 'panos',

	app_name = 'helios',
	repo = '/var/www/phaethon/bzr/helios',
	branch = '/var/www/phaethon/checkouts/helios',
)


def bzr_checkout():
	run('cd $(branch); bzr co $(repo)')

def bzr_push():
	local('bzr push sftp://$(fab_user)@%s//var/www/phaethon/bzr/helios' % ('192.168.2.44',))

def bzr_pull():
	run('cd $(branch); bzr pull $(repo)')

def reboot():
	sudo('apachectl -k graceful')

def deploy():
	bzr_push()
	bzr_pull()
