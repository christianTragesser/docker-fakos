import os
from argparse import ArgumentParser
from pyplineCI import Pipeline

dirPath = os.path.dirname(os.path.realpath(__file__))
buildPath = dirPath+'/src/'
pipeline = Pipeline(dockerRegistry='registry.gitlab.com/christiantragesser')
localTag = 'local/fakos'

def ci(option):
    stage = {
        'test': test,
        'scan': securityScan,
        'local': local
    }
    run = stage.get(option, test)
    run()

def test():
    testDir = '/tmp/docker/test'
    volumes = {
        dirPath: { 'bind': '/tmp', 'mode': 'rw'}
    }
    print('Starting tests:')
    pipeline.runi(image=pipeline.dockerRegistry+'/pypline-ci:fakos',
                                     name='fakos-test', working_dir=testDir, volumes=volumes, command='pytest')
    pipeline.build_image(buildPath, localTag)
    print('Testing complete')

def securityScan():
    print('Starting security scans:')
    pipeline.cve_scan(localTag)

def local():
    volumes = {
        dirPath: { 'bind': '/tmp', 'mode': 'rw'}
    }
    print('Initializing locally built instance:')
    pipeline.build_image(buildPath,localTag)
    pipeline.runi(image=localTag,
                                     name='fakos-local', working_dir='/tmp', volumes=volumes, command='/bin/sh')

def main():
    parser = ArgumentParser(prog='ci-py')
    parser.add_argument('stage', type=str,
                        help='run pipeline stage; test, scan, local')
    args = parser.parse_args()
    ci(args.stage)

if __name__ == '__main__':
    main()