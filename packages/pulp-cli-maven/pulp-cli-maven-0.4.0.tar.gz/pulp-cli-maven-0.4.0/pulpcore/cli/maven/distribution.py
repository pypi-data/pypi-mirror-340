import click
from pulp_glue.common.i18n import get_translation
from pulp_glue.maven.context import (
    PulpMavenDistributionContext,
    PulpMavenRemoteContext,
    PulpMavenRepositoryContext,
)
from pulpcore.cli.common.generic import (
    PulpCLIContext,
    common_distribution_create_options,
    create_command,
    destroy_command,
    distribution_filter_options,
    distribution_lookup_option,
    href_option,
    label_command,
    list_command,
    name_option,
    pass_pulp_context,
    pulp_group,
    pulp_labels_option,
    resource_option,
    show_command,
    update_command,
)

translation = get_translation(__name__)
_ = translation.gettext


repository_option = resource_option(
    "--repository",
    default_plugin="maven",
    default_type="maven",
    context_table={"maven:maven": PulpMavenRepositoryContext},
    href_pattern=PulpMavenRepositoryContext.HREF_PATTERN,
    help=_(
        "Repository to be used for auto-distributing."
        " Specified as '[[<plugin>:]<type>:]<name>' or as href."
    ),
)


remote_option = resource_option(
    "--remote",
    default_plugin="maven",
    default_type="maven",
    context_table={"maven:maven": PulpMavenRemoteContext},
    href_pattern=PulpMavenRemoteContext.HREF_PATTERN,
    help=_(
        "Remote used for downloading content that is not yet in Pulp."
        " Specified as '[[<plugin>:]<resource_type>:]<name>' or by href."
    ),
)


@pulp_group()
@click.option(
    "-t",
    "--type",
    "distribution_type",
    type=click.Choice(["maven"], case_sensitive=False),
    default="maven",
)
@pass_pulp_context
@click.pass_context
def distribution(ctx: click.Context, pulp_ctx: PulpCLIContext, distribution_type: str) -> None:
    if distribution_type == "maven":
        ctx.obj = PulpMavenDistributionContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option, name_option, distribution_lookup_option]
nested_lookup_options = [distribution_lookup_option]
update_options = [
    remote_option,
    repository_option,
    pulp_labels_option,
]
create_options = common_distribution_create_options + update_options

distribution.add_command(list_command(decorators=distribution_filter_options))
distribution.add_command(show_command(decorators=lookup_options))
distribution.add_command(create_command(decorators=create_options))
distribution.add_command(
    update_command(decorators=lookup_options + update_options + [click.option("--base-path")])
)
distribution.add_command(destroy_command(decorators=lookup_options))
distribution.add_command(label_command(decorators=nested_lookup_options))
