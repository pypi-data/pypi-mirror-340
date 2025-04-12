import copy
from typing import Any

import sqlglot
from sqlglot import exp
from sqlglot.expressions import (
    ColumnConstraint,
    ColumnDef,
    DataType,
    DefaultColumnConstraint,
    Expression,
    Identifier,
    Literal,
)

from airfold_common.clickhouse import to_db_schema
from airfold_common.error import AirfoldError


class AirfoldCastError(AirfoldError):
    pass


class AirfoldParseError(AirfoldError, sqlglot.ParseError):
    pass


def set_nullable(data_type: exp.DataType, nullable: bool = True) -> exp.DataType:
    def _set_nullable(data_type: exp.DataType, nullable: bool) -> exp.DataType:
        if not data_type.args.get("nullable", False) and not data_type.args.get("nested", False):
            data_type.args["nullable"] = nullable
        return data_type

    # in CH nested types (Array, Map, Tuple) cannot be Nullable...
    if data_type.this == DataType.Type.LOWCARDINALITY:
        assert data_type.expressions
        data_type.expressions[0] = _set_nullable(data_type.expressions[0], nullable)
    else:
        data_type = _set_nullable(data_type, nullable)
    return data_type


def parse_one(sql: str, dialect: str = "clickhouse") -> Expression:
    try:
        return sqlglot.parse_one(sql, read=dialect)
    except sqlglot.ParseError as e:
        raise AirfoldParseError(str(e)) from e


CH_TO_JSON_MAP: dict[str, Any] = {
    "UInt8": {"type": "integer", "minimum": 0, "maximum": 255},
    "UInt16": {"type": "integer", "minimum": 0},
    "UInt32": {"type": "integer", "minimum": 0},
    "UInt64": {"type": "integer", "minimum": 0},
    "Int8": {"type": "integer"},
    "Int16": {"type": "integer"},
    "Int32": {"type": "integer"},
    "Int64": {"type": "integer"},
    "Float32": {"type": "number"},
    "Float64": {"type": "number"},
    "DOUBLE": {"type": "number"},
    # "Decimal": {"type": "number"}, # Precision/Scale handled separately
    "Boolean": {"type": "boolean"},
    "BOOLEAN": {"type": "boolean"},
    "Bool": {"type": "boolean"},
    "String": {"type": "string"},
    # "FixedString": {"type": "string"},  # Length handled separately
    "Date": {"type": "string", "format": "date"},
    "DATE": {"type": "string", "format": "date"},
    "Date32": {"type": "string", "format": "date"},
    "DateTime": {"type": "string", "format": "date-time"},
    "DATETIME": {"type": "string", "format": "date-time"},
    "DateTime64": {"type": "string", "format": "date-time"},
    "DateTime64(3)": {"type": "string", "format": "date-time"},
    "DateTime64(6)": {"type": "string", "format": "date-time"},
    "DateTime64(9)": {"type": "string", "format": "date-time"},
    "JSON": {"type": "object"},
    "UUID": {"type": "string", "format": "uuid"},
    # "Enum": {"type": "string"},  # Enum values handled separately
    "LowCardinality": {"type": "string"},
    # "Array": {"type": "array"},  # Element type handled separately
    # "Map": {"type": "object"},  # Key/Value types handled separately
    # "Nested": {"type": "object"},  # Nested structure handled separately
    # "Tuple": {"type": "array"},  # Tuple items handled separately
    # "Nullable": {"type": "null"},  # Nullable type handled separately
    "IPv4": {"type": "string", "format": "ipv4"},
    "IPv6": {"type": "string", "format": "ipv6"},
}

CH_TO_JSON_MAP_GPT: dict[str, Any] = {
    "UInt8": {"type": "number"},
    "UInt16": {"type": "number"},
    "UInt32": {"type": "number"},
    "UInt64": {"type": "number"},
    "Int8": {"type": "number"},
    "Int16": {"type": "number"},
    "Int32": {"type": "number"},
    "Int64": {"type": "number"},
    "Float32": {"type": "number"},
    "Float64": {"type": "number"},
    "DOUBLE": {"type": "number"},
    # "Decimal": {"type": "number"}, # Precision/Scale handled separately
    "Boolean": {"type": "boolean"},
    "BOOLEAN": {"type": "boolean"},
    "Bool": {"type": "boolean"},
    "String": {"type": "string"},
    # "FixedString": {"type": "string"},  # Length handled separately
    "Date": {"type": "string"},
    "DATE": {"type": "string"},
    "Date32": {"type": "string"},
    "DateTime": {"type": "string"},
    "DATETIME": {"type": "string"},
    "DateTime64": {"type": "string"},
    "DateTime64(3)": {"type": "string"},
    "DateTime64(6)": {"type": "string"},
    "DateTime64(9)": {"type": "string"},
    "JSON": {"type": "object"},
    "UUID": {"type": "string"},
    # "Enum": {"type": "string"},  # Enum values handled separately
    "LowCardinality": {"type": "string"},
    # "Array": {"type": "array"},  # Element type handled separately
    # "Map": {"type": "object"},  # Key/Value types handled separately
    # "Nested": {"type": "object"},  # Nested structure handled separately
    # "Tuple": {"type": "array"},  # Tuple items handled separately
    # "Nullable": {"type": "null"},  # Nullable type handled separately
    "IPv4": {"type": "string"},
    "IPv6": {"type": "string"},
}


def convert_type(
    data_type: Expression,
    constraints: list[ColumnConstraint],
    dialect: str = "clickhouse",
    openapi: bool = False,
    gpt: bool = False,
) -> dict[str, Any]:
    default: Any | None = None
    if (
        constraints
        and isinstance(constraints[0].kind, DefaultColumnConstraint)
        and isinstance(constraints[0].kind.this, Literal)
    ):
        default = constraints[0].kind.this.this
    dt = (CH_TO_JSON_MAP_GPT if gpt else CH_TO_JSON_MAP).get(data_type.sql(dialect))
    res: dict[str, Any]
    if dt:
        res = copy.deepcopy(dt)
    elif data_type.this == DataType.Type.LOWCARDINALITY:
        value_type = data_type.expressions[0]
        res = convert_type(value_type, constraints, dialect, openapi=openapi, gpt=gpt)
    elif data_type.this == DataType.Type.FIXEDSTRING:
        length = int(data_type.expressions[0].this.sql(dialect))
        if gpt:
            # see https://platform.openai.com/docs/guides/structured-outputs/some-type-specific-keywords-are-not-yet-supported
            res = {"type": "string"}
        else:
            res = {"type": "string", "minLength": length, "maxLength": length}
    elif data_type.this == DataType.Type.DECIMAL:
        # TODO: theres "exclusiveMaximum" in the spec, but it's limited to Int32 (decimals can be Int64)
        # p = 10
        # if len(data_type.expressions) > 0:
        #     p = int(data_type.expressions[0].sql(dialect))
        s = 0
        if len(data_type.expressions) > 1:
            s = int(data_type.expressions[1].sql(dialect))
        if gpt:
            # see https://platform.openai.com/docs/guides/structured-outputs/some-type-specific-keywords-are-not-yet-supported
            res = {"type": "number"}
        else:
            multiple = 10 ** (-s)
            res = {"type": "number", "multipleOf": multiple}
    elif data_type.this in [DataType.Type.ENUM, DataType.Type.ENUM8, DataType.Type.ENUM16]:
        enum = []
        for item in data_type.expressions:
            if isinstance(item, Literal):
                name = item.this
            else:
                name = item.this.this
            enum.append(name)
        res = {"type": "string", "enum": enum}
    elif data_type.this == DataType.Type.ARRAY:
        array_type = data_type.expressions[0]
        res = {"type": "array", "items": convert_type(array_type, [], dialect, openapi=openapi, gpt=gpt)}
    elif data_type.this == DataType.Type.MAP:
        key_type = data_type.expressions[0]
        if key_type.this != DataType.Type.TEXT:
            if openapi:
                res = {"type": "string"}
            else:
                raise AirfoldCastError(f"Unsupported map with non-string keys: {data_type.sql(dialect)}")
        else:
            if gpt:
                raise AirfoldCastError("Map is unsupported for AI")
            value_type = data_type.expressions[1]
            res = {
                "type": "object",
                "additionalProperties": convert_type(value_type, [], dialect, openapi=openapi, gpt=gpt),
            }
    elif data_type.this == DataType.Type.STRUCT:
        items = []
        for item in data_type.expressions:
            if isinstance(item, Identifier):
                str_type = item.this
                expr = parse_one(f"CREATE TABLE t (a {str_type})", dialect=dialect)
                col = expr.this.expressions[0]
                items.append(convert_type(col.args["kind"], [], dialect, openapi=openapi, gpt=gpt))
            elif isinstance(item, DataType):
                items.append(convert_type(item, [], dialect, openapi=openapi, gpt=gpt))
        # TODO: maybe {"items": false} is needed
        res = {"type": "array", "prefixItems": items}
    elif data_type.args.get("nullable"):
        data_type.args["nullable"] = False
        res = convert_type(data_type, [], dialect, openapi=openapi, gpt=gpt)
        if openapi:
            res["nullable"] = True
        elif gpt:
            # gpt should never have an "escape hatch" to `null`
            pass
        else:
            res = {"oneOf": [{"type": "null"}, res]}
    else:
        if openapi:
            res = {"type": "string"}
        else:
            raise AirfoldCastError(f"Unsupported data type: {data_type.sql(dialect)}")
    if default:
        res["default"] = default
    return res


def convert_schema(
    schema: str | dict[str, str], dialect: str = "clickhouse", openapi: bool = False, gpt: bool = False
) -> dict[str, Any]:
    res: dict[str, Any] = {"type": "object", "properties": {}}
    str_schema = schema if isinstance(schema, str) else ", ".join([" ".join([f"`{n}`", t]) for n, t in schema.items()])
    create_table = f"CREATE TABLE t ({str_schema})"
    sql_exp = parse_one(create_table, dialect=dialect)
    required = []
    for col in sql_exp.this.expressions:
        if isinstance(col, ColumnDef):
            name = str(col.this.this)
            required.append(name)
            data_type = col.args["kind"]
            constraints = col.args["constraints"]
            if data_type.this == DataType.Type.NESTED:
                nested_types = ", ".join([t.sql(dialect) for t in data_type.expressions])
                res["properties"][name] = convert_schema(nested_types, dialect, openapi=openapi, gpt=gpt)
            else:
                res["properties"][name] = convert_type(data_type, constraints, dialect, openapi=openapi, gpt=gpt)
        else:
            raise AirfoldCastError(f"Unsupported data type: {col.sql(dialect)}")
    res["required"] = required
    res["additionalProperties"] = False
    return res


def filter_schema(schema: dict[str, str], skip_materialized: bool, skip_alias: bool) -> dict[str, str]:
    if not skip_materialized and not skip_alias:
        return schema

    parsed = parse_one(f"CREATE TABLE t ({to_db_schema(schema)})")
    col_defs = list(parsed.find_all(ColumnDef))
    filtered_schema = {}
    for i, cd in enumerate(col_defs):
        computed_constraints = cd.find_all(exp.ComputedColumnConstraint)
        props = {}
        for e in computed_constraints:
            props["materialized"] = e.args.get("persisted", False)
            props["alias"] = not props["materialized"]

        if skip_materialized and props.get("materialized"):
            continue
        if skip_alias and props.get("alias"):
            continue
        filtered_schema[cd.name] = schema[cd.name]
    return filtered_schema


def schema_diff(type1: str, type2: str, dialect: str = "clickhouse") -> str:
    create_table = f"CREATE TABLE t (a {type1}, b {type2})"
    sql_exp = parse_one(create_table, dialect=dialect)
    cols = []
    for col in sql_exp.this.expressions:
        if isinstance(col, ColumnDef):
            assert col.kind  # type: ignore
            cols.append(col.kind)  # type: ignore
    # null handling:
    # Nullable -> Not-Nullable : fail
    # Nullable -> Nullable: ok
    # Not-Nullable -> Nullable: ok
    if not cols[0].args.get("nullable") or cols[1].args.get("nullable"):
        cols[0].args["nullable"] = False
        cols[1].args["nullable"] = False
    if cols[0] == cols[1]:
        return ""
    if cols[0].this in [DataType.Type.LOWCARDINALITY]:
        return schema_diff(cols[0].expressions[0].sql(dialect), type2)
    if cols[1].this in [DataType.Type.LOWCARDINALITY]:
        return schema_diff(type1, cols[1].expressions[0].sql(dialect))
    if cols[0].this in DataType.NESTED_TYPES and cols[0].this == cols[1].this:  # type: ignore
        diff = schema_diff(cols[0].expressions[0].sql(dialect), cols[1].expressions[0].sql(dialect))
        if diff:
            return f"{cols[0].this}({diff})"
        else:
            return ""
    if (cols[1].this in DataType.SIGNED_INTEGER_TYPES or cols[1].this in DataType.UNSIGNED_INTEGER_TYPES) and (  # type: ignore
        (cols[0].this in [DataType.Type.UTINYINT] and cols[1].this not in [DataType.Type.TINYINT])
        or (cols[0].this in [DataType.Type.TINYINT] and cols[1].this not in [DataType.Type.UTINYINT])
        or (
            cols[0].this in [DataType.Type.SMALLINT]
            and cols[1].this not in [DataType.Type.UTINYINT, DataType.Type.TINYINT, DataType.Type.USMALLINT]
        )
        or (
            cols[0].this in [DataType.Type.USMALLINT]
            and cols[1].this not in [DataType.Type.UTINYINT, DataType.Type.TINYINT, DataType.Type.SMALLINT]
        )
        or (
            cols[0].this in [DataType.Type.INT, DataType.Type.MEDIUMINT]
            and cols[1].this
            not in [
                DataType.Type.UTINYINT,
                DataType.Type.TINYINT,
                DataType.Type.USMALLINT,
                DataType.Type.SMALLINT,
                DataType.Type.UINT,
                DataType.Type.UMEDIUMINT,
            ]
        )
        or (
            cols[0].this in [DataType.Type.UINT, DataType.Type.UMEDIUMINT]
            and cols[1].this
            not in [
                DataType.Type.UTINYINT,
                DataType.Type.TINYINT,
                DataType.Type.USMALLINT,
                DataType.Type.SMALLINT,
                DataType.Type.INT,
                DataType.Type.MEDIUMINT,
            ]
        )
        or (cols[0].this in [DataType.Type.BIGINT] and cols[1].this in [DataType.Type.BIGINT])
        or (cols[0].this in [DataType.Type.UBIGINT] and cols[1].this in [DataType.Type.UBIGINT])
    ):
        return ""
    return f"{type1} -> {type2}"


def match_schema(
    schema1: dict[str, str], schema2: dict[str, str], ignore_materialized: bool = True, ignore_alias: bool = True
) -> str | None:
    result = ""
    schema1 = filter_schema(schema1, skip_materialized=ignore_materialized, skip_alias=ignore_alias)
    schema2 = filter_schema(schema2, skip_materialized=ignore_materialized, skip_alias=ignore_alias)
    if schema1 == schema2:
        return None
    for key in sorted(schema1.keys()):
        if not schema2.get(key):
            result += f"- {key}: {schema1[key]}\n"
        else:
            diff = schema_diff(schema1[key], schema2[key])
            if diff:
                result += f"> {key}: {diff}\n"
    for key in sorted(schema2.keys()):
        if not schema1.get(key):
            result += f"+ {key}: {schema2[key]}\n"
    if not result:
        return None
    return result
