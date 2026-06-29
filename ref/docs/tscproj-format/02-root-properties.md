# Root Level Properties

This document describes the top-level properties of a `.tscproj` file. These settings control project metadata, canvas size, video and audio parameters, version info, and content structure.

## Project Metadata

### `title` (string)
Project title.  
Default: `""`  
Example: `"My Tutorial Video"`

### `description` (string)
Project description or notes.  
Default: `""`  
Example: `"Introduction video for product launch"`

### `author` (string)
Name of the project creator.  
Default: `""`  
Example: `"John Smith"`

## Canvas Dimensions

### `width` (float)
Canvas width in pixels.  
Required: Yes  
Common values: `1920.0`, `1280.0`, `3840.0`  
Example: `1920.0`

### `height` (float)
Canvas height in pixels.  
Required: Yes  
Common values: `1080.0`, `720.0`, `2160.0`  
Example: `1080.0`

## Video Settings

### `videoFormatFrameRate` (integer)
Target output frame rate.  
Common values: `30`, `60`, `24`, `25`  
Example: `60`

### `allowSubFrameEditing` (boolean)
Enables sub-frame editing precision. Available in version 9.0+.  
Default: `false`  
Example: `false`

## Audio Settings

### `audioFormatSampleRate` (integer)
Audio sample rate in Hz.  
Common values: `44100`, `48000`  
Example: `44100`

### `targetLoudness` (float)
Target loudness in LUFS.  
Default: `-18.0`  
Range: Typically -23.0 to -16.0  
Example: `-18.0`

### `shouldApplyLoudnessNormalization` (boolean)
Applies loudness normalization to exported audio.  
Default: `true`  
Example: `true`

## Version Information

### `version` (string)
Project format version.  
Values:
- `"4.0"` – Camtasia 2020 and earlier
- `"9.0"` – Camtasia 2021 and later  
Required: Yes  
Example: `"9.0"`

### `editRate` (integer)
Time base used for all time values in the project.  
Values:
- `60` – Version 4.0
- `705600000` – Version 9.0 (higher precision)  
Required: Yes  
Usage: `seconds = timeValue / editRate`

### `authoringClientName` (object)
Identifies the Camtasia version that created the project.

Structure:
```json
{
  "name": "Camtasia",
  "platform": "Mac" | "Windows",
  "version": "2025.1.4"
}
```

Sub-properties:
- `name`: Always `"Camtasia"`
- `platform`: Either `"Mac"` or `"Windows"`
- `version`: Camtasia version string

## Content Arrays

### `sourceBin` (array)
List of all media sources used in the project.  
Required: Yes  
See: @03-source-media.md

### `timeline` (object)
Main timeline structure containing scenes and tracks.  
Required: Yes  
See: @04-timeline-structure.md

## Complete Example

```json
{
  "title": "Product Demo",
  "description": "Q1 2024 product demonstration video",
  "author": "Marketing Team",
  "targetLoudness": -18.0,
  "shouldApplyLoudnessNormalization": true,
  "videoFormatFrameRate": 60,
  "audioFormatSampleRate": 44100,
  "allowSubFrameEditing": false,
  "width": 1920.0,
  "height": 1080.0,
  "version": "9.0",
  "editRate": 705600000,
  "authoringClientName": {
    "name": "Camtasia",
    "platform": "Mac",
    "version": "2025.1.4"
  },
  "sourceBin": [...],
  "timeline": {...}
}
```

## Property Requirements by Version

### Version 4.0 Required Properties
- `width`, `height`
- `version`
- `editRate`
- `authoringClientName`
- `sourceBin`
- `timeline`

### Version 9.0 Additional Properties
- `allowSubFrameEditing`
- `targetLoudness`
- `shouldApplyLoudnessNormalization`

## Default Values

When creating new projects programmatically, use these defaults:

| Property                        | Default Value       |
|--------------------------------|---------------------|
| `title`                        | `""`                |
| `description`                  | `""`                |
| `author`                       | `""`                |
| `targetLoudness`               | `-18.0`             |
| `shouldApplyLoudnessNormalization` | `true`          |
| `videoFormatFrameRate`         | `30` or `60`        |
| `audioFormatSampleRate`        | `44100`             |
| `allowSubFrameEditing`         | `false`             |

## Validation Rules

1. **Dimensions**: `width` and `height` must be positive numbers.
2. **Frame Rate**: Must be a standard video frame rate (e.g., 24, 25, 30, 60).
3. **Sample Rate**: Must be a standard audio sample rate (e.g., 44100, 48000).
4. **Version**: Must align with the correct `editRate`.
5. **Edit Rate**:
   - Version 4.0: Must be `60`
   - Version 9.0: Must be `705600000`