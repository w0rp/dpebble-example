
#
# This file is the default set of rules to compile a Pebble project.
#
# Feel free to customize this to your needs.
#

import os
import sys
import subprocess

top = '.'
out = 'build'


def options(ctx):
    ctx.load('pebble_sdk')


def configure(ctx):
    ctx.load('pebble_sdk')


def build(ctx):
    ctx.load('pebble_sdk')

    build_worker = os.path.exists('worker_src')

    binaries = []

    for p in ctx.env.TARGET_PLATFORMS:
        ctx.set_env(ctx.all_envs[p])
        ctx.set_group(ctx.env.PLATFORM_NAME)
        app_elf = os.path.join(ctx.env.BUILD_DIR, 'pebble-app.elf')
        ctx.pbl_program(
            #source=ctx.path.ant_glob('src/**/*.c'),
            source=[],
            target=app_elf,
            stlib=['pebbleapp'],
            stlibpath=[os.path.abspath('lib')],
            ldscript='linker.ld',
        )

        if build_worker:
            worker_elf = os.path.join(ctx.env.BUILD_DIR, 'pebble-worker.elf')

            binaries.append({
                'platform': p,
                'app_elf': app_elf,
                'worker_elf': worker_elf
            })

            ctx.pbl_worker(
                source=ctx.path.ant_glob('worker_src/**/*.c'),
                target=worker_elf
            )
        else:
            binaries.append({
                'platform': p,
                'app_elf': app_elf
            })

    ctx.set_group('bundle')
    ctx.pbl_bundle(binaries=binaries, js=ctx.path.ant_glob('src/js/**/*.js'))
