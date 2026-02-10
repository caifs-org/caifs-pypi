#!/usr/bin/env bash
# Downloads caifs and caifs-common release tarballs into src/caifs/_vendor/.
# Usage: ./scripts/vendor.sh [caifs_version] [common_version]
#   Versions should be tags like "v0.6.2". Defaults to latest.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR_DIR="$REPO_ROOT/src/caifs/_vendor"

CAIFS_VERSION="${1:-latest}"
COMMON_VERSION="${2:-latest}"

fetch_tag() {
    local repo="$1" requested="$2"
    if [ "$requested" = "latest" ]; then
        gh release view --repo "caifs-org/$repo" --json tagName --jq .tagName
    else
        echo "$requested"
    fi
}

echo "==> Resolving versions..."
CAIFS_TAG=$(fetch_tag caifs "$CAIFS_VERSION")
COMMON_TAG=$(fetch_tag caifs-common "$COMMON_VERSION")
echo "    caifs:        $CAIFS_TAG"
echo "    caifs-common: $COMMON_TAG"

# Clean previous vendor contents (preserve .gitkeep)
find "$VENDOR_DIR" -mindepth 1 ! -name '.gitkeep' -exec rm -rf {} + 2>/dev/null || true

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# --- caifs framework ---
echo "==> Downloading caifs $CAIFS_TAG..."
gh release download "$CAIFS_TAG" --repo caifs-org/caifs --pattern 'release.tar.gz' --dir "$TMPDIR"
tar -xzf "$TMPDIR/release.tar.gz" -C "$TMPDIR"

# The tarball extracts to caifs/config/{bin,lib}
cp -r "$TMPDIR/caifs/config/bin" "$VENDOR_DIR/bin"
cp -r "$TMPDIR/caifs/config/lib" "$VENDOR_DIR/lib"

rm -f "$TMPDIR/release.tar.gz"
rm -rf "$TMPDIR/caifs"

# --- caifs-common collection ---
echo "==> Downloading caifs-common $COMMON_TAG..."
gh release download "$COMMON_TAG" --repo caifs-org/caifs-common --pattern 'release.tar.gz' --dir "$TMPDIR"
mkdir -p "$VENDOR_DIR/collections"
tar -xzf "$TMPDIR/release.tar.gz" -C "$VENDOR_DIR/collections"

echo ""
echo "Vendored successfully:"
echo "  caifs:        $CAIFS_TAG"
echo "  caifs-common: $COMMON_TAG"
echo "  location:     $VENDOR_DIR"
