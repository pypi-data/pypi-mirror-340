# Copyright 2024 Superlinked, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from beartype.typing import Generic, Sequence
from typing_extensions import override

from superlinked.framework.common.dag.context import ExecutionContext
from superlinked.framework.common.dag.schema_field_node import SchemaFieldNode
from superlinked.framework.common.parser.parsed_schema import (
    ParsedSchema,
    ParsedSchemaField,
)
from superlinked.framework.common.schema.schema_object import SFT
from superlinked.framework.common.storage_manager.storage_manager import StorageManager
from superlinked.framework.online.dag.evaluation_result import EvaluationResult
from superlinked.framework.online.dag.exception import ValueNotProvidedException
from superlinked.framework.online.dag.online_node import OnlineNode
from superlinked.framework.online.dag.parent_validator import ParentValidationType


class OnlineSchemaFieldNode(Generic[SFT], OnlineNode[SchemaFieldNode, SFT]):
    def __init__(
        self,
        node: SchemaFieldNode,
        parents: list[OnlineNode],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__(
            node,
            parents,
            storage_manager,
            ParentValidationType.NO_PARENTS,
        )

    @override
    def evaluate_self(
        self,
        parsed_schemas: Sequence[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[SFT] | None]:
        return [self.evaluate_self_single(schema) for schema in parsed_schemas]

    def evaluate_self_single(
        self,
        parsed_schema: ParsedSchema,
    ) -> EvaluationResult[SFT] | None:
        parsed_nodes: list[ParsedSchemaField] = [
            field for field in parsed_schema.fields if field.schema_field == self.node.schema_field
        ]
        result: SFT | None
        if parsed_nodes:
            result = parsed_nodes[0].value
        else:
            result = self.load_stored_results([(parsed_schema.schema, parsed_schema.id_)])[0]
        if result is not None:
            return EvaluationResult(self._get_single_evaluation_result(result))
        if self.node.schema_field.nullable:
            return None
        field_name = ".".join(
            [
                self.node.schema_field.schema_obj._schema_name,
                self.node.schema_field.name,
            ]
        )
        raise ValueNotProvidedException(
            (
                f"The SchemaField {field_name} "
                + "doesn't have a default value and was not provided in the ParsedSchema.",
            )
        )
