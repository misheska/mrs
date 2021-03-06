import os
import os.path
import subprocess

from crudlfap.management.commands.dev import signal, Command  # noqa


def webpackwatch(sender, **kwargs):
    watch = '.npm-watch.pid'

    if os.path.exists(watch):
        with open(watch, 'r') as f:
            pid = f.read().strip()

        if pid:
            pid = int(pid)
            if os.path.exists('/proc/{}'.format(pid)):
                os.kill(pid, 9)

        os.unlink(watch)

    npmroot = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../' * 4))

    process = subprocess.Popen(['npm start -- --watch'],
                               shell=True,
                               cwd=npmroot)
    with open(watch, 'w+') as f:
        f.write(str(process.pid))
signal.connect(webpackwatch)
