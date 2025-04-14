import contextlib
import subprocess
from functools import cached_property
from pathlib import Path

from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod


@register_action
class GradioAction(Action):
    name = 'gradio'
    category = PluginCategory.NEURAL_NET
    method = RunMethod.JOB

    @property
    def working_directory(self):
        dir = Path.cwd() / self.config['directory'].replace('.', '/')
        assert dir.is_dir(), f'Working directory {dir} does not exist.'
        return dir

    @property
    def _requirements(self):
        return self.config.get('requirements', ['gradio>=5'])

    @property
    def tag(self):
        _tag = f'{self.plugin_release.code}-{self.plugin_release.checksum}'
        return _tag.replace('@', '-')

    @cached_property
    def deploy_port(self):
        return self._get_avail_ports_host()

    def deploy(self):
        self.run.log('deploy', 'Start deploying')

        try:
            # Write Dockerfile and requirements.txt
            path_dockerfile = self.write_dockerfile_template()
            self.write_requirements(path_dockerfile.parent / 'requirements.txt')

            # Build docker image
            self.build_docker_image(path_dockerfile)

            # Run docker image
            self.run_docker_image()
        except Exception as e:
            self.run.log('deploy', f'Error: {e}')
            raise e

    def start(self):
        self.deploy()
        return {'endpoint': f'http://localhost:{self.deploy_port}'}

    def write_dockerfile_template(self):
        dockerfile_path = self.working_directory / 'Dockerfile'

        with open(dockerfile_path, 'w') as f:
            f.write("""FROM python:3.10
WORKDIR /home/user/app

RUN pip install --no-cache-dir pip -U && \\
    pip install --no-cache-dir uvicorn

RUN apt-get update && \\
    apt-get install -y curl && \\
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \\
    apt-get install -y nodejs && \\
    rm -rf /var/lib/apt/lists/* && \\
    apt-get clean

COPY . /home/user/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["python", "app.py"]
""")
        return dockerfile_path

    def write_requirements(self, path):
        with open(path, 'w') as f:
            f.write('\n'.join(self._requirements))

    def build_docker_image(self, path_dockerfile):
        self.run.log('deploy', 'Start building docker image')
        result = subprocess.run(
            [
                'docker',
                'build',
                '-t',
                self.tag,
                '-f',
                str(path_dockerfile),
                '.',
            ],
            cwd=self.working_directory,
            check=True,
        )
        print(result)

    @staticmethod
    def _get_avail_ports_host(start_port=8900, end_port=8999):
        import nmap

        nm = nmap.PortScanner()

        scan_range = f'{start_port}-{end_port}'
        nm.scan(hosts='host.docker.internal', arguments=f'-p {scan_range}')

        try:
            open_ports = nm['host.docker.internal']['tcp'].keys()
            open_ports = [int(port) for port in open_ports]
        except KeyError:
            open_ports = []

        for port in range(start_port, end_port + 1):
            if port not in open_ports:
                return port

        raise IOError(f'No free ports available in range {start_port}-{end_port}')

    def run_docker_image(self):
        self.run.log('deploy', 'Start running docker image')

        # Check for existing container
        self.run.log('deploy', 'Check for existing container')
        with contextlib.suppress(subprocess.CalledProcessError):
            subprocess.run(['docker', 'stop', self.tag], check=True)
            subprocess.run(['docker', 'rm', self.tag], check=True)

        # Run docker image
        self.run.log('deploy', 'Starting docker container')
        subprocess.run(
            [
                'docker',
                'run',
                '-d',
                '--name',
                self.tag,
                '-p',
                f'{self.deploy_port}:7860',
                self.tag,
            ],
            check=True,
        )
