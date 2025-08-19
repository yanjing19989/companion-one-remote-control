# Copilot Instructions for Companion One Remote Control

## Project Overview

This is a Flask-based web application designed for uploading, managing, and displaying images on "Companion One" 3D holographic displays connected to non-desktop Linux systems. The application provides remote control capabilities through a web interface and supports converting 2D images to 3D holographic displays using WebGL shaders.

## Technology Stack

- **Backend**: Python Flask
- **Image Processing**: PIL (Pillow)
- **Frontend**: HTML5, CSS3, JavaScript, jQuery, Bootstrap
- **3D Rendering**: WebGL with custom GLSL shaders
- **Display Control**: FBI (frame buffer imageviewer) for Linux
- **File Management**: Standard filesystem operations

## Architecture

### Core Components

1. **web.py**: Main Flask application with RESTful API endpoints
2. **templates/**: HTML templates for different display modes
   - `index.html`: Main upload/management interface
   - `depth.html`: Depth map to 3D converter
   - `40.html`: Quilt image (5x8 grid) to 3D converter
3. **static/**: Client-side assets (jQuery, Bootstrap, CamanJS)

### Key Features

- Multi-folder image organization
- Real-time 3D preview with adjustable parameters
- Slideshow and autoplay modes
- Thumbnail generation
- Remote system shutdown
- Bilingual interface (English/Chinese)

## Coding Conventions

### Python (Flask Backend)

- Use snake_case for function and variable names
- Global variables for application state (CURRENT_UPLOAD_FOLDER, lastpid, auto_play_active)
- Comprehensive error handling with try-catch blocks
- Chinese comments for complex logic
- RESTful API design with proper HTTP methods
- JSON responses for AJAX endpoints

### Frontend (HTML/JavaScript)

- Use Bootstrap classes for responsive design
- jQuery for DOM manipulation and AJAX calls
- WebGL with custom shaders for 3D rendering
- Event-driven architecture for user interactions
- Real-time parameter updates with range inputs

### File Structure

- Images stored in configurable upload directories
- Thumbnails generated automatically in parallel structure
- Folder-based organization with recursive directory support

## Development Guidelines

### Adding New Features

1. **API Endpoints**: Add routes to `web.py` following RESTful conventions
2. **Frontend**: Use existing Bootstrap/jQuery patterns for consistency
3. **3D Features**: Extend WebGL shaders in template files, following the uniform/attribute naming conventions
4. **Error Handling**: Always include try-catch blocks for file operations and external commands

### WebGL Development

- Uniforms use `u_` prefix (e.g., `u_lineNumber`, `u_obliquity`)
- Fragment shaders handle both depth map and quilt image processing
- Control parameters are synchronized between HTML inputs and shader uniforms
- Use precise floating-point ranges for fine-tuning 3D parameters

### System Integration

- FBI commands use `sudo` for display control
- Process management for slideshow functionality
- File permissions important for upload/thumbnail directories
- Linux framebuffer targeting with `-T 1` parameter

### Testing Considerations

- Test image upload with various formats
- Verify 3D parameter ranges produce valid output
- Check folder creation and permission handling
- Validate slideshow timing and control responsiveness

## Common Patterns

### AJAX Responses
```python
return jsonify({
    'success': True/False,
    'message': 'Description',
    'data': additional_data
})
```

### WebGL Uniform Updates
```javascript
gl.uniform1f(uniforms.u_parameterName, parseFloat(document.getElementById('parameterId').value));
```

### File Path Handling
- Always use `os.path.join()` for cross-platform compatibility
- Validate paths against base directories for security
- Generate thumbnails in parallel directory structure

### Error Handling
- Graceful degradation for missing files or permissions
- User-friendly error messages in both languages
- Console logging for debugging complex WebGL operations

## Security Considerations

- File upload validation and type checking
- Path traversal prevention in folder operations
- Sanitized file names and extensions
- Restricted directory access with base path validation

## Performance Notes

- Thumbnail generation on upload to reduce load times
- WebGL texture management for large images
- Process cleanup for FBI instances to prevent resource leaks
- Threading for autoplay functionality to maintain UI responsiveness