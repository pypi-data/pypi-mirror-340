from typing import Literal, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum


class SecurityProtocol(str, Enum):
    PLAINTEXT = "PLAINTEXT"
    SSL = "SSL"
    SASL_PLAINTEXT = "SASL_PLAINTEXT"
    SASL_SSL = "SASL_SSL"


class KafkaConfig(BaseModel):
    """Base configuration for all Kafka clients"""
    bootstrap_servers: str = Field(..., alias="bootstrap.servers",
                                   description="Comma-separated list of broker addresses")
    security_protocol: SecurityProtocol = Field(default=SecurityProtocol.SSL,
                                                alias="security.protocol")
    ssl_cafile: Optional[str] = Field(default=None, alias="ssl.ca.location")
    ssl_certfile: Optional[str] = Field(default=None, alias="ssl.certificate.location")
    ssl_keyfile: Optional[str] = Field(default=None, alias="ssl.key.location")
    ssl_check_hostname: bool = Field(default=True, alias="enable.ssl.certificate.verification")
    ssl_password: Optional[str] = Field(default=None, alias="ssl.key.password")

    def get(self) -> dict[str, Json]:
        return self.model_dump(by_alias=True)

    class Config:
        validate_by_name = True
        use_enum_values = True
        extra = "forbid"


class ConsumerConfig(KafkaConfig):
    """Configuration for basic Kafka consumer"""
    group_id: str = Field(..., alias="group.id")
    enable_auto_commit: bool = Field(default=False, alias="enable.auto.commit")
    auto_offset_reset: Literal["earliest", "latest"] = Field(default="latest",
                                                             alias="auto.offset.reset")
    session_timeout_ms: int = Field(default=10000, alias="session.timeout.ms")
    max_poll_interval_ms: int = Field(default=300000, alias="max.poll.interval.ms")
    fetch_max_bytes: int = Field(default=52428800, alias="fetch.max.bytes")


class ProducerConfig(KafkaConfig):
    """Configuration for basic Kafka producer"""
    acks: Literal["all", "0", "1"] = Field(default="all")
    retries: int = Field(default=0)
    linger_ms: int = Field(default=0, alias="linger.ms")
    compression_type: Literal["none", "gzip", "snappy", "lz4", "zstd"] = Field(
        default="none", alias="compression.type")
    batch_size: int = Field(default=16384, alias="batch.size")
    max_in_flight: int = Field(default=1000000, alias="max.in.flight.requests.per.connection")


class AvroConsumerConfig(ConsumerConfig):
    """Configuration for Avro consumer with Schema Registry"""
    schema_registry_url: str = Field(..., alias="schema.registry.url")
    schema_registry_ssl_cafile: Optional[str] = Field(default=None,
                                                      alias="schema.registry.ssl.ca.location")
    schema_registry_basic_auth_user_info: Optional[str] = Field(default=None,
                                                                alias="schema.registry.basic.auth.user.info")
    specific_avro_reader: bool = Field(default=False, alias="specific.avro.reader")


class AvroProducerConfig(ProducerConfig):
    """Configuration for Avro producer with Schema Registry"""
    schema_registry_url: str = Field(..., alias="schema.registry.url")
    schema_registry_ssl_cafile: Optional[str] = Field(default=None,
                                                      alias="schema.registry.ssl.ca.location")
    schema_registry_basic_auth_user_info: Optional[str] = Field(default=None,
                                                                alias="schema.registry.basic.auth.user.info")
    max_schemas_per_subject: int = Field(default=1000, alias="max.schemas.per.subject")


class JsonConsumerConfig(ConsumerConfig):
    """Configuration for JSON consumer"""
    json_deserializer: Optional[str] = None  # Custom deserializer function
    encoding: str = Field(default="utf-8")


class JsonProducerConfig(ProducerConfig):
    """Configuration for JSON producer"""
    json_serializer: Optional[str] = None  # Custom serializer function
    encoding: str = Field(default="utf-8")

    @classmethod
    @validator("compression_type")
    def validate_compression(cls, v):
        if v not in ["none", "gzip", "snappy", "lz4", "zstd"]:
            raise ValueError("Unsupported compression type")
        return v