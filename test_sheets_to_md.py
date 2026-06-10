#!/usr/bin/env python3
"""Tests for sheets_to_md converter. Run: python3 -m unittest test_sheets_to_md"""
import unittest
import sheets_to_md as s2m


class TestSlug(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(s2m.slugify("Affinity Groups"), "affinity_groups")

    def test_punctuation(self):
        self.assertEqual(s2m.slugify("XDMoD (OOD)"), "xdmod_ood")

    def test_ampersand_and_slash(self):
        self.assertEqual(s2m.slugify("RAC Registration/Attendance"),
                         "rac_registration_attendance")

    def test_collapses_repeats(self):
        self.assertEqual(s2m.slugify("A  -  B"), "a_b")


class TestReadType(unittest.TestCase):
    """Type is read verbatim from the sheet — no remapping. Bad values are the
    sheet's problem and get flagged by validation, not silently rewritten."""
    def test_passthrough_known(self):
        self.assertEqual(s2m.read_type("text"), "text")
        self.assertEqual(s2m.read_type("int"), "int")

    def test_invalid_value_passes_through_unchanged(self):
        # not normalized away — validation will flag it
        self.assertEqual(s2m.read_type("Video"), "Video")
        self.assertEqual(s2m.read_type("decimal, text, int"), "decimal, text, int")

    def test_blank_returns_none(self):
        self.assertIsNone(s2m.read_type(""))


class TestNormalizeAccess(unittest.TestCase):
    def test_comma_list_becomes_list(self):
        self.assertEqual(s2m.normalize_access("Public, Authenticated"),
                         ["Public", "Authenticated"])

    def test_plain_public_is_scalar(self):
        self.assertEqual(s2m.normalize_access("Public"), "Public")

    def test_blank(self):
        self.assertIsNone(s2m.normalize_access(""))


class TestIsPlaceholder(unittest.TestCase):
    def test_todo_name(self):
        self.assertTrue(s2m.is_placeholder_field({"Name": "TODO (Reports are new)"}))

    def test_todo_computed(self):
        self.assertTrue(s2m.is_placeholder_field(
            {"Name": "TODO (Computed from multiple API endpoint(s))"}))

    def test_blank_name(self):
        self.assertTrue(s2m.is_placeholder_field({"Name": ""}))

    def test_real_field(self):
        self.assertFalse(s2m.is_placeholder_field({"Name": "Endpoint Name"}))


class TestBuildField(unittest.TestCase):
    def test_full_field(self):
        # New sheet layout: 1/0 booleans, "Notes on Access" and "Notes" columns.
        row = {
            "Name": "Endpoint Name", "Type": "varchar", "Access": "Public",
            "Notes on Access": "", "Description": "XDMoD REST API Endpoint Name",
            "Required": "1", "Computed?": "0", "Notes": "", "MCP Name": "",
            "Semantic Type": "entity_name", "Primary Key (DBs only)": "",
            "Reference (DBs Only)": "",
        }
        f = s2m.build_field(row)
        self.assertEqual(f["name"], "Endpoint Name")
        self.assertEqual(f["type"], "varchar")
        self.assertEqual(f["access"], "Public")
        self.assertEqual(f["required"], True)  # "1" is truthy
        self.assertEqual(f["semantic_type"], "entity_name")
        # blank optionals omitted, not emitted as empty
        self.assertNotIn("mcp_name", f)
        self.assertNotIn("computed", f)  # "0" is the default, omit
        self.assertNotIn("references", f)
        self.assertNotIn("access_notes", f)
        self.assertNotIn("notes", f)

    def test_access_notes_from_column(self):
        row = {
            "Name": "Raw Data", "Type": "json", "Access": "Public, Authenticated",
            "Notes on Access": "Aggregate is public; per-user detail needs a token.",
            "Description": "Metrics payload", "Required": "0", "Computed?": "0",
            "Notes": "Returned by the data-access endpoints.", "MCP Name": "",
            "Semantic Type": "", "Primary Key (DBs only)": "", "Reference (DBs Only)": "",
        }
        f = s2m.build_field(row)
        self.assertEqual(f["access"], ["Public", "Authenticated"])
        self.assertEqual(f["access_notes"], "Aggregate is public; per-user detail needs a token.")
        self.assertEqual(f["notes"], "Returned by the data-access endpoints.")

    def test_authoritative_source_field(self):
        row = {
            "Name": "resource_id", "Type": "varchar", "Access": "Public",
            "Notes on Access": "", "Description": "Resource id", "Required": "1",
            "Computed?": "0", "Notes": "", "Authoritative Source": "CIDeR",
            "MCP Name": "", "Semantic Type": "entity_id",
            "Primary Key (DBs only)": "", "Reference (DBs Only)": "",
        }
        f = s2m.build_field(row)
        self.assertEqual(f["authoritative_source"], "CIDeR")

    def test_authoritative_source_omitted_when_blank(self):
        row = {
            "Name": "x", "Type": "text", "Access": "Public", "Notes on Access": "",
            "Description": "d", "Required": "0", "Computed?": "0", "Notes": "",
            "Authoritative Source": "", "MCP Name": "", "Semantic Type": "",
            "Primary Key (DBs only)": "", "Reference (DBs Only)": "",
        }
        self.assertNotIn("authoritative_source", s2m.build_field(row))

    def test_type_read_verbatim(self):
        # Whatever the sheet says is what we emit; validation polices it.
        row = {
            "Name": "Use Case Playlist", "Type": "Video", "Access": "Public",
            "Notes on Access": "", "Description": "Playlist", "Required": "0",
            "Computed?": "0", "Notes": "", "MCP Name": "", "Semantic Type": "media_ref",
            "Primary Key (DBs only)": "", "Reference (DBs Only)": "",
        }
        f = s2m.build_field(row)
        self.assertEqual(f["type"], "Video")
        self.assertEqual(f["semantic_type"], "media_ref")

    def test_dual_access_field(self):
        row = {
            "Name": "Raw Data", "Type": "json",
            "Access": "Public, Authenticated", "Notes on Access": "", "Description": "",
            "Required": "0", "Computed?": "0", "Notes": "", "MCP Name": "",
            "Semantic Type": "", "Primary Key (DBs only)": "",
            "Reference (DBs Only)": "",
        }
        f = s2m.build_field(row)
        self.assertEqual(f["type"], "json")
        self.assertEqual(f["access"], ["Public", "Authenticated"])
        # no Notes on Access provided -> no synthesized note
        self.assertNotIn("access_notes", f)


class TestParseFieldsCsv(unittest.TestCase):
    """Grouping: a row with Data Source starts a source; blank-DS rows are its fields."""
    def test_groups_fields_under_source(self):
        rows = [
            {"Data Source": "XDMoD Open API Documentation", "Name": ""},
            {"Data Source": "", "Name": "Endpoint Name", "Type": "varchar",
             "Access": "Public", "Description": "d", "Required": "TRUE",
             "Computed?": "FALSE", "MCP Name": "", "Semantic Type": "entity_name",
             "Primary Key (DBs only)": "", "Reference (DBs only)": ""},
            {"Data Source": "", "Name": "TODO", "Type": "", "Access": "",
             "Description": "", "Required": "", "Computed?": "", "MCP Name": "",
             "Semantic Type": "", "Primary Key (DBs only)": "",
             "Reference (DBs only)": ""},
        ]
        grouped, skipped = s2m.group_fields(rows)
        self.assertIn("XDMoD Open API Documentation", grouped)
        self.assertEqual(len(grouped["XDMoD Open API Documentation"]), 1)
        self.assertEqual(len(skipped), 1)  # the TODO row


class TestCanonicalSources(unittest.TestCase):
    """Blank 'Canonical Sources' -> the source is canonical. A non-blank value
    is a list of other inventory sources this one derives from."""
    def test_blank_is_canonical(self):
        is_canon, canon = s2m.parse_canonical_sources("")
        self.assertTrue(is_canon)
        self.assertIsNone(canon)

    def test_single_other_source(self):
        is_canon, canon = s2m.parse_canonical_sources("ACCESS Support Drupal")
        self.assertFalse(is_canon)
        self.assertEqual(canon, ["access_support_drupal"])

    def test_multiple_other_sources(self):
        is_canon, canon = s2m.parse_canonical_sources("XDMoD, NetSage")
        self.assertFalse(is_canon)
        self.assertEqual(canon, ["xdmod", "netsage"])

    def test_none_literal_is_canonical(self):
        # a cell literally reading "none" means no upstream -> canonical
        is_canon, canon = s2m.parse_canonical_sources("none")
        self.assertTrue(is_canon)
        self.assertIsNone(canon)


class TestInventoryEnrichment(unittest.TestCase):
    def test_storage_location_and_canonical(self):
        inv = {("Metrics", "XDMoD Open API Documentation"): {
            "Track": "Metrics", "Data Source": "XDMoD Open API Documentation",
            "Category": "Metrics & Reporting", "Access Level": "Public",
            "User-Facing Priority": "High", "Storage Location": "XDMoD Web Portal",
            "Canonical Sources": "", "Notes": "API docs.",
        }}
        fm, matched = s2m.build_frontmatter(
            "XDMoD Open API Documentation", "Metrics", [], inv)
        self.assertTrue(matched)
        self.assertEqual(fm["storage_location"], "XDMoD Web Portal")
        self.assertEqual(fm["priority"], "High")
        self.assertTrue(fm["is_canonical"])
        self.assertNotIn("canonical_source", fm)

    def test_non_canonical_lists_sources(self):
        inv = {("Metrics", "Derived Thing"): {
            "Track": "Metrics", "Data Source": "Derived Thing",
            "Canonical Sources": "XDMoD, NetSage", "Storage Location": "",
        }}
        fm, _ = s2m.build_frontmatter("Derived Thing", "Metrics", [], inv)
        self.assertFalse(fm["is_canonical"])
        self.assertEqual(fm["canonical_source"], ["xdmod", "netsage"])

    def test_optional_id_column_overrides_slug(self):
        # The sheet has no id column today; ids derive from the name. But if an
        # optional "id" column is added later, it overrides the derived value.
        inv = {("Metrics", "XDMoD Metrics"): {
            "Track": "Metrics", "Data Source": "XDMoD Metrics", "id": "xdmod",
            "Canonical Sources": "", "Storage Location": "",
        }}
        fm, _ = s2m.build_frontmatter("XDMoD Metrics", "Metrics", [], inv)
        self.assertEqual(fm["id"], "xdmod")
        self.assertEqual(fm["name"], "XDMoD Metrics")

    def test_id_falls_back_to_slug_when_absent(self):
        inv = {("Metrics", "XDMoD Metrics"): {
            "Track": "Metrics", "Data Source": "XDMoD Metrics",
            "Canonical Sources": "", "Storage Location": "",
        }}
        fm, _ = s2m.build_frontmatter("XDMoD Metrics", "Metrics", [], inv)
        self.assertEqual(fm["id"], "xdmod_metrics")

    def test_id_slug_when_no_inventory_match(self):
        fm, _ = s2m.build_frontmatter("XDMoD Metrics", "Metrics", [], None)
        self.assertEqual(fm["id"], "xdmod_metrics")

    def test_description_and_notes_columns(self):
        # Description column -> description; Notes column -> notes (distinct).
        inv = {("Metrics", "S"): {
            "Track": "Metrics", "Data Source": "S",
            "Description": "Usage metrics and findings",
            "Notes": "Porting to JIRA soon",
            "Canonical Sources": "", "Storage Location": "",
        }}
        fm, _ = s2m.build_frontmatter("S", "Metrics", [], inv)
        self.assertEqual(fm["description"], "Usage metrics and findings")
        self.assertEqual(fm["notes"], "Porting to JIRA soon")

    def test_remaining_inventory_columns(self):
        inv = {("Metrics", "S"): {
            "Track": "Metrics", "Data Source": "S",
            "Data Access mechanism(s)": "REST API",
            "Refresh Frequency": "Daily",
            "Query Capacity": "High",
            "Canonical Sources": "", "Storage Location": "",
        }}
        fm, _ = s2m.build_frontmatter("S", "Metrics", [], inv)
        self.assertEqual(fm["data_access_mechanism"], "REST API")
        self.assertEqual(fm["refresh_frequency"], "Daily")
        self.assertEqual(fm["query_capacity"], "High")

    def test_remaining_columns_omitted_when_blank(self):
        inv = {("Metrics", "S"): {
            "Track": "Metrics", "Data Source": "S",
            "Data Access mechanism(s)": "",
            "Refresh Frequency": "", "Query Capacity": "",
            "Canonical Sources": "", "Storage Location": "",
        }}
        fm, _ = s2m.build_frontmatter("S", "Metrics", [], inv)
        for k in ("data_access_mechanism", "refresh_frequency", "query_capacity"):
            self.assertNotIn(k, fm)


if __name__ == "__main__":
    unittest.main()
