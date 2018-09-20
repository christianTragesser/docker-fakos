#!/usr/bin/python3
import os
from argparse import ArgumentParser
from dind import Pipeline

dirPath = os.path.dirname(os.path.realpath(__file__))
buildPath = dirPath+'/docker/'
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
    pipeline.runContainerInteractive(image=pipeline.dockerRegistry+'/dind-py:fakos',
                                     name='fakos-test', working_dir=testDir, volumes=volumes, command='pytest')
    pipeline.buildImage(buildPath, localTag)
    print('Testing complete')

def securityScan():
    print('Starting security scans:')
    pipeline.cveScan(localTag)

def local():
    volumes = {
        dirPath: { 'bind': '/tmp', 'mode': 'rw'}
    }
    print('Initializing locally built instance:')
    pipeline.buildImage(buildPath,localTag)
    pipeline.runContainerInteractive(image=localTag,
                                     name='fakos-local', working_dir='/tmp', volumes=volumes, command='/bin/sh')

def main():
    parser = ArgumentParser(prog='ci-py')
    parser.add_argument('stage', type=str,
                        help='run pipeline stage; test, scan, local')
    args = parser.parse_args()
    ci(args.stage)

if __name__ == '__main__':
    main()