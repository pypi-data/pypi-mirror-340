"""Polars-based validator implementation."""

import logging
from typing import Optional

import patito as pt
import polars as pl
from patito.exceptions import _display_error_loc

from matrix_validator import util
from matrix_validator.checks import (
    CURIE_REGEX,
    DELIMITED_BY_PIPES,
    NO_LEADING_WHITESPACE,
    NO_TRAILING_WHITESPACE,
    STARTS_WITH_BIOLINK_REGEX,
)
from matrix_validator.checks.check_column_contains_biolink_model_agent_type import (
    validate as check_column_contains_biolink_model_agent_type,
)
from matrix_validator.checks.check_column_contains_biolink_model_knowledge_level import (
    validate as check_column_contains_biolink_model_knowledge_level,
)
from matrix_validator.checks.check_column_contains_biolink_model_prefix import validate as check_column_contains_biolink_model_prefix
from matrix_validator.checks.check_column_is_delimited_by_pipes import validate as check_column_is_delimited_by_pipes
from matrix_validator.checks.check_column_is_valid_curie import validate as check_column_is_valid_curie
from matrix_validator.checks.check_column_no_leading_whitespace import validate as check_column_no_leading_whitespace
from matrix_validator.checks.check_column_no_trailing_whitespace import validate as check_column_no_trailing_whitespace
from matrix_validator.checks.check_column_starts_with_biolink import validate as check_column_starts_with_biolink
from matrix_validator.checks.check_edge_ids_in_node_ids import validate as check_edge_ids_in_node_ids
from matrix_validator.validator import Validator

logger = logging.getLogger(__name__)

BIOLINK_KNOWLEDGE_LEVEL_KEYS = util.get_biolink_model_knowledge_level_keys()
BIOLINK_AGENT_TYPE_KEYS = util.get_biolink_model_agent_type_keys()


def create_edge_schema(prefixes: list[str]):
    """Create a EdgeSchema with a dynamic list of allowed prefixes."""

    class EdgeSchema(pt.Model):
        """EdgeSchema derived from Patito."""

        subject: str = pt.Field(constraints=[pt.field.str.contains(CURIE_REGEX), pt.field.str.contains_any(prefixes)])
        predicate: str = pt.Field(constraints=[pt.field.str.contains(STARTS_WITH_BIOLINK_REGEX)])
        object: str = pt.Field(constraints=[pt.field.str.contains(CURIE_REGEX), pt.field.str.contains_any(prefixes)])
        knowledge_level: str = pt.Field(constraints=[pt.field.str.contains_any(BIOLINK_KNOWLEDGE_LEVEL_KEYS)])
        agent_type: str = pt.Field(constraints=[pt.field.str.contains_any(BIOLINK_AGENT_TYPE_KEYS)])
        primary_knowledge_source: str
        aggregator_knowledge_source: str
        original_subject: str
        original_object: str
        publications: Optional[str]
        subject_aspect_qualifier: Optional[str]
        subject_direction_qualifier: Optional[str]
        object_aspect_qualifier: Optional[str]
        object_direction_qualifier: Optional[str]
        upstream_data_source: Optional[str]

    return EdgeSchema


def create_node_schema(prefixes: list[str]):
    """Create a NodeSchema with a dynamic list of allowed prefixes."""

    class NodeSchema(pt.Model):
        """NodeSchema derived from Patito."""

        id: str = pt.Field(constraints=[pt.field.str.contains(CURIE_REGEX), pt.field.str.contains_any(prefixes)])
        category: str = pt.Field(
            constraints=[
                pt.field.str.contains(STARTS_WITH_BIOLINK_REGEX),
                pt.field.str.contains(DELIMITED_BY_PIPES),
                pt.field.str.contains(NO_LEADING_WHITESPACE),
                pt.field.str.contains(NO_TRAILING_WHITESPACE),
            ]
        )
        name: Optional[str]
        description: Optional[str]
        equivalent_identifiers: Optional[str]
        all_categories: Optional[str]
        publications: Optional[str]
        labels: Optional[str]
        international_resource_identifier: Optional[str]

    return NodeSchema


class ValidatorPolarsImpl(Validator):
    """Polars-based validator implementation."""

    def __init__(self, config):
        """Create a new instance of the polars-based validator."""
        super().__init__(config)

    def validate(self, nodes_file_path, edges_file_path, limit: int | None = None):
        """Validate a knowledge graph as nodes and edges KGX TSV files."""
        validation_reports = []

        if nodes_file_path:
            tmp_val_violations = validate_kg_nodes(nodes_file_path, limit, self.prefixes)
            validation_reports.extend(tmp_val_violations)

        if edges_file_path:
            validation_reports.extend(validate_kg_edges(edges_file_path, limit, self.prefixes))

        if nodes_file_path and edges_file_path and not validation_reports:
            validation_reports.extend(validate_nodes_and_edges(nodes_file_path, edges_file_path, limit))

        # Write validation report
        self.write_report(validation_reports)
        logging.info(f"Validation report written to {self.get_report_file()}")


def validate_kg_nodes(nodes, limit, prefixes):
    """Validate a knowledge graph using optional nodes TSV files."""
    logger.info("Validating nodes TSV...")

    validation_reports = []

    # do an initial schema check
    schema_df = pl.scan_csv(nodes, separator="\t", has_header=True, ignore_errors=True, low_memory=True).limit(10).collect()
    superfluous_columns = []

    node_schema = create_node_schema(prefixes)

    try:
        node_schema.validate(schema_df, allow_missing_columns=True, allow_superfluous_columns=False)
    except pt.exceptions.DataFrameValidationError as ex:
        superfluous_columns.extend([_display_error_loc(e) for e in ex.errors() if e["type"] == "type_error.superfluouscolumns"])

    try:
        node_schema.validate(schema_df, allow_missing_columns=True, allow_superfluous_columns=True)
    except pt.exceptions.DataFrameValidationError as ex:
        logger.warning(f"number of schema violations: {len(ex.errors())}")
        validation_reports.append("\n".join(f"{e['msg']}: {_display_error_loc(e)}" for e in ex.errors()))
        return validation_reports

    # and if schema check is good, move on to data checks
    if not validation_reports:
        usable_columns = [pl.col("id"), pl.col("category")]

        main_df = pl.scan_csv(nodes, separator="\t", has_header=True, ignore_errors=True, low_memory=True).select(usable_columns)

        try:
            if limit:
                df = main_df.limit(limit).collect()
            else:
                df = main_df.collect()

            logger.info("collecting node counts")

            counts_df = df.select(
                [
                    (~pl.col("id").str.contains(CURIE_REGEX)).sum().alias("invalid_curie_id_count"),
                    (~pl.col("id").str.contains_any(prefixes)).sum().alias("invalid_contains_biolink_model_prefix_id_count"),
                    (~pl.col("category").str.contains(STARTS_WITH_BIOLINK_REGEX)).sum().alias("invalid_starts_with_biolink_category_count"),
                    (~pl.col("category").str.contains(DELIMITED_BY_PIPES)).sum().alias("invalid_delimited_by_pipes_category_count"),
                    (~pl.col("category").str.contains(NO_LEADING_WHITESPACE)).sum().alias("invalid_no_leading_whitespace_category_count"),
                    (~pl.col("category").str.contains(NO_TRAILING_WHITESPACE)).sum().alias("invalid_no_trailing_whitespace_category_count"),
                ]
            )

            logger.info(counts_df.head())

            if counts_df.get_column("invalid_curie_id_count").item(0) > 0:
                validation_reports.append(check_column_is_valid_curie(df, "id"))

            if counts_df.get_column("invalid_contains_biolink_model_prefix_id_count").item(0) > 0:
                validation_reports.append(check_column_contains_biolink_model_prefix(df, "id", prefixes))

            if counts_df.get_column("invalid_no_leading_whitespace_category_count").item(0) > 0:
                validation_reports.append(check_column_no_leading_whitespace(df, "category"))

            if counts_df.get_column("invalid_no_trailing_whitespace_category_count").item(0) > 0:
                validation_reports.append(check_column_no_trailing_whitespace(df, "category"))

            if counts_df.get_column("invalid_starts_with_biolink_category_count").item(0) > 0:
                validation_reports.append(check_column_starts_with_biolink(df, "category"))

            if counts_df.get_column("invalid_delimited_by_pipes_category_count").item(0) > 0:
                validation_reports.append(check_column_is_delimited_by_pipes(df, "category"))

            logger.info(f"number of total violations: {len(validation_reports)}")

        except pl.exceptions.ColumnNotFoundError as ex:
            logger.error(f"missing required column: {repr(ex)}")
            validation_reports.append(f"Missing required column: {repr(ex)}")
            return validation_reports

        if superfluous_columns:
            logger.warning(
                "The following columns are not recognised by the biolink model. "
                + "This is not an error but consider suggesting these to be added to "
                + f"biolink at https://github.com/biolink/biolink-model/issues.: {','.join(superfluous_columns)}"
            )

    return validation_reports


def validate_kg_edges(edges, limit, prefixes):
    """Validate a knowledge graph using optional edges TSV files."""
    logger.info("Validating edges TSV...")

    validation_reports = []

    # do an initial schema check
    schema_df = pl.scan_csv(edges, separator="\t", has_header=True, ignore_errors=True, low_memory=True).limit(10).collect()

    superfluous_columns = []

    edge_schema = create_edge_schema(prefixes)

    try:
        edge_schema.validate(schema_df, allow_missing_columns=True, allow_superfluous_columns=False)
    except pt.exceptions.DataFrameValidationError as ex:
        superfluous_columns.extend([_display_error_loc(e) for e in ex.errors() if e["type"] == "type_error.superfluouscolumns"])

    try:
        edge_schema.validate(schema_df, allow_missing_columns=True, allow_superfluous_columns=True)
    except pt.exceptions.DataFrameValidationError as ex:
        validation_reports.append("\n".join(f"{e['msg']}: {_display_error_loc(e)}" for e in ex.errors()))

    # and if schema check is good, move on to data checks
    if not validation_reports:
        usable_columns = [pl.col("subject"), pl.col("predicate"), pl.col("object"), pl.col("knowledge_level"), pl.col("agent_type")]

        main_df = pl.scan_csv(edges, separator="\t", has_header=True, ignore_errors=True, low_memory=True).select(usable_columns)

        try:
            if limit:
                df = main_df.limit(limit).collect()
            else:
                df = main_df.collect()

            logger.info("collecting edge counts")

            counts_df = df.select(
                [
                    (~pl.col("subject").str.contains(CURIE_REGEX)).sum().alias("invalid_curie_subject_count"),
                    (~pl.col("subject").str.contains_any(prefixes)).sum().alias("invalid_contains_biolink_model_prefix_subject_count"),
                    (~pl.col("predicate").str.contains(STARTS_WITH_BIOLINK_REGEX))
                    .sum()
                    .alias("invalid_starts_with_biolink_predicate_count"),
                    (~pl.col("object").str.contains(CURIE_REGEX)).sum().alias("invalid_curie_object_count"),
                    (~pl.col("object").str.contains_any(prefixes)).sum().alias("invalid_contains_biolink_model_prefix_object_count"),
                    (~pl.col("knowledge_level").str.contains_any(BIOLINK_KNOWLEDGE_LEVEL_KEYS))
                    .sum()
                    .alias("invalid_contains_biolink_model_knowledge_level_count"),
                    (~pl.col("agent_type").str.contains_any(BIOLINK_AGENT_TYPE_KEYS))
                    .sum()
                    .alias("invalid_contains_biolink_model_agent_type_count"),
                ]
            )

            logger.info(counts_df.head())

            if counts_df.get_column("invalid_curie_subject_count").item(0) > 0:
                validation_reports.append(check_column_is_valid_curie(df, "subject"))

            if counts_df.get_column("invalid_contains_biolink_model_prefix_subject_count").item(0) > 0:
                validation_reports.append(check_column_contains_biolink_model_prefix(df, "subject", prefixes))

            if counts_df.get_column("invalid_curie_object_count").item(0) > 0:
                validation_reports.append(check_column_is_valid_curie(df, "object"))

            if counts_df.get_column("invalid_contains_biolink_model_prefix_object_count").item(0) > 0:
                validation_reports.append(check_column_contains_biolink_model_prefix(df, "object", prefixes))

            if counts_df.get_column("invalid_starts_with_biolink_predicate_count").item(0) > 0:
                validation_reports.append(check_column_starts_with_biolink(df, "predicate"))

            if counts_df.get_column("invalid_contains_biolink_model_knowledge_level_count").item(0) > 0:
                validation_reports.append(
                    check_column_contains_biolink_model_knowledge_level(df, "knowledge_level", BIOLINK_KNOWLEDGE_LEVEL_KEYS)
                )

            if counts_df.get_column("invalid_contains_biolink_model_agent_type_count").item(0) > 0:
                validation_reports.append(check_column_contains_biolink_model_agent_type(df, "agent_type", BIOLINK_AGENT_TYPE_KEYS))

        except pl.exceptions.ColumnNotFoundError as ex:
            logger.error(f"missing required column: {repr(ex)}")
            validation_reports.append(f"Missing required column: {repr(ex)}")
            return validation_reports

        if superfluous_columns:
            logger.warning(
                "The following columns are not recognised by the biolink model. "
                + "This is not an error but consider suggesting these to be added to "
                + f"biolink at https://github.com/biolink/biolink-model/issues.: {','.join(superfluous_columns)}"
            )

    return validation_reports


def validate_nodes_and_edges(nodes, edges, limit):
    """Validate a knowledge graph nodes vs edges."""
    logger.info("Validating nodes & edges")

    edges_df = (
        pl.scan_csv(edges, separator="\t", has_header=True, ignore_errors=False, low_memory=True)
        .select([pl.col("subject"), pl.col("object")])
        .collect()
    )
    edge_ids = (
        pl.concat(
            items=[edges_df.select(pl.col("subject").alias("id")), edges_df.select(pl.col("object").alias("id"))],
            how="vertical",
            parallel=True,
        )
        .unique()
        .get_column("id")
        .to_list()
    )

    logger.info("collecting counts")

    main_df = pl.scan_csv(nodes, separator="\t", has_header=True, ignore_errors=False, low_memory=True).select([pl.col("id")])

    if limit:
        df = main_df.limit(limit).collect()
    else:
        df = main_df.collect()

    counts_df = df.select([(~pl.col("id").str.contains_any(edge_ids)).sum().alias("invalid_edge_ids_in_node_ids_count")])

    logger.info(counts_df.head())

    validation_reports = []

    if counts_df.get_column("invalid_edge_ids_in_node_ids_count").item(0) > 0:
        validation_reports.append(check_edge_ids_in_node_ids(df, edge_ids, nodes))

    return validation_reports
