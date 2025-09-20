# Design Document

## Overview

This design addresses the PDF upload completion issues and preview image display problems in the EduSecure system. The solution involves fixing the upload process flow, ensuring proper metadata creation, and correcting the preview API endpoints to serve actual images.

## Architecture

The fix involves three main components:
1. **Upload Process Enhancement** - Ensure complete upload workflow execution
2. **Preview API Correction** - Fix image serving endpoints 
3. **Error Handling Improvement** - Add proper error handling and logging

## Components and Interfaces

### Upload Process Flow

The current upload process in `backend/upload.py` has the following flow:
1. File validation and temporary storage
2. PDF to image conversion
3. Image scrambling with chaos key
4. Metadata creation and encryption
5. Cleanup of temporary files

**Issue Identified:** The process may be failing during metadata creation or cleanup phases.

**Solution:** Add comprehensive error handling and ensure all steps complete successfully before returning success response.

### Preview API Endpoints

Current endpoints in `backend/app.py`:
- `/api/preview/info/<exam_id>` - Returns preview information
- `/api/preview/original/<exam_id>/<page>` - Serves original images
- `/api/preview/scrambled/<exam_id>/<page>` - Serves scrambled images

**Issue Identified:** Endpoints may not be correctly locating or serving image files.

**Solution:** Fix file path resolution and add proper error handling for missing files.

### Frontend Preview Component

The `ImagePreview.tsx` component handles:
- Fetching preview information
- Displaying original and scrambled images
- Page navigation controls

**Issue Identified:** Component may not be handling API errors properly or image loading states.

**Solution:** Improve error handling and loading states in the component.

## Data Models

### Upload Response Model
```typescript
interface UploadResponse {
  success: boolean;
  exam_id?: string;
  total_pages?: number;
  scrambled_images?: number;
  message?: string;
  error?: string;
}
```

### Preview Info Model
```typescript
interface PreviewInfo {
  exam_id: string;
  scrambled_pages: number[];
  original_pages: number[];
  total_pages: number;
}
```

## Error Handling

### Upload Process Errors
- File validation failures
- PDF conversion errors
- Image scrambling failures
- Metadata creation failures
- File system operation errors

### Preview API Errors
- Missing exam directory
- Missing image files
- Permission errors
- File serving errors

### Frontend Error Handling
- API request failures
- Image loading failures
- Network connectivity issues

## Testing Strategy

### Backend Testing
1. Test upload process with various PDF files
2. Test preview API endpoints with existing exam data
3. Test error scenarios (missing files, permissions, etc.)
4. Verify metadata file creation

### Frontend Testing
1. Test image loading and display
2. Test error state handling
3. Test page navigation
4. Test permission-based image visibility

### Integration Testing
1. End-to-end upload and preview workflow
2. Cross-browser compatibility
3. Network error handling
4. File system edge cases

## Implementation Approach

### Phase 1: Fix Upload Process
1. Add detailed logging to upload process
2. Fix metadata creation issues
3. Ensure proper error handling and cleanup
4. Test upload completion

### Phase 2: Fix Preview API
1. Debug and fix image serving endpoints
2. Add proper file path resolution
3. Implement proper HTTP headers for images
4. Test API endpoints independently

### Phase 3: Frontend Improvements
1. Improve error handling in ImagePreview component
2. Add better loading states
3. Test image display functionality
4. Verify user experience

### Phase 4: Integration and Testing
1. Test complete upload-to-preview workflow
2. Verify all error scenarios
3. Performance testing
4. User acceptance testing