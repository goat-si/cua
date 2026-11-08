from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


PINNED_UPSTREAM_FILES = (
    "apps/cua-spaces-macos/scripts/fetch-cua-driver.sh",
    "apps/cua-spaces-macos/scripts/fetch-spacesd.sh",
    "libs/cua/crates/cua-vmm/src/lume/builtin.rs",
    "libs/cua-driver/python/build_wheel.py",
    "libs/cua-driver/hyprland-plugin/packaging/release/PKGBUILD.in",
    "libs/cua-driver/hyprland-plugin/packaging/release/profile_download_recipe.py",
    "libs/cua-driver/hyprland-plugin/packaging/release/test_profile_download_recipe.py",
    "libs/cua-driver/rust/crates/cua-driver-e2e/tests/perception_capture_loop_test.rs",
    "libs/images/omarchy/Dockerfile",
    "libs/xfce/Dockerfile",
    "libs/kasm/Dockerfile",
    "libs/qemu-docker/linux/src/vm/setup/setup-spacesd.sh",
    "libs/qemu-docker/windows/src/vm/setup/setup-spacesd.ps1",
    "libs/lume/scripts/setup-cua.sh",
    "libs/python/cua-sandbox/cua_sandbox/builder/build.py",
)


CURRENT_REPOSITORY_FILES = (
    "apps/cua-spaces-macos/Sources/CuaSpacesMacKit/Models/UpdatesModel.swift",
    "apps/cua-spaces-desktop/src/updater.ts",
    "apps/cua-spaces/src-tauri/tauri.conf.json",
    "libs/cua-spacesd/packaging/install.sh",
    "libs/cua-driver/scripts/_install-rust.sh",
    "libs/cua/crates/cua-spaces-app-core/src/about.rs",
)


def test_historical_pinned_assets_stay_upstream() -> None:
    for name in PINNED_UPSTREAM_FILES:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "trycua/cua" in text, name
        assert "releases/download" in text, name
        assert "goat-si/goat-cua/releases/download" not in text, name


def test_current_install_and_update_links_use_goat_cua() -> None:
    for name in CURRENT_REPOSITORY_FILES:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "goat-si/goat-cua" in text, name
        assert "releases/download" in text, name


def test_linux_image_distinguishes_pinned_and_latest_downloads() -> None:
    text = (ROOT / "libs/images/linux/Dockerfile").read_text(encoding="utf-8")
    assert "default_url='https://github.com/trycua/cua/releases/download/" in text
    assert "CUA_SPACESD_RELEASE_URL=\"https://github.com/goat-si/goat-cua/releases/download/" in text
    assert "default_url='https://github.com/trycua/cua/releases/download/cua-sdk-v" in text


def test_pinned_driver_keeps_checksum_and_signature_verification() -> None:
    driver = (ROOT / "apps/cua-spaces-macos/scripts/fetch-cua-driver.sh").read_text()
    spacesd = (ROOT / "apps/cua-spaces-macos/scripts/fetch-spacesd.sh").read_text()
    lume = (ROOT / "libs/cua/crates/cua-vmm/src/lume/builtin.rs").read_text()

    assert "CUA_DRIVER_RELEASE_BASE_URL" in driver
    assert "got_sha" in driver
    assert "codesign --verify" in driver
    assert "lipo" in driver
    assert '.sha256"' in spacesd
    assert "pub const SHA256" in lume
    assert "pub const TEAM_ID" in lume
