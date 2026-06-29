# Media Item Types

Media items are clips, images, audio files, and annotations placed on the timeline. Each type has specific properties and behaviors.

## Common Media Properties

All media items share these base properties:

```json
{
  "id": 25,
  "_type": "VMFile",
  "src": 1,
  "trackNumber": 0,
  "attributes": {
    "ident": "clip_name"
  },
  "parameters": {...},
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

### Core Properties

#### `id` (integer)
Unique identifier for this media item. Must be unique across the entire timeline.

#### `_type` (string)
Media type identifier. See media types below for valid values.

#### `src` (integer)
Source media ID from sourceBin. Required for all types except generated content. References `sourceBin[].id`.

#### `trackNumber` (integer)
Source track to use for multi-track sources. Default: `0`. Example: `0` for video, `1` for audio in the same file.

### Timing Properties

#### `start` (integer)
Position on timeline. Units: project edit rate. Required.

#### `duration` (integer)
Length on timeline. Units: project edit rate. Required.

#### `mediaStart` (integer)
In-point within source media. Units: source media edit rate. Default: `0`.

#### `mediaDuration` (integer)
Length of source media used. Units: source media edit rate. Default: same as `duration`.

#### `scalar` (float)
Playback speed multiplier. Default: `1`. Examples: `2` = double speed, `0.5` = half speed.

## Video Media Types

### VMFile
Basic video clip.

```json
{
  "_type": "VMFile",
  "src": 1,
  "parameters": {
    "translation0": 0.0,
    "translation1": 0.0,
    "scale0": 1.0,
    "scale1": 1.0,
    "rotation0": 0.0,
    "rotation1": 0.0,
    "rotation2": 0.0,
    "opacity": 1.0
  }
}
```

### ScreenVMFile
Screen recording with audio sync control.

```json
{
  "_type": "ScreenVMFile",
  "src": 2,
  "parameters": {
    // Same as VMFile
  },
  "systemAudioOffset": 0
}
```

### UnifiedMedia
Combined video and audio tracks from the same source.

```json
{
  "_type": "UnifiedMedia",
  "video": {
    "id": 16,
    "_type": "ScreenVMFile",
    "src": 1,
    "trackNumber": 1
  },
  "audio": {
    "id": 17,
    "_type": "AMFile",
    "src": 1,
    "trackNumber": 0
  }
}
```

## Audio Media Types

### AMFile
Audio clip with channel control.

```json
{
  "_type": "AMFile",
  "src": 3,
  "trackNumber": 0,
  "attributes": {
    "ident": "background_music",
    "gain": 1.0,
    "mixToMono": false,
    "loudnessNormalization": true,
    "sourceFileOffset": 0
  },
  "channelNumber": "0,1",
  "parameters": {
    "volume": 1.0
  }
}
```

#### Audio Attributes
- **`gain`** (float): Audio gain multiplier
- **`mixToMono`** (boolean): Convert to mono
- **`loudnessNormalization`** (boolean): Apply normalization
- **`sourceFileOffset`** (integer): Offset in source file

## Image Media Types

### IMFile
Still image.

```json
{
  "_type": "IMFile",
  "src": 4,
  "parameters": {
    "translation0": 100.0,
    "translation1": 50.0,
    "scale0": 0.5,
    "scale1": 0.5,
    "opacity": 0.8
  }
}
```

## Annotation Types

### Callout
Visual annotation with shape and styling.

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
    "stroke-width": 3.0,
    "width": 240.0,
    "height": 180.0,
    "fill-style": "solid",
    "stroke-style": "solid"
  }
}
```

### Text Callout
Text-based annotation.

```json
{
  "_type": "Callout",
  "def": {
    "kind": "remix",
    "shape": "text",
    "style": "abstract",
    "text": "Hello World",
    "font": {
      "color-blue": 1.0,
      "color-green": 1.0,
      "color-red": 1.0,
      "size": 48.0,
      "tracking": 0.0,
      "name": "Arial",
      "weight": "Bold"
    },
    "horizontal-alignment": "center",
    "vertical-alignment": "center",
    "word-wrap": 1.0,
    "width": 400.0,
    "height": 100.0
  }
}
```

#### Callout Shapes
- `"shape-rectangle"`
- `"shape-rounded-rectangle"`
- `"shape-ellipse"`
- `"shape-triangle"`
- `"shape-pentagon"`
- `"shape-hexagon"`
- `"shape-cloud"`
- `"text"`

#### Text Attributes
```json
"textAttributes": {
  "type": "textAttributeList",
  "keyframes": [{
    "time": 0,
    "value": [
      {
        "name": "fontSize",
        "rangeStart": 0,
        "rangeEnd": 12,
        "value": 48.0,
        "valueType": "double"
      }
    ]
  }]
}
```

### Group
Container for nested media items.

```json
{
  "_type": "Group",
  "medias": [
    // Array of nested media items
  ],
  "parameters": {
    // Group-level transformations
  }
}
```

## Media Parameters

### Transform Parameters
All visual media supports these parameters:

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `translation0` | X position | 0.0 | -∞ to +∞ |
| `translation1` | Y position | 0.0 | -∞ to +∞ |
| `scale0` | X scale | 1.0 | 0.0 to +∞ |
| `scale1` | Y scale | 1.0 | 0.0 to +∞ |
| `rotation0` | X rotation | 0.0 | -360 to 360 |
| `rotation1` | Y rotation | 0.0 | -360 to 360 |
| `rotation2` | Z rotation | 0.0 | -360 to 360 |
| `opacity` | Transparency | 1.0 | 0.0 to 1.0 |

### Cropping Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| `geometryCrop0` | Left crop | 0.0 |
| `geometryCrop1` | Top crop | 0.0 |
| `geometryCrop2` | Right crop | 0.0 |
| `geometryCrop3` | Bottom crop | 0.0 |

## Media Metadata

```json
"metadata": {
  "clipSpeedAttribute": false,
  "effectApplied": "none",
  "audiateLinkedSession": "",
  "mediaType": "video"
}
```

## Asset Properties

For grouped visual elements:

```json
"attributes": {
  "assetProperties": [{
    "type": 1,
    "name": "Callout",
    "objects": [41],
    "themeMappings": {
      "fill": "background-1"
    }
  }]
}
```

## Best Practices

1. **Type Selection**
   - Match content to appropriate media type
   - Use UnifiedMedia for synchronized video/audio
   - Use Groups for complex annotations

2. **Parameter Defaults**
   - Include default transform values
   - Set opacity to 1.0 unless fading
   - Initialize scale to 1.0

3. **ID Management**
   - IDs must be unique across timeline
   - Use sequential numbering
   - Don't reuse IDs

4. **Source References**
   - Verify source exists in sourceBin
   - Match trackNumber to available tracks
   - Handle missing sources gracefully