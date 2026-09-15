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
        grouped, skipped, bad = s2m.group_fields(rows)
        self.assertEqual(bad, [])
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


class TestParseMcp(unittest.TestCase):
    def test_package_and_tools(self):
        mcp = s2m.parse_mcp({"MCP": "@access-mcp/software-discovery | search_software, list_all_software"})
        self.assertTrue(mcp["available"])
        self.assertEqual(mcp["package"], "@access-mcp/software-discovery")
        self.assertEqual(mcp["tools"], [{"name": "search_software"}, {"name": "list_all_software"}])

    def test_package_only(self):
        mcp = s2m.parse_mcp({"MCP": "@access-mcp/events"})
        self.assertTrue(mcp["available"])
        self.assertEqual(mcp["package"], "@access-mcp/events")
        self.assertNotIn("tools", mcp)

    def test_blank_is_unavailable(self):
        self.assertEqual(s2m.parse_mcp({"MCP": ""}), {"available": False})

    def test_legacy_mcp_available_fallback(self):
        # No 'MCP' cell, but a legacy 'MCP Available' yes/no column.
        self.assertTrue(s2m.parse_mcp({"MCP Available": "yes"})["available"])
        self.assertFalse(s2m.parse_mcp({"MCP Available": "no"})["available"])


class TestApiEndpoint(unittest.TestCase):
    def test_api_column_maps_to_api_endpoint(self):
        inv = {("Support", "S"): {
            "Track": "Support", "Data Source": "S",
            "API": "https://support.access-ci.org/api/1.0/resources",
        }}
        fm, _ = s2m.build_frontmatter("S", "Support", [], inv)
        self.assertEqual(fm["api_endpoint"], "https://support.access-ci.org/api/1.0/resources")

    def test_blank_api_omitted(self):
        inv = {("Support", "S"): {"Track": "Support", "Data Source": "S", "API": ""}}
        fm, _ = s2m.build_frontmatter("S", "Support", [], inv)
        self.assertNotIn("api_endpoint", fm)


class TestErrorHeadings(unittest.TestCase):
    """A 'Data Source' heading that is a spreadsheet error (a broken lookup
    formula) is not a source; it and its rows are dropped and reported."""
    def test_error_heading_is_skipped(self):
        rows = [
            {"Data Source": "#NUM!", "Name": ""},
            {"Data Source": "", "Name": "orphan", "Type": "int", "Access": "Public",
             "Description": "d"},
            {"Data Source": "Real", "Name": ""},
            {"Data Source": "", "Name": "f", "Type": "int", "Access": "Public",
             "Description": "d"},
        ]
        grouped, skipped, bad = s2m.group_fields(rows)
        self.assertEqual(list(grouped), ["Real"])
        self.assertEqual(bad, ["#NUM!"])

    def test_blank_rows_not_reported(self):
        rows = [{"Data Source": "S", "Name": ""}, {"Data Source": "", "Name": ""}]
        _, skipped, _ = s2m.group_fields(rows)
        self.assertEqual(skipped, [])


class TestReadFieldsDirKeyedByTrack(unittest.TestCase):
    """Two tracks may each list a source of the same name; they stay separate."""
    def test_same_name_in_two_tracks(self):
        import tempfile
        from pathlib import Path
        header = "Data Source,Name,Type,Access,Description\n"
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "X - Metrics Fields.csv").write_text(
                header + "Publications,,,,\n,Year,int,Public,y\n")
            (Path(d) / "X - Allocations Fields.csv").write_text(
                header + "Publications,,,,\n")
            sources, _, warnings = s2m.read_fields_dir(Path(d))
        self.assertEqual(len(sources[("Metrics", "Publications")]["fields"]), 1)
        self.assertEqual(sources[("Allocations", "Publications")]["fields"], [])
        self.assertEqual(warnings, [])


class TestMcpUrl(unittest.TestCase):
    def test_url_first_segment_lands_in_url(self):
        mcp = s2m.parse_mcp({"MCP": "https://mcp.access-ci.org/events/mcp | search_events"})
        self.assertEqual(mcp["url"], "https://mcp.access-ci.org/events/mcp")
        self.assertNotIn("package", mcp)
        self.assertEqual(mcp["tools"], [{"name": "search_events"}])


class TestNewInventoryColumns(unittest.TestCase):
    def test_docs_sensitivity_request_access(self):
        inv = {("Support", "S"): {
            "Track": "Support", "Data Source": "S",
            "Docs": "https://support.access-ci.org/api-docs/events",
            "Sensitivity": "Low", "How to request access": "Ask the Support team",
        }}
        fm, _ = s2m.build_frontmatter("S", "Support", [], inv)
        self.assertEqual(fm["docs_url"], "https://support.access-ci.org/api-docs/events")
        self.assertEqual(fm["sensitivity"], "Low")
        self.assertEqual(fm["how_to_request_access"], "Ask the Support team")


class TestMergeFrontmatter(unittest.TestCase):
    """Regenerating over an existing file: sheet-owned keys come from the sheet,
    hand-curated keys and the existing id survive."""
    def setUp(self):
        self.existing = {
            "id": "events", "name": "Events and Training", "track": "Support",
            "description": "old desc", "api_endpoint": "https://old",
            "dynamic": False, "use_cases": ["q?"],
            "relationships": [{"type": "has_many", "target": "tags"}],
            "mcp": {"available": True, "package": "@access-mcp/events",
                    "tools": [{"name": "search_events", "method": "GET",
                               "description": "Search"}]},
            "fields": [{"name": "old_field", "type": "int", "access": "Public",
                        "description": "d"}],
        }

    def test_sheet_keys_replace_curated_keys_survive(self):
        sheet = {"id": "events_and_training", "name": "Events and Training",
                 "track": "Support", "description": "new desc",
                 "fields": [{"name": "title", "type": "varchar", "access": "Public",
                             "description": "t"}]}
        w = []
        merged = s2m.merge_frontmatter(self.existing, sheet, w, "Support/Events")
        self.assertEqual(merged["id"], "events")
        self.assertEqual(merged["description"], "new desc")
        self.assertEqual([f["name"] for f in merged["fields"]], ["title"])
        self.assertEqual(merged["use_cases"], ["q?"])
        self.assertEqual(merged["relationships"][0]["target"], "tags")
        self.assertIs(merged["dynamic"], False)
        self.assertNotIn("api_endpoint", merged)  # blank in sheet -> dropped
        self.assertTrue(any("dropped 'api_endpoint'" in m for m in w))
        self.assertEqual(list(merged)[:3], ["id", "name", "track"])  # order kept

    def test_empty_sheet_fields_keep_curated_fields(self):
        sheet = {"id": "events", "name": "Events and Training", "track": "Support",
                 "description": "d", "fields": []}
        w = []
        merged = s2m.merge_frontmatter(self.existing, sheet, w, "Support/Events")
        self.assertEqual(merged["fields"][0]["name"], "old_field")
        self.assertTrue(any("no field rows" in m for m in w))

    def test_mcp_tool_descriptions_ride_along(self):
        sheet = {"id": "events", "name": "Events and Training", "track": "Support",
                 "fields": [], "mcp": {"available": True,
                                       "url": "https://mcp.access-ci.org/events/mcp",
                                       "tools": [{"name": "search_events"},
                                                 {"name": "get_event_by_id"}]}}
        merged = s2m.merge_frontmatter(self.existing, sheet, [], "x")
        tools = {t["name"]: t for t in merged["mcp"]["tools"]}
        self.assertEqual(tools["search_events"]["method"], "GET")
        self.assertEqual(tools["search_events"]["description"], "Search")
        self.assertEqual(tools["get_event_by_id"], {"name": "get_event_by_id"})
        self.assertEqual(merged["mcp"]["url"], "https://mcp.access-ci.org/events/mcp")
        self.assertNotIn("package", merged["mcp"])

    def test_mcp_notes_ride_along(self):
        self.existing["mcp"] = {"available": False, "notes": "Too sensitive for MCP"}
        sheet = {"id": "events", "name": "Events and Training", "track": "Support",
                 "fields": [], "mcp": {"available": False}}
        merged = s2m.merge_frontmatter(self.existing, sheet, [], "x")
        self.assertEqual(merged["mcp"], {"available": False, "notes": "Too sensitive for MCP"})


class TestInventoryOnlySources(unittest.TestCase):
    def test_rows_missing_from_fields_tab_are_added_empty(self):
        sources = {("Support", "Events"): {"track": "Support", "name": "Events", "fields": [1]}}
        inv = {("Support", "Events"): {}, ("Support", "Chatbot"): {},
               ("Support", "#NUM!"): {}, ("", ""): {}}
        added = s2m.add_inventory_only_sources(sources, inv)
        self.assertEqual(added, [("Support", "Chatbot")])
        self.assertEqual(sources[("Support", "Chatbot")]["fields"], [])
        self.assertNotIn(("Support", "#NUM!"), sources)


class TestFindExisting(unittest.TestCase):
    def setUp(self):
        from pathlib import Path
        self.entry = (Path("events.md"), {"id": "events", "name": "Events and Training",
                                          "track": "Support"}, "")
        self.by_id = {"events": self.entry}
        self.by_name = {"Events and Training": [self.entry]}

    def test_matches_by_id_or_name_within_track(self):
        self.assertIs(s2m.find_existing(self.by_id, self.by_name, "events", "x", "Support"), self.entry)
        self.assertIs(s2m.find_existing(self.by_id, self.by_name, "events_and_training",
                                        "Events and Training", "Support"), self.entry)

    def test_other_track_does_not_match(self):
        self.assertIsNone(s2m.find_existing(self.by_id, self.by_name, "events",
                                            "Events and Training", "Metrics"))

    def test_same_name_two_tracks_each_find_their_own_file(self):
        from pathlib import Path
        metrics = (Path("publications.md"), {"id": "publications", "name": "Publications",
                                             "track": "Metrics"}, "")
        alloc = (Path("publications_allocations.md"),
                 {"id": "publications_allocations", "name": "Publications",
                  "track": "Allocations"}, "")
        by_id = {"publications": metrics, "publications_allocations": alloc}
        by_name = {"Publications": [metrics, alloc]}
        self.assertIs(s2m.find_existing(by_id, by_name, "publications", "Publications", "Metrics"), metrics)
        self.assertIs(s2m.find_existing(by_id, by_name, "publications", "Publications", "Allocations"), alloc)


class TestRenderMarkdown(unittest.TestCase):
    def test_body_preserved(self):
        out = s2m.render_markdown({"id": "x", "name": "X"}, "## Overview\n\nHi\n")
        self.assertTrue(out.startswith("---\nid: x\nname: X\n---\n\n## Overview"))
        fm, body = s2m.split_frontmatter(out)
        self.assertEqual(fm, {"id": "x", "name": "X"})
        self.assertEqual(body, "## Overview\n\nHi")

    def test_no_body(self):
        self.assertEqual(s2m.render_markdown({"id": "x"}), "---\nid: x\n---\n")


if __name__ == "__main__":
    unittest.main()
