set(
	fab_hosts = ['192.168.2.44'],
	fab_user = 'root',

	app_name = 'helios',
	repo = '/var/www/phaethon/bzr/helios',
	branch = '/var/www/phaethon/checkouts/helios',
)


def bzr_checkout():
	run('cd $(branch); bzr co $(repo)')

def bzr_push():
	local('bzr push sftp://%s@%s//var/www/phaethon/bzr/helios' % ('root', '192.168.2.44'))

def bzr_pull():
	run('cd $(branch); bzr pull $(repo)')

def reboot():
	run('apachectl -k graceful')

def deploy(initial=False):
	bzr_push()
	bzr_pull()
	reboot()
