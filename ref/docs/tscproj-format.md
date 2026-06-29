# Camtasia .tscproj File Format Documentation

## Overview

The `.tscproj` file is TechSmith Camtasia's project file. It's a JSON document containing all data needed to reconstruct a video editing project: media references, timeline structure, effects, and settings.

## File Structure

A `.tscproj` file has this top-level structure:

```json
{
  "title": "",
  "description": "",
  "author": "",
  "targetLoudness": -18.0,
  "shouldApplyLoudnessNormalization": true,
  "videoFormatFrameRate": 60,
  "audioFormatSampleRate": 44100,
  "allowSubFrameEditing": false,
  "width": 1280.0,
  "height": 720.0,
  "version": "9.0",
  "editRate": 705600000,
  "authoringClientName": {...},
  "sourceBin": [...],
  "timeline": {...}
}
```

## Root-Level Properties

### Project Metadata
- **`title`** (string): Project title
- **`description`** (string): Project description
- **`author`** (string): Project author

### Canvas Settings
- **`width`** (float): Canvas width in pixels
- **`height`** (float): Canvas height in pixels

### Audio/Video Settings
- **`videoFormatFrameRate`** (integer): Target frame rate (30, 60, etc.)
- **`audioFormatSampleRate`** (integer): Audio sample rate in Hz (44100, 48000, etc.)
- **`targetLoudness`** (float): Target loudness in LUFS (usually -18.0)
- **`shouldApplyLoudnessNormalization`** (boolean): Enable loudness normalization
- **`allowSubFrameEditing`** (boolean): Enable sub-frame editing

### Technical Properties
- **`version`** (string): Project format version ("4.0", "9.0", etc.)
- **`editRate`** (integer): Time base for timing calculations
  - Older versions: 60 (ticks per second)
  - Newer versions: 705600000 (higher precision)
- **`authoringClientName`** (object): Camtasia version information
  ```json
  {
    "name": "Camtasia",
    "platform": "Mac" | "Windows",
    "version": "2025.1.4"
  }
  ```

## Source Media (sourceBin)

The `sourceBin` array contains all imported media files:

```json
"sourceBin": [
  {
    "id": 1,
    "src": "./media/1752976336.728338/filename.mp4",
    "rect": [0, 0, 1920, 1080],
    "lastMod": "20250419T143221",
    "loudnessNormalization": true,
    "sourceTracks": [...],
    "metadata": {...}
  }
]
```

### Source Item Properties
- **`id`** (integer): Unique identifier
- **`src`** (string): Relative path to media file
- **`rect`** (array[4]): Bounding rectangle [x, y, width, height]
- **`lastMod`** (string): Last modification timestamp (ISO format)
- **`loudnessNormalization`** (boolean): Audio normalization setting

### Source Tracks

Each source item contains `sourceTracks` describing media streams:

```json
"sourceTracks": [
  {
    "range": [0, 9817],
    "type": 0,
    "editRate": 1000,
    "trackRect": [0, 0, 1280, 720],
    "sampleRate": 60,
    "bitDepth": 0,
    "numChannels": 0,
    "integratedLUFS": 100.0,
    "peakLevel": -1.0,
    "tag": 0,
    "metaData": "...",
    "parameters": {}
  }
]
```

#### Track Types
- **`type: 0`**: Video
- **`type: 1`**: Image
- **`type: 2`**: Audio

## Timeline Structure

The timeline contains edit information:

```json
"timeline": {
  "id": 22,
  "sceneTrack": {
    "scenes": [
      {
        "csml": {
          "tracks": [...]
        }
      }
    ]
  }
}
```

### Track Structure

Timeline tracks contain media items:

```json
{
  "trackIndex": 0,
  "medias": [...],
  "parameters": {},
  "ident": "",
  "audioMuted": false,
  "videoHidden": false,
  "magnetic": false,
  "matte": 0,
  "solo": false,
  "metadata": {
    "IsLocked": "False",
    "trackHeight": "54"
  }
}
```

## Media Types

Media items use these `_type` values:

### Video Types
- **`VMFile`**: Video from sourceBin
- **`ScreenVMFile`**: Screen recording
- **`IMFile`**: Still image
- **`UnifiedMedia`**: Combined video/audio

### Audio Types
- **`AMFile`**: Audio file

### Annotations
- **`Callout`**: Annotation object
- **`Group`**: Group of items

### Common Media Properties

```json
{
  "id": 25,
  "_type": "VMFile",
  "src": 1,  // References sourceBin ID
  "trackNumber": 0,
  "attributes": {
    "ident": "clip_name"
  },
  "parameters": {
    "translation0": 0.0,    // X position
    "translation1": 0.0,    // Y position
    "scale0": 1.0,          // X scale
    "scale1": 1.0,          // Y scale
    "rotation0": 0.0,       // X rotation
    "rotation1": 0.0,       // Y rotation
    "rotation2": 0.0,       // Z rotation
    "geometryCrop0": 0.0,   // Left crop
    "geometryCrop1": 0.0,   // Top crop
    "geometryCrop2": 0.0,   // Right crop
    "geometryCrop3": 0.0,   // Bottom crop
    "opacity": 1.0
  },
  "effects": [],
  "start": 164640000,
  "duration": 1081920000,
  "mediaStart": 4727520000,
  "mediaDuration": 1081920000,
  "scalar": 1,
  "metadata": {...},
  "animationTracks": {...}
}
```

## Timing and Duration

Time values depend on project version:

- **Older versions**: Ticks (60 per second)
- **Newer versions**: High-precision units (based on editRate)

Key timing properties:
- **`start`**: Timeline start position
- **`duration`**: Timeline duration
- **`mediaStart`**: Source media start point
- **`mediaDuration`**: Source media duration

## Keyframe Animation

Animated properties use keyframes:

```json
"scale0": {
  "type": "double",
  "defaultValue": 1.0,
  "keyframes": [
    {
      "endTime": 58800000,
      "time": 11760000,
      "value": 0.444444444444444,
      "interp": "linr",
      "duration": 47040000
    }
  ]
}
```

### Keyframe Properties
- **`time`**: Keyframe timestamp
- **`endTime`**: Segment end time
- **`value`**: Property value
- **`interp`**: Interpolation ("linr" = linear)
- **`duration`**: Time to next keyframe

## Callout Objects

Callouts are annotation elements:

```json
{
  "_type": "Callout",
  "def": {
    "kind": "remix",
    "shape": "shape-rectangle",
    "style": "basic",
    "corner-radius": 8.0,
    "fill-color-red": 0.0,
    "fill-color-green": 0.0,
    "fill-color-blue": 0.0,
    "fill-color-opacity": 1.0,
    "stroke-color-red": 1.0,
    "stroke-color-green": 1.0,
    "stroke-color-blue": 1.0,
    "stroke-color-opacity": 1.0,
    "stroke-width": 0.0,
    "width": 240.0,
    "height": 180.0,
    "fill-style": "solid",
    "stroke-style": "solid"
  }
}
```

## Effects and Transitions

Effects appear in media item `effects` arrays:

```json
"effects": [
  {
    "name": "Effect Name",
    "parameters": {...}
  }
]
```

Transitions between clips:

```json
"transitions": [
  {
    "name": "Glitch",
    "duration": 294000000,
    "rightMedia": 36,
    "attributes": {
      "Random": 0.0,
      "bypass": false,
      "reverse": false
    }
  }
]
```

## Version Differences

### Camtasia 2020 and Earlier
- Version: "4.0"
- Edit rate: 60
- Simple timing

### Camtasia 2021 and Later
- Version: "9.0"
- Edit rate: 705600000
- High-precision timing
- `allowSubFrameEditing` support

## File References

Media files use relative paths, typically organized in timestamped folders:

```
./media/1752976336.728338/filename.mp4
```

## Parsing Guidelines

1. **Check version first** - Handle format differences appropriately
2. **Convert time values** - Account for different editRate values
3. **Handle missing media** - Files may be moved or deleted
4. **Watch property types** - Numbers sometimes stored as strings
5. **Expect missing fields** - Not all properties appear in every file

## Common Operations

### Project Scaling
When changing resolution (1080p to 4K, etc.):
- Update root `width` and `height`
- Adjust all `rect` and `trackRect` values
- Modify position properties (`translation0`, `translation1`)
- Scale size properties (`scale0`, `scale1`, `width`, `height`)
- Update animated property keyframe values

### Duration Calculation
Convert timeline duration to seconds:
```
duration_seconds = duration / editRate
```

### Media Type Identification
- Audio tracks: `numChannels > 0`
- Video tracks: Check `trackRect` dimensions
- Track types: `type` field (0=video, 1=image, 2=audio)