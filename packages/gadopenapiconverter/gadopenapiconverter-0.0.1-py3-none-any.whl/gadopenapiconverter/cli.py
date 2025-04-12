import pathlib
import shlex
import subprocess

import jinja2
import typer
from datamodel_code_generator import InputFileType
from datamodel_code_generator import generate as generate_models
from gadutils import json
from gadutils import paths
from gadutils import strings
from gadutils import temp

from gadopenapiconverter import const
from gadopenapiconverter import enums
from gadopenapiconverter import mappers
from gadopenapiconverter import models
from gadopenapiconverter import parsers
from gadopenapiconverter.os import File
from gadopenapiconverter.os import Folder
from gadopenapiconverter.utils import sorting
from gadopenapiconverter.utils import toml

app = typer.Typer(help="gadopenapiconverter")


@app.command()
def generate(
    file: str = typer.Option(..., "-f", "--file", help="Path or link to configuration file"),
    context: str = typer.Option("{}", "-c", "--context", help="JSON context for templates"),
) -> None:
    cwd = paths.current()

    file, buffer = parsers.getconfig(file)

    config = toml.todict(File.read(file))

    if buffer:
        file.unlink(missing_ok=True)

    workdir = paths.define(config.get(const.SYNTAX_WORKDIR))

    Folder.create(workdir)

    context = json.fromjson(context)

    context["workdir"] = workdir

    specifications = config.get(const.SYNTAX_SPECIFICATION, [])

    for specification in specifications:
        content = json.fromjson(
            parsers.getcontent(workdir=cwd, content=specification.get(const.SYNTAX_SPECIFICATION_CONTENT))
        )

        if operations := specification.get(const.SYNTAX_SPECIFICATION_OPERATIONS, []):
            content = parsers.filtercontent(content=content, operations=operations)

        if model := specification.get(const.SYNTAX_SPECIFICATION_MODEL):
            module = enums.PythonModule(model)
        else:
            module = enums.PythonModule.pydantic

        schema = models.Specification(**content)

        path = workdir / pathlib.Path(specification.get(const.SYNTAX_SPECIFICATION_PATH))

        file, buffer = temp.getfile(str(content), extension=const.EXTENSION_JSON), True

        generate_models(
            file,
            output=path,
            input_file_type=InputFileType.OpenAPI,
            output_model_type=mappers.MAPPING_PYTHON_MODULE_TO_DATAMODEL.get(module),
            use_title_as_name=False,
        )

        if buffer:
            file.unlink(missing_ok=True)

        File.write(
            path=path,
            content=jinja2.Template(File.read(pathlib.Path(const.TEMPLATE_MODEL.format(module=module.name)))).render(),
            mode=const.FILE_APPEND,
        )

        File.write(
            path=path,
            content=jinja2.Template(File.read(pathlib.Path(const.TEMPLATE_CLIENT))).render(),
            mode=const.FILE_APPEND,
        )

        for url, route in schema.paths.items():
            for method in enums.HTTPMethod:
                if not (operation := getattr(route, method)):
                    continue

                function = parsers.parseoperation(operation)

                method = jinja2.Template(File.read(pathlib.Path(const.TEMPLATE_METHOD))).render(
                    {
                        "function": {
                            "async": specification.get(const.SYNTAX_SPECIFICATION_ASYNC, True),
                            "name": strings.snake(operation.operationId)
                            if operation.operationId
                            else strings.snake(operation.summary),
                            "arguments": ", ".join(f"{arg.name}: {arg.annotation}" for arg in function.arguments),
                            "annotation": enums.TypingType.array.wrapp(function.options["response"]["name"])
                            if function.options["response"]["array"]
                            else function.options["response"]["name"],
                            "serialize": jinja2.Template(
                                File.read(pathlib.Path(const.TEMPLATE_MODEL_SERIALIZE.format(module=module.name)))
                            ).render(function.options["response"]),
                        },
                        "request": {
                            "method": method,
                            "url": url,
                            "paths": [
                                arg.name for arg in function.arguments if arg.location == enums.HTTPAttribute.path
                            ],
                            "params": {
                                arg.name: arg.name
                                for arg in function.arguments
                                if arg.location == enums.HTTPAttribute.query
                            },
                            "headers": {header.name: header.annotation for header in function.headers},
                            "json": function.options.get("body"),
                            "data": function.options.get("data"),
                            "file": function.options.get("file"),
                            "files": function.options.get("files"),
                            "auth": function.options.get("auth"),
                        },
                    }
                )

                File.write(path=path, content=const.SYMBOL_NEWLINE + method, mode=const.FILE_APPEND)

        File.write(path=path, content=sorting.sortimports(File.read(path=path, tolist=True)))

    if scripts := config.get(const.SYNTAX_SCRIPTS, []):
        for script in scripts:
            if command := script.get(const.SYNTAX_SCRIPTS_COMMAND):
                subprocess.run(
                    shlex.split(jinja2.Template(command).render(context)),
                    cwd=workdir,
                    text=True,
                    check=script.get(const.SYNTAX_SCRIPTS_CHECK, False),
                )


if __name__ == "__main__":
    app()
