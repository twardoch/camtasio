#!/usr/bin/env bash
llms . "*.tscproj,*.txt"
uvx hatch clean
gitnextver .
uvx hatch build
uvx hatch publish
