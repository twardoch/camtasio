#!/usr/bin/env bash
# this_file: example/test_comprehensive.sh

# Comprehensive test script for tscprojpy

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Change to script directory
cd $(dirname "$0")

echo -e "${BLUE}=== Comprehensive tscprojpy Test Suite ===${NC}\n"

# Test 1: Basic xyscale test
echo -e "${BLUE}Test 1: Basic XY scaling (150%)${NC}"
python -m tscprojpy.cli xyscale \
    --scale 150 \
    --input 2507vlteas2.cmproj/project.tscproj \
    --output test_output_xyscale_150.tscproj

if [ -f "test_output_xyscale_150.tscproj" ]; then
    echo -e "${GREEN}✓ XY scale 150% test passed${NC}\n"
else
    echo -e "${RED}✗ XY scale 150% test failed${NC}\n"
    exit 1
fi

# Test 2: Downscale test
echo -e "${BLUE}Test 2: Downscaling (50%)${NC}"
python -m tscprojpy.cli xyscale \
    --scale 50 \
    --input 2507vlteas2.cmproj/project.tscproj \
    --output test_output_xyscale_50.tscproj

if [ -f "test_output_xyscale_50.tscproj" ]; then
    echo -e "${GREEN}✓ XY scale 50% test passed${NC}\n"
else
    echo -e "${RED}✗ XY scale 50% test failed${NC}\n"
    exit 1
fi

# Test 3: Timescale test
echo -e "${BLUE}Test 3: Time scaling (200%)${NC}"
python -m tscprojpy.cli timescale \
    --scale 200 \
    --input 2507vlteas2.cmproj/project.tscproj \
    --output test_output_timescale_200.tscproj

if [ -f "test_output_timescale_200.tscproj" ]; then
    echo -e "${GREEN}✓ Time scale 200% test passed${NC}\n"
else
    echo -e "${RED}✗ Time scale 200% test failed${NC}\n"
    exit 1
fi

# Test 4: Timescale with fractional value
echo -e "${BLUE}Test 4: Time scaling with fractional value (125%)${NC}"
python -m tscprojpy.cli timescale \
    --scale 125.5 \
    --input 2507vlteas2.cmproj/project.tscproj \
    --output test_output_timescale_125_5.tscproj

if [ -f "test_output_timescale_125_5.tscproj" ]; then
    echo -e "${GREEN}✓ Time scale 125.5% test passed${NC}\n"
else
    echo -e "${RED}✗ Time scale 125.5% test failed${NC}\n"
    exit 1
fi

# Test 5: Verbose mode test
echo -e "${BLUE}Test 5: Verbose mode test${NC}"
python -m tscprojpy.cli xyscale \
    --scale 100 \
    --input 2507vlteas2.cmproj/project.tscproj \
    --output test_output_verbose.tscproj \
    --verbose > test_verbose_output.log 2>&1

if [ -s "test_verbose_output.log" ]; then
    echo -e "${GREEN}✓ Verbose mode test passed${NC}\n"
else
    echo -e "${RED}✗ Verbose mode test failed${NC}\n"
    exit 1
fi

# Test 6: Auto-generated output filename
echo -e "${BLUE}Test 6: Auto-generated output filename${NC}"
# Remove any existing auto-generated files first
rm -f 2507vlteas2.cmproj/project_175pct.tscproj

python -m tscprojpy.cli xyscale \
    --scale 175 \
    --input 2507vlteas2.cmproj/project.tscproj

if [ -f "2507vlteas2.cmproj/project_175pct.tscproj" ]; then
    echo -e "${GREEN}✓ Auto-generated filename test passed${NC}\n"
    rm -f 2507vlteas2.cmproj/project_175pct.tscproj
else
    echo -e "${RED}✗ Auto-generated filename test failed${NC}\n"
    exit 1
fi

# Test 7: Verify file contents are different
echo -e "${BLUE}Test 7: Verify scaled file is different from original${NC}"
original_size=$(wc -c < "2507vlteas2.cmproj/project.tscproj")
scaled_size=$(wc -c < "test_output_xyscale_150.tscproj")

if [ "$original_size" != "$scaled_size" ]; then
    echo -e "${GREEN}✓ File modification test passed (original: $original_size bytes, scaled: $scaled_size bytes)${NC}\n"
else
    echo -e "${RED}✗ File modification test failed - files are the same size${NC}\n"
    exit 1
fi

# Test 8: Version command
echo -e "${BLUE}Test 8: Version command${NC}"
python -m tscprojpy.cli version

echo -e "${GREEN}✓ Version command test passed${NC}\n"

# Cleanup test files
echo -e "${BLUE}Cleaning up test files...${NC}"
rm -f test_output_*.tscproj
rm -f test_verbose_output.log

echo -e "${GREEN}=== All tests passed! ===${NC}"