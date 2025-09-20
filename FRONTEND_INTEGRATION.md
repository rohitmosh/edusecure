# EduSecure Frontend Integration Guide

## Overview

The EduSecure system now has complete frontend-backend integration with real image upload, processing, and preview functionality.

## Features Implemented

### ✅ Faculty Upload Interface
- **Real PDF/Image Upload**: Upload actual PDF or image files
- **Live Processing Feedback**: Real-time progress indicators during upload
- **Actual Image Preview**: View real scrambled and original images after upload
- **Scheduled Release**: Set custom release times for exams
- **Upload Results**: See detailed upload statistics and metadata

### ✅ Admin Dashboard
- **Paper Management**: View all uploaded exam papers
- **Key Release Control**: Release chaos keys at scheduled times
- **Integrity Verification**: Verify paper integrity with SHA-256 hashes
- **System Logs**: View tamper-proof audit logs

### ✅ Exam Center Interface
- **Paper Download**: Download scrambled exam papers
- **Real Image Preview**: View actual scrambled images
- **Key-based Decryption**: Decrypt papers when keys are released
- **Live Status Updates**: Real-time updates on key release status

## Quick Start

### Option 1: Complete System Startup (Recommended)
```bash
python start_complete_system.py
```
This will:
1. Create test files
2. Start the backend server
3. Test system integration
4. Start the frontend development server

### Option 2: Manual Startup

1. **Start Backend Server:**
   ```bash
   python run_backend.py
   ```

2. **Create Test Files:**
   ```bash
   python create_test_pdf.py
   ```

3. **Test Backend Integration:**
   ```bash
   python test_frontend_integration.py
   ```

4. **Start Frontend:**
   ```bash
   npm install
   npm run dev
   ```

## Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Faculty | faculty1 | faculty123 |
| Admin | admin1 | admin123 |
| Exam Center | center1 | center123 |

## Testing the Complete Workflow

### 1. Faculty Upload Test
1. Login as `faculty1`
2. Enter exam title (e.g., "Math Final Exam")
3. Select the `test.pdf` file
4. Set a scheduled release time (optional)
5. Click "Secure Upload"
6. Watch the real-time processing steps
7. View the actual scrambled and original images in the preview

### 2. Admin Management Test
1. Login as `admin1`
2. View all uploaded papers in the dashboard
3. Verify paper integrity
4. Release chaos keys at scheduled times
5. View system audit logs

### 3. Exam Center Test
1. Login as `center1`
2. View available exam papers
3. Download scrambled papers
4. View actual scrambled images
5. Decrypt papers when keys are released (by admin)

## Key Features Demonstrated

### Real Image Processing
- ✅ PDF to image conversion using pdf2image
- ✅ Chaotic pixel scrambling with visual verification
- ✅ Original image preservation for preview
- ✅ SHA-256 hash generation for integrity

### Security Features
- ✅ Homomorphic encryption for metadata
- ✅ Time-locked key release system
- ✅ Tamper-proof audit logging
- ✅ Role-based access control

### User Experience
- ✅ Real-time upload progress
- ✅ Live image previews
- ✅ Responsive error handling
- ✅ Intuitive role-based interfaces

## File Structure

```
├── backend/
│   ├── app.py              # Main Flask application
│   ├── upload.py           # Upload processing logic
│   ├── chaotic.py          # Chaotic scrambling algorithms
│   ├── phe_wrapper.py      # Homomorphic encryption
│   └── ...
├── src/
│   ├── components/
│   │   ├── FacultyUpload.tsx    # Enhanced faculty interface
│   │   ├── ImagePreview.tsx     # Real image preview component
│   │   ├── AdminDashboard.tsx   # Admin management interface
│   │   └── ExamCenterView.tsx   # Exam center interface
│   └── ...
├── papers/                 # Uploaded exam papers storage
├── test.pdf               # Generated test file
└── run_backend.py         # Backend server runner
```

## Troubleshooting

### Backend Issues
- **Port 5000 in use**: Change port in `run_backend.py`
- **Missing dependencies**: Run `pip install -r backend/requirements.txt`
- **Poppler not found**: Run `python install_poppler_windows.py`

### Frontend Issues
- **Node modules missing**: Run `npm install`
- **Port 5173 in use**: Vite will automatically use next available port
- **API connection failed**: Ensure backend is running on port 5000

### Upload Issues
- **PDF conversion fails**: Install poppler-utils
- **Images not showing**: Check browser console for CORS issues
- **Upload stuck**: Check backend logs for detailed error messages

## API Endpoints

### Faculty Endpoints
- `POST /api/faculty/upload` - Upload exam papers
- `GET /api/preview/info/{exam_id}` - Get preview information
- `GET /api/preview/original/{exam_id}/{page}` - Get original image
- `GET /api/preview/scrambled/{exam_id}/{page}` - Get scrambled image

### Admin Endpoints
- `GET /api/admin/papers` - List all papers
- `POST /api/admin/release_key/{exam_id}` - Release chaos key
- `GET /api/admin/verify_integrity/{exam_id}` - Verify integrity
- `GET /api/admin/logs` - Get audit logs

### Exam Center Endpoints
- `GET /api/examcenter/papers` - List available papers
- `GET /api/examcenter/download/{exam_id}` - Download scrambled paper
- `POST /api/examcenter/decrypt/{exam_id}` - Decrypt paper

## Next Steps

1. **Production Deployment**: Configure for production environment
2. **Database Integration**: Replace file-based storage with database
3. **Advanced Security**: Add additional encryption layers
4. **Performance Optimization**: Optimize image processing for large files
5. **Mobile Support**: Enhance responsive design for mobile devices

## Support

For issues or questions:
1. Check the browser console for frontend errors
2. Check backend logs for server errors
3. Run the integration test: `python test_frontend_integration.py`
4. Verify all dependencies are installed correctly