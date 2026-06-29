# Camtasia .tscproj Format Specification

## Summary

The `.tscproj` file is Camtasia's project format saved as JSON. It includes:
- **Canvas size** (`width`, `height`) and basic settings
- **Source media** (`sourceBin`) – imported files with metadata
- **Timeline layout** (`timeline`) – scenes, tracks, and clips
- **Transforms** – position, scale, rotation, opacity
- **Animations** – keyframe-driven property changes over time
- **Effects & transitions** – visual/audio effects between clips

Key scaling properties:
- Root `width`/`height`: canvas dimensions
- `rect`: `[x, y, width, height]` defining media bounds
- `translation0`/`translation1`: X/Y positioning
- `scale0`/`scale1`: X/Y scaling factors
- Keyframe values: for animated properties

## Contents

1. **@01-overview.md** – General Structure and Purpose  
   - JSON structure  
   - Main components: root, sourceBin, timeline  
   - File references and paths  
   - Use cases  

2. **@02-root-properties.md** – Root-Level Settings  
   - Metadata: title, author, description  
   - Canvas dimensions and aspect ratio  
   - Frame rate and audio config  
   - Version info and authoring tool details  
   - Edit rate and time format  

3. **@03-source-media.md** – Media Management  
   - `sourceBin` layout  
   - File references and paths  
   - Track types: video, audio, image  
   - Metadata per source  
   - Loudness normalization  

4. **@04-timeline-structure.md** – Timeline Layout  
   - Scene and track hierarchy  
   - Track indexing and layering  
   - Clip placement on tracks  
   - Track parameters and settings  
   - Magnetic tracks and locking behavior  

5. **@05-media-types.md** – Media Item Categories  
   - Video: VMFile, ScreenVMFile, UnifiedMedia  
   - Audio: AMFile  
   - Image: IMFile  
   - Annotations: Callout, Group  
   - Text and shape callouts  

6. **@06-animation-keyframes.md** – Animation Mechanics  
   - Keyframe structure  
   - Interpolation methods  
   - Animated properties  
   - Time handling in keyframes  
   - Animation tracks  

7. **@07-effects-transitions.md** – Effects and Transitions  
   - Applying and configuring effects  
   - Transition types and duration  
   - Audio/visual pre-roll  
   - Effect attributes  
   - Transition placement  

8. **@08-positioning-scaling.md** – Coordinate Systems  
   - Canvas coordinates  
   - Rectangle arrays (`rect`, `trackRect`)  
   - Translation and positioning  
   - Scale factors and transformations  
   - Rotation (X, Y, Z axes)  
   - Cropping  
   - Opacity and blending  

9. **@09-version-differences.md** – Version Compatibility  
   - Version 4.0: Camtasia 2020 and earlier  
   - Version 9.0: Camtasia 2021+  
   - Edit rate differences  
   - Time format changes  
   - Feature updates by version  
   - Backward compatibility notes  

## Quick Reference

### Core Scaling Properties
```json
{
  "width": 1920.0,           // Canvas width
  "height": 1080.0,          // Canvas height
  "sourceBin": [{
    "rect": [0, 0, 1920, 1080],  // Source bounds
    "trackRect": [0, 0, 1920, 1080]  // Track bounds
  }],
  "timeline": {
    "tracks": [{
      "medias": [{
        "parameters": {
          "translation0": 0.0,   // X position
          "translation1": 0.0,   // Y position
          "scale0": 1.0,         // X scale
          "scale1": 1.0          // Y scale
        }
      }]
    }]
  }
}
```

### Version Check
- **Version 4.0**: `editRate: 60`  
- **Version 9.0**: `editRate: 705600000`