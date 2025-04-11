from typing import TypedDict


class ScanArgs(TypedDict):
    source: str
    format: str
    output: str
    docker_user: str | None
    docker_password: str | None
    aws_external_id: str | None
    aws_role: str | None
    config: bool
    debug: bool


class DockerCredentials(TypedDict):
    username: str
    password: str


class AwsCredentials(TypedDict):
    external_id: str
    role: str


class OutputConfig(TypedDict):
    name: str
    format: str


class LoadedConfig(TypedDict):
    source: str
    source_type: str
    execution_id: str
    exclude: tuple[str]
    docker_credentials: DockerCredentials | None
    aws_credentials: AwsCredentials | None
    output: OutputConfig
    debug: bool
