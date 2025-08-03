#!/usr/bin/env bash
llms . "*.tscproj,*.txt"
uvx hatch clean
gitnextver .

# Get the current tag version without the 'v' prefix for PyPI
TAG_VERSION=$(git describe --tags --exact-match HEAD 2>/dev/null | sed 's/^v//')
if [ -n "$TAG_VERSION" ]; then
    echo "Building release version: $TAG_VERSION"
    # Set environment variable to override version detection
    export SETUPTOOLS_SCM_PRETEND_VERSION="$TAG_VERSION"
fi

uvx hatch build
uvx hatch publish
