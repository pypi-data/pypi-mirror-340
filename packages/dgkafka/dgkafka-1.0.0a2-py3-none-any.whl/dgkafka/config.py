from typing import Literal, Optional
from pydantic import BaseModel, Field


class KafkaConfig(BaseModel):
    bootstrap_servers: str = Field(..., alias="bootstrap.servers",
                                 description="Comma-separated list of broker addresses")
    security_protocol: Optional[str] = Field(default="SSL", alias="security.protocol",
                                           description="Protocol used to communicate with brokers")
    ssl_ca_location: Optional[str] = Field(default=None, alias="ssl.ca.location",
                                         description="Path to CA certificate file")
    ssl_certificate_location: Optional[str] = Field(default=None, alias="ssl.certificate.location",
                                                  description="Path to client certificate file")
    ssl_key_location: Optional[str] = Field(default=None, alias="ssl.key.location",
                                          description="Path to client private key file")
    ssl_certificate_verification: Optional[bool] = Field(default=True,
                                                       alias="enable.ssl.certificate.verification",
                                                       description="Enable SSL certificate verification")
    ssl_endpoint_identification_algorithm: Optional[str] = Field(default="https",
                                                               alias="ssl.endpoint.identification.algorithm",
                                                               description="Endpoint identification algorithm")

    class Config:
        allow_population_by_field_name = True
        extra = "forbid"


class ConsumerConfig(KafkaConfig):
    group_id: str = Field(..., alias="group.id",
                         description="Consumer group identifier")
    enable_auto_commit: bool = Field(default=False, alias="enable.auto.commit",
                                   description="Automatically commit offsets periodically")
    auto_offset_reset: Literal["earliest", "latest"] = Field(default="earliest",
                                                           alias="auto.offset.reset",
                                                           description="Reset policy when no offset is available")
    max_poll_records: Optional[int] = Field(default=500, alias="max.poll.records",
                                          description="Maximum records per poll")
    session_timeout_ms: int = Field(default=10000, alias="session.timeout.ms",
                                  description="Timeout for consumer session")


class ProducerConfig(KafkaConfig):
    acks: Literal["all", "-1", "0", "1"] = Field(default="all",
                                                description="Number of acknowledgments")
    retries: int = Field(default=3, description="Number of retries on failure")
    linger_ms: int = Field(default=0, alias="linger.ms",
                         description="Delay in milliseconds to wait for messages in the buffer")
    compression_type: Optional[str] = Field(default=None, alias="compression.type",
                                          description="Compression codec to use")
    batch_size: int = Field(default=16384, alias="batch.size",
                          description="Batch size in bytes")


class AvroConfigMixin(BaseModel):
    schema_registry_url: str = Field(..., alias="schema.registry.url",
                                   description="URL of Schema Registry")
    schema_registry_ssl_ca_location: Optional[str] = Field(default=None,
                                                         alias="schema.registry.ssl.ca.location",
                                                         description="Schema Registry CA certificate path")
    auto_register_schemas: bool = Field(default=True, alias="auto.register.schemas",
                                      description="Automatically register schemas")


class AvroConsumerConfig(ConsumerConfig, AvroConfigMixin):
    use_latest_version: bool = Field(default=True, alias="use.latest.version",
                                   description="Use latest schema version")
    skip_known_types: bool = Field(default=False, alias="skip.known.types",
                                 description="Skip known types during deserialization")


class AvroProducerConfig(ProducerConfig, AvroConfigMixin):
    value_subject_name_strategy: Optional[str] = Field(default=None,
                                                     alias="value.subject.name.strategy",
                                                     description="Strategy for subject name generation")
    key_subject_name_strategy: Optional[str] = Field(default=None,
                                                   alias="key.subject.name.strategy",
                                                   description="Strategy for key subject name generation")


class JsonConsumerConfig(ConsumerConfig):
    json_deserializer: Optional[str] = Field(default=None,
                                           description="Custom JSON deserializer function")
    encoding: str = Field(default="utf-8", description="Message encoding")


class JsonProducerConfig(ProducerConfig):
    json_serializer: Optional[str] = Field(default=None,
                                         description="Custom JSON serializer function")
    encoding: str = Field(default="utf-8", description="Message encoding")