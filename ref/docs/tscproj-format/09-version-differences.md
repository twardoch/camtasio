# Version Differences and Compatibility

Camtasia's `.tscproj` format has changed over time. This document explains the key differences and compatibility requirements.

## Version Identification

Each project file contains two version fields:

```json
{
  "version": "9.0",        // Format version
  "editRate": 705600000,   // Time precision
  "authoringClientName": {
    "name": "Camtasia",
    "platform": "Mac",
    "version": "2025.1.4"  // Application version
  }
}
```

## Major Format Versions

### Version 4.0 (Legacy)
- **Camtasia versions**: 2020 and earlier
- **Edit rate**: 60
- **Time units**: Basic ticks (60 per second)
- **Features**: Limited editing capabilities

### Version 9.0 (Current)
- **Camtasia versions**: 2021 and later
- **Edit rate**: 705600000
- **Time units**: High-precision units
- **Features**: Advanced editing with sub-frame accuracy

## Key Differences

### 1. Time Representation

#### Version 4.0
```json
{
  "editRate": 60,
  "start": 120,      // 2 seconds (120 / 60)
  "duration": 300    // 5 seconds (300 / 60)
}
```

#### Version 9.0
```json
{
  "editRate": 705600000,
  "start": 1411200000,     // 2 seconds
  "duration": 3528000000   // 5 seconds
}
```

**Conversion formulas**:
```
v9_time = v4_time * (705600000 / 60)
v4_time = v9_time * (60 / 705600000)
```

### 2. Property Additions

#### New in Version 9.0
```json
{
  "allowSubFrameEditing": false,
  "targetLoudness": -18.0,
  "shouldApplyLoudnessNormalization": true
}
```

These properties:
- Don't exist in v4.0
- Use sensible defaults when absent
- Must be preserved if present

### 3. Media Structure Changes

#### Version 4.0 Source Tracks
```json
"sourceTracks": [
  {
    "range": [0, 10000],
    "type": 0,
    "editRate": 30,
    "sampleRate": 30,      // Simple number
    "metaData": ""         // Often empty
  }
]
```

#### Version 9.0 Source Tracks
```json
"sourceTracks": [
  {
    "range": [0, 10000],
    "type": 0,
    "editRate": 1000,
    "sampleRate": "2997/100",  // Precise fraction
    "metaData": "filename.mp4;",
    "parameters": {}           // New field
  }
]
```

### 4. Sample Rate Representation

#### Version 4.0
- Integer or float: `30`, `29.97`
- Approximate for fractional rates

#### Version 9.0
- String fractions: `"2997/100"`, `"12081/200"`
- Exact representation

### 5. Animation Differences

#### Version 4.0
```json
"scale0": {
  "type": "double",
  "keyframes": [
    {
      "time": 0,
      "value": 1.0,
      "interp": "linr"
      // No endTime or duration
    }
  ]
}
```

#### Version 9.0
```json
"scale0": {
  "type": "double",
  "defaultValue": 1.0,    // Added default
  "keyframes": [
    {
      "time": 0,
      "endTime": 58800000,
      "value": 1.0,
      "interp": "linr",
      "duration": 58800000  // Explicit duration
    }
  ]
}
```

### 6. Effect Enhancements

#### Version 4.0
- Basic effects only
- Limited parameters
- No effect IDs

#### Version 9.0
- Extended effect library
- Effect IDs for referencing
- More parameter options
- Custom effect support

### 7. Transition Improvements

#### Version 4.0
```json
{
  "name": "Fade",
  "duration": 60,
  "rightMedia": 5
}
```

#### Version 9.0
```json
{
  "name": "Fade",
  "duration": 70560000,
  "rightMedia": 5,
  "attributes": {
    "bypass": false,
    "reverse": false,
    "trivial": false,
    "useAudioPreRoll": true,
    "useVisualPreRoll": true
  }
}
```

## Compatibility Guidelines

### Reading Files

1. **Check version first**
   ```javascript
   if (data.version === "4.0") {
     // Use v4.0 parsing logic
   } else if (data.version === "9.0") {
     // Use v9.0 parsing logic
   }
   ```

2. **Handle missing properties**
   ```javascript
   const allowSubFrame = data.allowSubFrameEditing ?? false;
   const loudness = data.targetLoudness ?? -18.0;
   ```

3. **Parse sample rates**
   ```javascript
   function parseSampleRate(rate) {
     if (typeof rate === 'string' && rate.includes('/')) {
       const [num, den] = rate.split('/');
       return parseFloat(num) / parseFloat(den);
     }
     return parseFloat(rate);
   }
   ```

### Writing Files

1. **Maintain version consistency**
   - Don't mix v4.0 and v9.0 properties
   - Match editRate to version

2. **Time value conversion**
   ```javascript
   function convertTime(time, fromRate, toRate) {
     return Math.round(time * (toRate / fromRate));
   }
   ```

3. **Preserve unknown properties**
   - Keep unrecognized properties
   - Ensures forward compatibility

### Upgrading Projects

To upgrade v4.0 to v9.0:

1. **Update version and editRate**
   ```json
   "version": "9.0",
   "editRate": 705600000
   ```

2. **Convert all time values**
   ```javascript
   const ratio = 705600000 / 60;
   newTime = Math.round(oldTime * ratio);
   ```

3. **Add new properties**
   ```json
   "allowSubFrameEditing": false,
   "targetLoudness": -18.0,
   "shouldApplyLoudnessNormalization": true
   ```

4. **Update sample rate format**
   ```javascript
   // Convert 29.97 to "2997/100"
   function toFraction(decimal, precision = 100) {
     const numerator = Math.round(decimal * precision);
     return `${numerator}/${precision}`;
   }
   ```

## Platform Differences

### Mac vs Windows
```json
"authoringClientName": {
  "platform": "Mac" | "Windows"
}
```

No format differences between platforms, but:
- File paths use forward slashes on both
- Media codec support varies
- Some effects are platform-specific

## Feature Support Matrix

| Feature | v4.0 | v9.0 |
|---------|------|------|
| Basic editing | ✓ | ✓ |
| Keyframe animation | ✓ | ✓ |
| Sub-frame editing | ✗ | ✓ |
| Loudness normalization | ✗ | ✓ |
| Fractional frame rates | Limited | ✓ |
| Advanced effects | Limited | ✓ |
| Custom effects | ✗ | ✓ |
| Effect IDs | ✗ | ✓ |
| Transition attributes | Basic | Full |

## Best Practices

1. **Version Detection**
   - Check version before processing
   - Support both formats when possible
   - Handle unknown versions gracefully

2. **Time Handling**
   - Use high-precision arithmetic
   - Round appropriately
   - Test edge cases

3. **Property Management**
   - Set defaults for missing properties
   - Preserve unrecognized properties
   - Validate data types

4. **Testing**
   - Test with files from multiple Camtasia versions
   - Verify time conversions work correctly
   - Check effect compatibility across versions