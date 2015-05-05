
#
# This file is the default set of rules to compile a Pebble project.
#
# Feel free to customize this to your needs.
#

import itertools
import os
import sys
import subprocess
import json

top = '.'
out = 'build'
d_compiler = '/home/w0rp/bin/arm-none-eabi-gdc/bin/arm-none-eabi-gdc'


def options(ctx):
    ctx.load('pebble_sdk')


def configure(ctx):
    ctx.load('pebble_sdk')


def load_d_import_paths():
    dub = subprocess.Popen(['dub', 'describe'], stdout=subprocess.PIPE)

    dub_json = json.loads(dub.stdout.read())

    # Read import paths from the packages.
    import_path_list = tuple(itertools.chain.from_iterable(
        (
            os.path.join(package['path'], tail)
            for tail in
            package['importPaths']
        )
        for package in
        dub_json['packages']
    ))

    return import_path_list


def compile_d_sources(ctx):
    path_list = tuple(nod.relpath() for nod in ctx.path.ant_glob('src/**/*.d'))

    # Load the import paths from dub.json.
    import_path_list = load_d_import_paths()

    # Turn the paths import import flags.
    import_path_args = tuple(
        itertools.chain.from_iterable(
            itertools.izip(itertools.repeat('-I'), import_path_list)
        )
    )

    for source_path in path_list:
        # Get the path to the object file.
        object_path = ''.join(('obj', source_path[3:-2], '.o'))

        if os.path.getmtime(object_path) >= os.path.getmtime(source_path):
            # This object file is up to date, so we can skip it.
            continue

        # Create the directory if needed.
        object_dir = os.path.dirname(object_path)

        if not os.path.exists(object_dir):
            os.makedirs(object_dir)

        # Compile the source file.
        subprocess.check_call(
            (d_compiler, )
            + import_path_args
            + (
                '-mthumb',
                '-mcpu=cortex-m4',
                '-fno-emit-moduleinfo',
                '-fdata-sections',
                '-fno-exceptions',
                '-Os',
                '-c',
                source_path,
                '-o',
                object_path,
            )
        )


def build(ctx):
    ctx.load('pebble_sdk')

    build_worker = os.path.exists('worker_src')

    compile_d_sources(ctx)

    binaries = []

    for p in ctx.env.TARGET_PLATFORMS:
        ctx.set_env(ctx.all_envs[p])
        ctx.set_group(ctx.env.PLATFORM_NAME)
        app_elf = os.path.join(ctx.env.BUILD_DIR, 'pebble-app.elf')

        ctx.pbl_program(
            source=ctx.path.ant_glob('obj/**/*.o'),
            target=app_elf,
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
