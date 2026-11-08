from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def test_fork_accepts_contributions_without_a_cla_signature() -> None:
    policy = (ROOT / "legal/CLA.md").read_text()
    contributing = (ROOT / ".github/CONTRIBUTING.md").read_text()

    assert "No separate Contributor License Agreement or signature is required" in policy
    assert "licence covering" in policy
    assert "No separate Contributor License Agreement or signature is required" in contributing
    assert not (ROOT / ".github/workflows/cla.yml").exists()


def test_attribution_has_no_signature_branch_lookup() -> None:
    attribution = (ROOT / ".github/scripts/release_attribution.py").read_text()

    assert "cla-signatures" not in attribution
    assert "validate_pr_cla" not in attribution
    assert "validate_pr_attribution(" in attribution


def test_license_preserves_upstream_and_attributes_modifications() -> None:
    license_text = (ROOT / "LICENSE.md").read_text()

    assert "Copyright (c) 2025 Cua AI, Inc." in license_text
    assert "Modifications Copyright (c) 2026 goat-si" in license_text
    assert "Permission is hereby granted, free of charge" in license_text
