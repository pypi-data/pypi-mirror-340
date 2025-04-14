from itertools import product
from os.path import join, dirname
from logging import getLogger
import jinja2
from yaml import dump, safe_load
from gitops_configserver.config import Config
from gitops_configserver.config_loader import TenantsConfigLoader
from gitops_configserver.utils import create_dir, read_file, write_to_file
from gitops_configserver.hieradata_resolver import HieradataResolver


logger = getLogger(__name__)


class TemplateRendering:
    def __init__(self, config: Config):
        self.config = config
        self.tenants_config_loader = TenantsConfigLoader(config)
        self.jinja_env = jinja2.Environment(
            block_start_string=r"\BLOCK{",
            block_end_string="}",
            variable_start_string="{",
            variable_end_string="}",
            comment_start_string=r"\#{",
            comment_end_string="}",
            line_statement_prefix="%%",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
        )
        self.hieradata_resolver = HieradataResolver(self.config)
        self.jinja_env.filters.update(
            {
                "to_yaml": lambda data: dump(data).strip(),
                "variants_matrix_resolver": lambda data: VariantsMatrixResolver.resolve(
                    data, self.tenant_variables
                ),
            },
        )

    def _render_template(self, template: str, variables: dict) -> str:
        new_template = self.jinja_env.from_string(template)
        return new_template.render(**variables)

    def render(self, tenant_name, template_name, facts):
        self.tenant_variables = self.hieradata_resolver.render(
            tenant_name, facts
        )
        template_content = read_file(
            join(
                self.config.CONFIG_DIR, tenant_name, "templates", template_name
            )
        )
        rendered_content = self._render_template(
            template_content, self.tenant_variables
        )
        return rendered_content


class TemplatesRendering:

    def __init__(self, config: Config):
        self.config = config
        self.tenants_config_loader = TenantsConfigLoader(config)
        self.jinja_env = jinja2.Environment(
            block_start_string=r"\BLOCK{",
            block_end_string="}",
            variable_start_string="{",
            variable_end_string="}",
            comment_start_string=r"\#{",
            comment_end_string="}",
            line_statement_prefix="%%",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
        )
        self.hieradata_resolver = HieradataResolver(self.config)
        self.jinja_env.filters.update(
            {"to_yaml": lambda data: dump(data).strip()}
        )

    def render(self, tenant_name) -> dict:
        tenant_variables = self.hieradata_resolver.render(
            tenant_name, self.config.FACTS
        )
        tenant_config = self.tenants_config_loader.tenant(tenant_name)

        templates_dict = {
            "repositories": tenant_config.get("repositories", {}),
            "files": [],
        }

        for template_config in tenant_config.get("configs", {}):
            template_variables_mapping = template_config.get("variables", [])
            tpl_variables = VariablesResolver.resolve_for_template(
                template_variables_mapping, tenant_variables
            )
            logger.info(f"tpl_variables: {tpl_variables}")
            variants = self._get_variants(template_config, tenant_variables)

            for variant in variants:
                template_content = read_file(
                    join(
                        self.config.CONFIG_DIR,
                        tenant_name,
                        "templates",
                        template_config.get("template_file"),
                    )
                )
                logger.info(f"template_content: {template_content}")

                rendered_content = self._render_template(
                    template_content, tpl_variables
                )
                logger.info(f"rendered_content: {rendered_content}")

                destination_filename = TemplateResolver.resolve(
                    template_config.get("destination_filename", ""),
                    {
                        **tpl_variables,
                        "environment": template_config.get("environment"),
                        "matrix": variant,
                    },
                )
                destination_filepath = join(
                    self.config.TARGET_DIR, tenant_name, destination_filename
                )
                logger.info(f"destination_filepath: {destination_filepath}")
                create_dir(dirname(destination_filepath))
                write_to_file(destination_filepath, rendered_content)

                templates_dict["files"] += [
                    {
                        "tmp_path": destination_filepath,
                        "destination_filename": destination_filename,
                        "repo": template_config.get(
                            "destination_repo", "local"
                        ),
                    }
                ]

        return templates_dict

    def _get_variants(
        self, template_config: dict, tenant_variables: dict
    ) -> list:
        matrix = template_config.get("matrix", {})
        matrix_include = template_config.get("matrix_include", [])
        resolved_variants = MatrixResolver.resolve(matrix, tenant_variables)
        variants = resolved_variants + matrix_include
        return variants

    def _render_template(self, template: str, variables: dict) -> str:
        new_template = self.jinja_env.from_string(template)
        return new_template.render(**variables)


class TemplateResolver:
    @staticmethod
    def resolve(template_content, variables) -> str:
        env = jinja2.Environment()
        template = env.from_string(template_content)
        output = template.render(**variables)
        return output


class VariantsMatrixResolver:
    @staticmethod
    def resolve(matrix, tenant_variables) -> list:
        env = jinja2.Environment()
        for key, value in matrix.items():
            if isinstance(value, str):
                template = env.from_string(value)
                output = template.render(**tenant_variables)
                matrix[key] = safe_load(output)
        matrix_filtered = {
            k: v for k, v in matrix.items() if k not in ["include"]
        }
        keys, values = zip(*matrix_filtered.items())
        permutations_dicts = [dict(zip(keys, v)) for v in product(*values)]
        permutations_dicts += matrix.get("include", {})
        return permutations_dicts or []


class MatrixResolver:
    @staticmethod
    def resolve(matrix, tenant_variables) -> list:
        env = jinja2.Environment()
        for key, value in matrix.items():
            if isinstance(value, str):
                template = env.from_string(value)
                output = template.render(**tenant_variables)
                matrix[key] = safe_load(output)

        if not matrix:
            return [{"_variant": "default"}]
        keys, values = zip(*matrix.items())
        permutations_dicts = [dict(zip(keys, v)) for v in product(*values)]
        return permutations_dicts


class VariablesResolver:
    @staticmethod
    def resolve_for_template(
        template_variables_mapping: list, tenant_variables: dict
    ) -> dict:
        resolved_dict = {}
        for template_variable_item in template_variables_mapping:
            key = template_variable_item.get("tpl_variable")
            value = tenant_variables.get(
                template_variable_item.get("tenant_variable")
            )
            resolved_dict[key] = value
        return resolved_dict
