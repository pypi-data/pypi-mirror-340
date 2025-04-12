#
# PartCAD, 2025
# OpenVMP, 2023-2024
#
# Author: Aleksandr Ilin (ailin@partcad.org)
# Created: Fri Nov 22 2024
#
# Licensed under Apache License, Version 2.0.
#

import rich_click as click
import asyncio

import partcad as pc
from partcad.test.all import tests as all_tests
from partcad.user_config import user_config


async def cli_test_async(ctx, packages, filter_prefix, sketch, interface, assembly, scene, object):
    """
    TODO-118: @alexanderilyin: Add scene support
    """
    tasks = []

    tests_to_run = all_tests(user_config.threads_max)
    if filter_prefix:
        tests_to_run = list(filter(lambda t: t.name.startswith(filter_prefix), tests_to_run))
        pc.logging.debug(f"Running tests with prefix {filter_prefix}")

    for package in packages:
        if object:
            package, object = pc.utils.resolve_resource_path(ctx.get_current_project_path(), object)

        prj = ctx.get_project(package)
        if not object:
            # Test all parts and assemblies in this project
            tasks.append(prj.test_log_wrapper_async(ctx, tests=tests_to_run))
        elif interface:
            # Test the requested interface
            shape = prj.get_interface(object)
            if shape is None:
                pc.logging.error(f"{object} is not found")
            elif not shape.finalized:
                pc.logging.warning(f"{object} is not finalized")
            else:
                tasks.append(shape.test_async())
        else:
            # Test the requested part or assembly
            if sketch:
                shape = prj.get_sketch(object)
            elif assembly:
                shape = prj.get_assembly(object)
            else:
                shape = prj.get_part(object)

            if shape is None:
                pc.logging.error(f"{object} is not found")
            elif not shape.finalized:
                pc.logging.warning(f"{object} is not finalized")
            else:
                tasks.extend([t.test_log_wrapper(tests_to_run, ctx, shape) for t in tests_to_run])

    await asyncio.gather(*tasks)


@click.command(help="Run tests on a part, assembly, or scene")
@click.option(
    "--package",
    "-P",
    type=str,
    default="",
    show_envvar=True,
    help="Package to retrieve the object from",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    show_envvar=True,
    help="Recursively test all imported packages",
)
@click.option(
    "--filter",
    "-f",
    help="Only run tests that start with the given prefix",
    type=str,
    show_envvar=True,
    default=None,
)
@click.option(
    "--sketch",
    "-s",
    is_flag=True,
    show_envvar=True,
    help="The object is a sketch",
)
@click.option(
    "--interface",
    "-i",
    is_flag=True,
    show_envvar=True,
    help="The object is an interface",
)
@click.option(
    "--assembly",
    "-a",
    is_flag=True,
    show_envvar=True,
    help="The object is an assembly",
)
@click.option(
    "--scene",
    "-S",
    is_flag=True,
    show_envvar=True,
    help="The object is a scene",
)
@click.argument("object", type=str, required=False)  # help="Part (default), assembly or scene to test"
@click.pass_obj
def cli(cli_ctx, package, recursive, filter, sketch, interface, assembly, scene, object):
    with pc.telemetry.set_context(cli_ctx.otel_context):
        ctx: pc.Context = cli_ctx.get_partcad_context()

        package = ctx.resolve_package_path(package)
        package_obj = ctx.get_project(package)
        if not package_obj:
            pc.logging.error(f"Package {package} is not found")
            return
        package = package_obj.name  # '//' may end up having a different name

        with pc.logging.Process("Test", package):
            if recursive:
                all_packages = ctx.get_all_packages(parent_name=package)
                if ctx.stats_git_ops:
                    pc.logging.info(f"Git operations: {ctx.stats_git_ops}")
                packages = [p["name"] for p in all_packages]
            else:
                packages = [package]

            asyncio.run(
                cli_test_async(
                    ctx,
                    packages,
                    filter_prefix=filter,
                    sketch=sketch,
                    interface=interface,
                    assembly=assembly,
                    scene=scene,
                    object=object,
                )
            )
